---
name: "css-guidelines"
description: "Provides all decisions and conventions for CSS styling used in the Task Manager project"
parameters:
  - name: component
    type: string
    description: "Optional specific UI component or context to style (e.g. task card, button, form)"
    required: false
---

# CSS Guidelines Prompt

This prompt explains the styling conventions, decisions, and choices used across the project. It can also generate example CSS snippets for a specified component.

## Design Decisions

- **Color Palette**: use muted blues and grays with accent colors for priority (red for critical, orange for high, blue for medium, green for low). Keep contrast high for accessibility.
- **Typography**: system font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`), base font size 16px, headings 1.5–2x.
- **Layout**: Flexbox for layout, responsive breakpoints at 600px and 900px. Use `container` class for max-width and centered content.
- **Spacing**: use a 8px scale (`.m-1` = 8px margin, `.p-2` = 16px padding, etc). Utility classes available in CSS file.
- **Class Naming**: BEM-inspired naming (`.task-list__item`, `.button--primary`). Keep selectors simple and avoid overly specific rules.
- **Buttons**: base `.button` class with modifiers `.button--primary`, `.button--danger`. Use `cursor: pointer;` and `transition: background-color 0.2s`.
- **Forms**: inputs have `.input` class, full width, 8px padding, border-radius 4px, border `1px solid #ccc`.
- **Responsive**: use `@media (max-width: 600px)` to stack columns and make buttons full-width.
- **Icons**: use SVG icons inline or via `<img>` with class `.icon` and fixed size 24px.
- **Dark Mode**: not currently supported but structure CSS with variables for easy switching later (`--bg-color`, `--text-color`).

## Example Usage

```html
<!-- task card -->
<div class="task-card task-card--high">
  <h3 class="task-card__title">Review PR</h3>
  <p class="task-card__description">Check code quality</p>
</div>
```

```css
.task-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 8px;
  transition: box-shadow 0.2s;
}
.task-card--high { border-left: 4px solid orange; }
.task-card__title { font-size: 1.125rem; margin-bottom: 4px; }
```

## Parameterized Generation

If a `component` is provided, include a focused CSS example and notes for that component. Otherwise return general guidelines.

## Usage Example

```bash
# Generate guidelines for a button component
# (the agent will substitute {{ component }} when running the prompt)
```


---
