# Cultivation RPG: Agent Directives

## Vision Snapshot
- Deliver a systemic xianxia-inspired RPG where player choices echo through personal growth, faction politics, and evolving biomes.
- Extend the existing prototype loop (Meditate → Train → Explore → Breakthrough → Combat) into a living world with seasonal cadence, dynamic NPC agendas, and multiplayer-friendly foundations.
- Ship in narrative-driven Chapters; each Chapter unlocks new realms, disciplines, and regions while keeping earlier content relevant through scaling and prestige hooks.

## North-Star Pillars
1. **Authentic Cultivation Fantasy** – make breakthroughs and dao insights feel earned; communicate power shifts through mechanics, visuals, and narrative.
2. **Player-Authored Progression** – branching techniques, customizable sect affiliations, and base-building empower unique paths.
3. **Living Ecosystem** – biomes, factions, and world events react to the player’s cultivation stage and moral choices.
4. **Sustainable Systems** – modular architecture, data-driven content, and live operations tooling to support ongoing updates.

## HTML5 Tooling Stack (Installed)
- **Engine & Rendering:** `phaser@^3` for the core HTML5 gameplay framework.
- **State Management:** `mobx@^6` to coordinate reactive game state across cultivation, skills, and narrative systems.
- **Designer Tuning:** `tweakpane@^4` for live balancing panels during playtests.
- **UI Layering:** `@floating-ui/dom@^1` to drive contextual HUDs, tooltips, and popovers.
- **Audio:** `howler@^2` enabling cross-platform SFX/music playback.
- **Narrative Runtime:** `inkjs@^1` to execute Ink-authored side stories and branching dialogue in browser builds.
- **Dev Workflow:** `vite@^7`, `typescript@^5`, `eslint@^9`, `prettier@^3`, and `vitest@^3` powering HMR, strict typing, linting, formatting, and automated tests.

---

## Agent Briefs

### Agent Aether (Creative Director)
- Finalize game bible structure: tone guide, realm aesthetics, cultivation philosophy glossary.
- Approve Chapter roadmap (Road to Ascension: Mortal → Nascent Soul arcs) with milestone beats and key art requirements.
- Align cross-discipline reviews biweekly; keep canon consistent with design documents and narrative scripts.

### Agent Meridian (Lead Systems Designer)
- Expand core loop into layered systems: dual cultivation tracks (Body vs. Soul), sect reputation, artifact crafting, and companion bonds.
- Specify formulas for Qi flow, resource sinks, and difficulty curves through Realm tiers 1-6.
- Own balance matrix for skills, techniques, and enemy archetypes; provide tuning dashboards using telemetry hooks.

### Agent Forge (Principal Engineer)
- Architect service-oriented game backend: save-state service, combat resolver, world simulation tick loop.
- Evaluate engine options (Unity ECS vs. Godot 4) with prototype parity; document trade-offs and tooling needs.
- Define content pipeline (JSON/Scriptable Objects) and build automation for Chapter drops and live patches.

### Agent Lumen (UX & Accessibility Lead)
- Translate prototype UI into scalable layout: diegetic HUD, controller-first navigation, narrated screen reader support.
- Run 3 usability sprints targeting onboarding, breakthrough feedback, and combat clarity.
- Produce accessibility compliance matrix (WCAG 2.2 AA + game-specific heuristics).

### Agent Warden (Combat Designer)
- Broaden enemy taxonomy: beasts, rogue cultivators, spirit guardians, domain bosses, PvP ghosts.
- Draft stance-based combat extension: Quick, Control, Burst; integrate Qi skill trees and weapon forms.
- Prototype enemy AI behaviors (threat assessment, soft counters to player builds) and document telegraph standards.

### Agent Scribe (Narrative Director)
- Map main story arcs, faction questlines, and character-driven cultivation trials per Chapter.
- Collaborate with Systems to ensure narrative gating aligns with breakthroughs and sect politics.
- Establish narrative tooling (ink/Articy export) and localization-ready scripting format.

### Agent Terra (World & Economy Designer)
- Build biome kit: resources, climate cycles, dungeon seeds, rare event tables.
- Define settlement upgrade paths, spirit farm mechanics, and trading caravans linked to faction favor.
- Own economy model across single-player and optional co-op hubs; prevent inflation through sinks and soft resets.

