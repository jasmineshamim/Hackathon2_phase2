---
name: frontend-skills
description: Build modern frontend pages, reusable components, layouts, and styling for web applications. Use for UI development and frontend architecture.
---

# Frontend Development Skills

## Instructions

1. **Page Structure**
   - Use clear folder organization (`pages` / `app`)
   - Separate layout, page, and component responsibilities
   - Use semantic HTML structure
   - Ensure accessibility (aria labels, alt text)

2. **Component Design**
   - Build reusable and modular components
   - Keep components small and focused
   - Use props for configuration
   - Avoid duplicated UI logic
   - Follow consistent naming conventions

3. **Layout System**
   - Use responsive layouts (flexbox, grid)
   - Implement shared layouts for navigation and footer
   - Support mobile-first design
   - Maintain consistent spacing and alignment

4. **Styling**
   - Use Tailwind CSS or utility-first styling
   - Avoid inline styles
   - Follow consistent color and typography scale
   - Use responsive breakpoints properly
   - Maintain design consistency across pages

5. **State & Interaction**
   - Use client components only when interactivity is required
   - Manage local state cleanly
   - Handle loading and error states gracefully
   - Provide visual feedback for user actions

6. **Performance**
   - Optimize component rendering
   - Avoid unnecessary re-renders
   - Lazy load heavy components
   - Optimize images and assets

## Best Practices
- Mobile-first approach
- Keep UI predictable and consistent
- Prefer composition over large components
- Maintain clean folder structure
- Use meaningful component names
- Keep styling reusable
- Follow accessibility standards

## Example Structure
```tsx
// components/Button.tsx
export function Button({ label, onClick }) {
  return (
    <button className="px-4 py-2 rounded bg-black text-white" onClick={onClick}>
      {label}
    </button>
  )
}

// app/page.tsx
import { Button } from "@/components/Button"

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <Button label="Get Started" />
    </main>
  )
}
