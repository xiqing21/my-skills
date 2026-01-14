---
name: react-shadcn-builder
description: This skill should be used when building React applications with TypeScript, Tailwind CSS, and shadcn/ui. Use this skill when creating web apps, adding UI components, or working with React projects that follow this tech stack specification. The skill enforces specific project structure, routing conventions, and component library usage patterns.
---

# React Shadcn Builder

## Overview

Enables rapid development of modern React applications using TypeScript, React Router, Tailwind CSS, and shadcn/ui components. Provides standardized project structure, routing conventions, and UI component patterns for consistent, maintainable web applications.

## When to Use This Skill

Use this skill when:
- Building a new React web application from scratch
- Adding new pages or components to an existing React project
- Working with TypeScript, React Router, and Tailwind CSS stack
- Creating UI components using shadcn/ui library
- Routing updates are needed in src/App.tsx
- Structuring React source code with proper folder organization

## Tech Stack Requirements

### Core Technologies
- **React**: Primary UI framework
- **TypeScript**: Type-safe JavaScript
- **React Router**: Client-side routing with routes defined in `src/App.tsx`
- **Tailwind CSS**: Utility-first CSS framework for all styling
- **shadcn/ui**: Pre-built accessible component library

### Project Structure
- `src/`: All source code directory
- `src/pages/`: Page components (e.g., `src/pages/Index.tsx` for default page)
- `src/components/`: Reusable UI components
- `src/App.tsx`: Central routing configuration (KEEP routes here)

### Available Libraries and Components
- `lucide-react`: Icon library (pre-installed)
- `shadcn/ui`: Complete component library with all dependencies installed
- `Radix UI`: All necessary primitives available

## Development Guidelines

### Component Creation Workflow

1. **Create Components**: Place reusable components in `src/components/`
2. **Create Pages**: Add page components in `src/pages/` with default page as `src/pages/Index.tsx`
3. **Update Routes**: Modify `src/App.tsx` to include new page routes
4. **Import shadcn/ui Components**: Use prebuilt components directly, do not edit shadcn/ui files
5. **Apply Tailwind Styling**: Use Tailwind utility classes for all layout, spacing, colors, and design aspects

### Critical Requirements

- **ALWAYS** try to use shadcn/ui components before creating custom ones
- **ALWAYS** update `src/App.tsx` when adding new pages - users cannot see components without routing
- **NEVER** edit shadcn/ui component files directly - create new components if customization is needed
- **ALWAYS** put source code in the `src` folder
- **KEEP** routing configuration in `src/App.tsx`

### Styling Best Practices

Use Tailwind CSS extensively for:
- Layout: flexbox, grid, positioning
- Spacing: margins, padding, gaps
- Colors: text colors, background colors, borders
- Typography: font sizes, weights, line heights
- Responsive design: breakpoints, mobile-first approach
- State styles: hover, focus, active states

### Component Usage Patterns

When working with shadcn/ui:
1. Import components from the shadcn/ui library
2. Use pre-styled components as building blocks
3. Apply Tailwind classes for layout and positioning
4. Create wrapper components only when extending functionality

Example import pattern:
```tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
```

## Routing Configuration

All routes must be defined in `src/App.tsx`. Keep the router configuration centralized and use consistent path naming conventions.

Example routing structure:
```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Index />} />
        {/* Add new routes here */}
      </Routes>
    </BrowserRouter>
  );
}
```

## Resources

This skill does not currently include bundled resources. All necessary dependencies (shadcn/ui, Radix UI, lucide-react) are assumed to be pre-installed in the project environment.
