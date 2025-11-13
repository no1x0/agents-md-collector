# agents.md

This file provides context and guidance for AI agents working on the Stage Plot Creator project.

## Development Workflow

### Build/Lint/Test Commands

- **Development server**: `npm run dev`
- **Build for production**: `npm run build`
- **Preview production build**: `npm run preview`
- **Lint code**: `npm run lint` (runs Prettier and ESLint checks)
- **Format code**: `npm run format` (runs Prettier to format files)
- **Run all tests**: `npm test`
- **Run unit tests only**: `npm run test:unit`
- **Run single unit test**: `npm run test:unit -- testNamePattern="specific test name"`
- **Run end-to-end tests**: `npm run test:e2e`
- **Type checking**: `npm run check`

### Code Style Guidelines

#### Imports

- Use ES modules with import/export syntax
- Group imports in order: built-in Node.js modules, external packages, internal modules
- Use absolute imports when possible with `$lib/` for library files

#### Formatting

- Use tabs for indentation (not spaces)
- Single quotes for strings
- No trailing commas
- Line width: 100 characters
- Semicolons are optional (follow existing code style)
- Files end with a newline

#### Types

- Use TypeScript for all new code
- Strict mode enabled (strict: true in tsconfig.json)
- Prefer interfaces over types for object shapes
- Use proper typing for Svelte components and stores

#### Naming Conventions

- Use camelCase for variables and functions
- Use PascalCase for components and classes
- Use UPPER_CASE for constants
- Use descriptive names that convey purpose
- Svelte files: +page.svelte, +layout.svelte, etc.

#### Svelte Conventions

- Component files end in .svelte
- Use TypeScript in Svelte files with lang="ts"
- Use reactive statements ($:) for derived values
- Use Svelte stores for global state management
- Follow SvelteKit file-based routing conventions

#### Error Handling

- Use try/catch blocks for async operations
- Provide meaningful error messages
- Handle errors at appropriate levels
- Use Svelte's error boundaries for UI errors

### Testing Strategy

- **Unit Tests**: Components tested in browser environment with Vitest. Use `describe/it` blocks with clear descriptions. Test both component rendering and behavior.
- **E2E Tests**: Critical user flows tested with Playwright.
- **Manual Testing**: Always test both light and dark modes

### Code Quality

- **TypeScript**: Strict typing required for all new code
- **Accessibility**: ARIA attributes and keyboard navigation essential
- **Responsive**: Mobile-first design with Tailwind breakpoints
- **Performance**: Consider bundle size impact of new dependencies

## Project Status & History

### Recent Development (August 2025)

- **Dark Mode Implementation**: Successfully implemented using mode-watcher library with CSS custom properties
- **Advanced UI Components**: Added Bits UI for headless component primitives
- **Musician Management**: Created sophisticated MusicianCombobox with search and autocomplete
- **Canvas Improvements**: Fixed dark mode canvas rendering and grid patterns

### Architecture Decisions Made

1. **Dark Mode Strategy**: Chose mode-watcher + CSS custom properties over manual theme management
2. **Component Library**: Selected Bits UI for accessibility and flexibility over pre-styled alternatives
3. **State Management**: Continuing with Svelte 5 runes ($state, $props) for simplicity
4. **Styling Approach**: Using semantic color tokens for consistent theming across modes

## Current Priorities

### High Priority Features Needed

1. **Equipment Item Types**: Expand beyond "amp" items to support full equipment library
2. **Export Functionality**: PDF/image export for stage plots
3. **Save/Load**: Persistence layer for stage plot data
4. **Item Categories**: Better organization of equipment types in add modal

### Technical Debt

1. **Single Component File**: Main app logic is all in +page.svelte - needs componentization
2. **Hard-coded Items**: Equipment types and images are manually configured
3. **No Data Validation**: Missing input validation and error handling
4. **Performance**: Large equipment image library could benefit from lazy loading

## Component System

### Established Patterns

- **Custom Properties**: Use CSS custom properties for theming (--color-text-primary, etc.)
- **Bits UI Integration**: Leverage Bits UI primitives for complex interactions
- **Export Pattern**: Components in src/lib/components/, export via src/lib/index.ts
- **Props Interface**: Define TypeScript interfaces for component props

### Style System

```css
/* Color Tokens - Use these consistently */
--color-bg-primary: #ffffff; /* Main backgrounds */
--color-bg-secondary: #f9fafb; /* Secondary backgrounds */
--color-text-primary: #111827; /* Primary text */
--color-text-secondary: #4b5563; /* Secondary text */
--color-surface: #ffffff; /* Component surfaces */
--color-border-primary: #e5e7eb; /* Borders */
```

## Known Issues & Limitations

### Current Bugs

- Canvas items only support "amp" type visually
- No validation on form inputs
- Musicians panel could benefit from drag-and-drop reordering

### Browser Compatibility

- Requires modern browser supporting CSS custom properties
- Uses Svelte 5 features (runes syntax)
- Tailwind CSS 4 alpha may have edge cases

### Performance Considerations

- 500+ images in static/img/ directory
- Single-page application with no code splitting
- Canvas redraws on every interaction

## Integration Points

### External Libraries

- **mode-watcher**: Theme management (don't replace without strong reason)
- **Bits UI**: Component primitives (established pattern)
- **Tailwind CSS v4**: Styling framework (custom variant setup)

### File Structure

```
src/
├── lib/
│   ├── components/          # Reusable components
│   │   └── MusicianCombobox.svelte
│   └── index.ts            # Component exports
├── routes/
│   ├── +layout.svelte      # Theme setup
│   └── +page.svelte        # Main application
└── app.css                 # Global styles & tokens
```

## Future Agent Guidance

### When Adding Features

1. Check if existing components can be extended vs. creating new ones
2. Maintain theming consistency with established color tokens
3. Consider both light and dark mode appearance
4. Test keyboard navigation and screen reader compatibility
5. Update this file with significant architectural decisions

### When Debugging

1. Check browser console for Svelte/TypeScript errors
2. Verify dark mode styles are applied correctly
3. Test component interactions don't break canvas functionality
4. Ensure new features work with existing drag-and-drop system

### Communication Style

- Be concise and direct
- Focus on user's specific request
- Avoid unnecessary explanations unless asked
- Proactively use TodoWrite for complex multi-step tasks

This project values clean, accessible, and maintainable code over rapid feature addition.