### Agent Pulse (Audio Director)
- Craft audio identity board: realm ambience layers, breakthrough motifs, combat SFX taxonomy.
- Plan adaptive score reacting to Qi thresholds, enemy threat, and weather phenomena.
- Scope VO plans for mentors, faction leaders, and ritual chants; coordinate localization budget.

### Agent Loom (Art & Animation Lead)
- Produce style guide referencing ink-wash inspirations blended with neon spiritual energy.
- Deliver character pipeline (high-level concept → rigged in-engine assets) and VFX language for cultivation techniques.
- Coordinate environment modular kits for each Chapter; ensure performance budgets align with engineering targets.

### Agent Echo (Analytics & Live Ops)
- Stand up telemetry schema: session flow, breakthrough attempts, economy transactions, churn signals.
- Prototype live event framework (seasonal tournaments, realm invasions) with configurable rewards.
- Partner with Community to design feedback loops, surveys, and patch-note comms cadence.

### Agent Lens (QA & Release Manager)
- Develop test plan covering core loop, Chapter regression, cross-save, and multiplayer sync.
- Automate scenario suites for meditation economy, breakthrough odds, combat edge cases, and narrative flags.
- Own release checklist, certification requirements, and hotfix protocols.

---

## Milestone Cadence
- **M0 – Foundations (Month 1-2):** Engine decision, vertical slice spec, content pipeline scaffold.
- **M1 – Core Loop (Month 3-5):** Prototype parity in engine, expanded progression to Foundation Establishment tier, baseline AI.
- **M2 – Chapter One Alpha (Month 6-8):** Fully playable loop with one major region, faction questline, stance combat prototype.
- **M3 – Systems Beta (Month 9-11):** Economy tuning, base-building, social hub test, analytics integration.
- **Launch Prep (Month 12+):** Polish, localization, performance, marketing beats, live ops tooling.

---

## Collaboration Rituals
- Weekly cross-discipline stand-up anchored around player journey goals.
- Fortnightly playtest reviews with annotated telemetry dashboards.
- Monthly roadmap retro to adjust feature scope, mitigate risks, and iterate on community feedback.

## Kickoff Convergence
- **Pre-Work (Day -3 to -1):**
  - Agent Forge drafts vertical-slice tech map and dependency board.
  - Agent Meridian prepares core loop expansion storyboard with risk callouts.
  - Agent Scribe circulates Chapter One narrative spine and faction primer.
  - Agent Lumen compiles prototype UX pain points and accessibility deltas.
  - Agent Echo gathers reference analytics dashboards; Agent Lens seeds test matrix shell.
- **Live Session (Day 0, 3 hrs):**
  - Opening vision sync led by Agent Aether (15 min) framing pillars and success metrics.
  - Lightning share-outs (10 min each) from Forge, Meridian, Scribe, Terra, Warden, Lumen on pre-work artefacts.
  - Breakout workshops (60 min):
    - Loop & Systems pod (Meridian, Terra, Warden, Echo) maps milestone scope + telemetry needs.
    - Narrative & UX pod (Aether, Scribe, Lumen, Loom) aligns player journey with visual/audio beats.
    - Tech & QA pod (Forge, Lens, Pulse) locks engine eval criteria, automation targets, and tooling gaps.
  - Regroup (45 min) to stitch dependencies, confirm Chapter One Definition of Done, assign owners.
  - Close with risk/decision log review and next-step commitments (15 min).
- **Follow-Through (Day +1 to +5):**
  - Publish kickoff minutes, updated roadmap, and task board swimlanes.
  - Agents own breakout outputs as living documents; first cross-discipline stand-up validates alignment.
  - Capture outstanding decisions (multiplayer scope, monetization, platform) for executive sync.

## Definition of Done (per feature)
- Design spec signed off by relevant agents.
- Playtest or simulation data reviewed; balance adjustments documented.
- Accessibility, localization, and telemetry hooks verified.
- QA regression suite updated; release notes drafted.

## Open Questions
- Multiplayer scope (drop-in co-op vs. asynchronous sect support) – needs greenlight by M1.
- Monetization strategy (premium vs. expansions vs. cosmetic season pass) – collaborate with Agent Echo before M2.
- Cross-platform targets (PC first? Console?) – decision influences engine/tooling budgets.
