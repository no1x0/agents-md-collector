# OpenAI Codex Guidelines

This repository uses TypeScript and Lit to build web components, a browser extension, and a small PWA demo. When modifying code you should:

- Keep the codebase accessible and mobile friendly. Follow WCAG 2.1 AA guidelines and prefer responsive, mobile‑first layout techniques.
- Use the `webcomponents` package as the source of truth for the RSVP player component. Tests live under `webcomponents/src` and must pass via `npm test`.
- Run `npm run lint` before committing. The linter checks TypeScript code with ESLint (including `lit-a11y`) and CSS with Stylelint. **Warnings are treated as errors** so the build fails if any are present.
- New lint rules using SonarJS and Unicorn enforce software craftsmanship. Fix or disable warnings to keep code clean, DRY, and easy to maintain. Never commit with remaining warnings.
- Practice the Boy Scout Rule: whenever you touch code, run the linters and clean up any warnings you encounter.
- Follow Uncle Bob's Clean Code and Architecture guidelines. Keep modules small, respect SRP, and avoid needless repetition.
- When adding new features, include unit tests and ensure existing tests keep ≥90% coverage.
- GitHub Actions run `npm run lint` and `npm test`. Make sure they succeed locally before pushing.

- Always `git pull` from origin or merge the PR's destination branch before beginning a task. If origin isn't available, use `main`. Resolve any merge conflicts first.
- Record design decisions that deviate from existing docs under `docs/design/decisions/`.
- Take a test-driven approach, especially for new UI behaviour.
- Document preferences from conversations, noting whether they are standards or one-off exceptions.
- Override existing features gracefully, e.g. intercept swipe gestures so mobile browsers don't navigate back.
- Ensure documentation (including `README.md`) stays in sync with the latest code.

