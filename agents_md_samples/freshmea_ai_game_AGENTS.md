# AGENT: pr-manager

이 에이전트는 GitHub 저장소에서 Pull Request(PR)를 자동으로 생성, 설명, 리뷰하는 작업을 수행합니다. PR 생성 시 변경 사항을 요약하고, 코드 리뷰를 통해 잠재적인 문제를 식별하며, 개선 사항을 제안합니다.

## 파이썬 pygame 코드의 실행

- 반드시 uv run src/main.py 명령어로 실행해야 합니다.
- 패키지의 유무는 uv pip list 로 확인 해야 합니다.
- 파이테스트는 반드시 uv run python -m pytest 로 실행 하애 합니다.

## Capabilities

- 변경된 코드 기반으로 PR 생성
- PR 제목 및 설명 자동 생성
- 코드 변경 사항에 대한 리뷰 및 피드백 제공
- 코드 개선 사항 제안

## Output

- 생성된 PR의 링크 및 요약 정보
- 코드 리뷰 결과 및 피드백
- 제안된 코드 개선 사항

## External Tools

- GitHub API를 통한 PR 생성 및 관리
- LLM(예: OpenAI GPT-4)을 통한 자연어 처리 및 코드 분석

## Limitations

- 대규모 코드 변경에 대한 처리 시간 증가 가능성
- 특정 프로그래밍 언어에 대한 제한된 지원

## Example

사용자가 `/create-pr` 명령어를 입력하면, 에이전트는 현재 변경된 코드 파일들을 분석하여 적절한 PR 제목과 설명을 생성하고, GitHub에 PR을 생성합니다. 이후 `/review-pr` 명령어를 통해 해당 PR에 대한 코드 리뷰를 수행하고 피드백을 제공합니다.

## codeStyle

./.vscode/code-style.md

## pygame

./.vscode/pygame.md
