# AGENTS.md

##  Project Overview
This is a repository for **Agents.md Templates** — a collection of structured templates to standardize `AGENTS.md` guidelines for AI agents across projects. It provides conventions, examples, and starter templates so agents can easily understand and assist.

## ​ Setup & Build
- Install dependencies: `npm install` or `pnpm install`
- Run local server: `npm run dev` or `pnpm dev` (if applicable)
- Build (if needed): `npm run build` or `pnpm build`

##  Code Conventions
- Use Markdown for files and templates.
- Keep examples concise and realistic.
- Avoid overly verbose instructions that could clutter agent context.

##  Testing Instructions
- Lint templates: `npm run lint`
- (Optional) Test markdown: run your markdown linter (e.g., `markdownlint`)

##  Contribution & PR Guidelines
- Title format: `[Agents.md Templates] <brief description>`
- Ensure formatting and lint pass before opening PR.
- Include examples or use-cases with any new template.

##  Usage Notes
- Place more detailed `AGENTS.md` files inside subdirectories if you create specialized template modules.
- Agents automatically pick up the nearest `AGENTS.md` file based on the directory context. 

##  Reminders for Agents
- Always respect existing templates and conventions.
- If unsure, ask for clarification or a human review.
- This file is agent-focused—keep project background concise; non-agent documentation belongs in README.md.
