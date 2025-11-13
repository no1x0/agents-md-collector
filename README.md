# GitHub AGENTS.md Collector

A simple and efficient Python tool to find and download `AGENTS.md` files from public repositories on GitHub. This tool is designed to help researchers, developers, and AI enthusiasts gather a dataset of agent instructions for analysis.

This repository includes a `samples_top100` directory containing 100 sample files to allow for immediate exploration without any setup.

## Features

- **Find & Download:** A single script to find and directly download files.
- **Flexible Limits:** Control the number of files to download using the `-l` / `--limit` argument.
- **Custom Output:** Specify a custom download directory with `--output-dir`.
- **Idempotent:** Skips already downloaded files, making it efficient to run multiple times to fetch updates.
- **Overwrite Option:** Force re-downloading of all files with the `--overwrite` flag.
- **Configurable Logging:** Adjust the log verbosity for normal use or debugging.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *On Windows, use `venv\Scripts\activate`*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure GitHub Token:**
    - Create a `.env` file in the project root.
    - Add your GitHub Personal Access Token (with `public_repo` scope) to the file:
      ```
      GITHUB_TOKEN=github_pat_YourTokenHere...
      ```

## Usage

The primary script is `fetch_agents.py`.

**Basic Usage (downloads the default 100 files to `downloads/`):**
```bash
python3 fetch_agents.py
```

**Download a specific number of files:**
```bash
python3 fetch_agents.py -l 20
```

**Download to a custom directory:**
```bash
python3 fetch_agents.py --limit 50 --output-dir my_custom_folder
```

**Force re-download of all files:**
```bash
python3 fetch_agents.py -l 100 --overwrite
```

**Get help on all commands:**
```bash
python3 fetch_agents.py --help
```

## License

This project is licensed under the MIT License.
