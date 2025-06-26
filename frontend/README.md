# Domain Registry ॱ Check

A clean, fast frontend for searching .ooo domain availability.

## Features

- **Random 50**: Shows 50 random domains on load
- **Real-time search**: Search through domains as you type
- **Mobile-first**: Responsive design that works perfectly on all devices
- **Minimal design**: Clean table layout with excellent attention to detail
- **Default fonts**: Uses system fonts for fast loading and accessibility

## Tech Stack

- SvelteKit 2.0
- Tailwind CSS
- Bun runtime
- TypeScript

## Getting Started

```bash
# Install dependencies
bun install

# Start development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview
```

## Data

The frontend uses a cached CSV file (`domains.csv`) containing:
- Domain names
- Status (free/taken)
- TTL (time to live in seconds)

---

*Generated with AI on 2025-01-11. Likely reviewed by a human* ॱ
