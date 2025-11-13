#!/usr/bin/env python3
"""Search for AGENTS.md files and download the best matches in one pass."""

from __future__ import annotations

import argparse
import base64
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional, Sequence, Set, Tuple

from dotenv import load_dotenv
from github import Auth, Github, GithubException
from github.GithubException import RateLimitExceededException
from github.Repository import Repository

QUERY = "agents.md in:path extension:md"
DEFAULT_LIMIT = 100
MAX_RETRIES = 3


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch AGENTS.md examples directly into the downloads directory."
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum number of files to download (default: {DEFAULT_LIMIT}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("downloads"),
        help="Directory where downloaded files will be stored.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files if they already exist.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging verbosity (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger("fetch-agents")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


def load_token(logger: logging.Logger) -> str:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.error("GITHUB_TOKEN is not set. Please provide it via environment or .env.")
        sys.exit(1)
    return token


def wait_for_rate_limit(client: Github, resource: str, logger: logging.Logger) -> None:
    """Pause until the GitHub quota for a specific resource resets."""
    try:
        rate_limit = getattr(client.get_rate_limit(), resource)
        resource_name = resource.capitalize()
    except AttributeError:
        logger.error("Unknown rate-limit resource: %s. Waiting 60s as a fallback.", resource)
        time.sleep(60)
        return

    reset_time = rate_limit.reset
    reset_ts = reset_time.timestamp() if hasattr(reset_time, "timestamp") else time.time() + 60
    sleep_for = max(reset_ts - time.time() + 5, 5)
    logger.warning(
        "%s rate limit exceeded (remaining: %s). Sleeping for %.0f seconds.",
        resource_name,
        rate_limit.remaining,
        sleep_for,
    )
    time.sleep(sleep_for)


def sanitize_filename(repository: str, path: str, output_dir: Path) -> Path:
    owner, repo = repository.split("/", 1)
    sanitized = path.strip("/").replace("/", "_").replace("\\", "_")
    return output_dir / f"{owner}_{repo}_{sanitized}"


def decode_blob(repo: Repository, sha: str, client: Github, logger: logging.Logger) -> bytes:
    """Fetch file contents via git blob API with retry and rate-limit handling."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            blob = repo.get_git_blob(sha)
            return base64.b64decode(blob.content)
        except RateLimitExceededException:
            wait_for_rate_limit(client, "core", logger)
        except GithubException as exc:  # Retry on transient server issues
            if 500 <= exc.status < 600:
                logger.warning(
                    "Server error (%s) fetching blob %s. Attempt %d/%d.",
                    exc.status,
                    sha,
                    attempt,
                    MAX_RETRIES,
                )
                time.sleep(2**attempt)
                continue
            raise
    raise RuntimeError(f"Unable to fetch blob contents for {repo.full_name}@{sha}")


def search_and_download(
    client: Github,
    limit: int,
    output_dir: Path,
    overwrite: bool,
    logger: logging.Logger,
) -> Tuple[int, int]:
    search = client.search_code(query=QUERY, order="desc", sort="indexed")
    iterator = iter(search)
    seen: Set[str] = set()
    downloaded_count = 0
    processed_count = 0

    logger.info("Processing up to %d items from search results...", limit)

    while processed_count < limit:
        try:
            item = next(iterator)
        except StopIteration:
            logger.info("Search returned fewer items than the limit (%d).", processed_count)
            break
        except RateLimitExceededException:
            wait_for_rate_limit(client, "search", logger)
            continue
        except GithubException as exc:
            if 500 <= exc.status < 600:
                logger.warning("Search API error %s. Retrying after short pause.", exc.status)
                time.sleep(5)
                continue
            logger.error("Fatal GitHub API error %s: %s", exc.status, exc.data)
            break
        
        processed_count += 1
        key = f"{item.repository.full_name}:{item.path}"
        if key in seen:
            continue
        seen.add(key)

        output_path = sanitize_filename(item.repository.full_name, item.path, output_dir)
        if output_path.exists() and not overwrite:
            logger.info("Skipping %s (already exists).", output_path)
            continue

        try:
            file_bytes = decode_blob(item.repository, item.sha, client, logger)
        except RateLimitExceededException:
            wait_for_rate_limit(client, "core", logger)
            continue
        except GithubException as exc:
            logger.warning(
                "Failed to fetch blob %s (%s). Skipping entry.",
                item.sha,
                exc.status,
            )
            continue
        except RuntimeError as err:
            logger.warning(str(err))
            continue

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as handle:
            handle.write(file_bytes)
        logger.info("Downloaded %s -> %s", item.path, output_path)
        downloaded_count += 1

    # This log is now more of a debug-level detail, main will summarize.
    logger.debug("Processed %d items, downloaded %d new files.", processed_count, downloaded_count)
    return downloaded_count, processed_count


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    logger = configure_logging(args.log_level)
    token = load_token(logger)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    auth = Auth.Token(token)
    client = Github(auth=auth, per_page=100)

    logger.info("Executing query '%s' with limit=%d.", QUERY, args.limit)
    downloaded, processed = search_and_download(
        client=client,
        limit=args.limit,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
        logger=logger,
    )

    if downloaded == 0:
        if processed == 0:
            logger.warning("Search query did not return any results.")
        else:
            logger.info("No new files downloaded (all requested items already existed).")
    else:
        logger.info("Completed. Downloaded %d file(s).", downloaded)

    # Treat runs with zero available search results as failures, otherwise succeed even if nothing new
    return 0 if processed > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
