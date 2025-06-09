### Context
check.webring.ooo is part of the webring.ooo project and it's made just for fun, but also to help people join by checking if the .ooo domain for their first name is available. The webring started because the .ooo is very cool. The webring's vibe is simple (like the internet of the past, HTML vibe) and potentially slightly playful (but in subtle ways, not over the top).

### Features
- instantly check and search a pre-cached list of <firstname>.ooo domains - are they free? are they already part of the webring?
- check any domain name, even if it's not a first name or not cached
- things are displayed in a table. search and check is the same box above the table - if there are no results in the cached firstnames thing, there is a button to search
- list of first names is stashed as names.csv. it contains a 100 examples for now, will be replaced with a longer list at some point

### Tech stack 
- FastAPI backend with async support for domain checking
- Svelte frontend for clean, lightweight UI
- `uv` and `ruff` for Python development
- `prettier` for Svelte formatting

### Tool stack
- Cursor with Claude 4 at the time of writing
- Taskmaster AI
- Puppeteer MCP
- Netlify or Vercel for hosting, or the new hip one from Code Uni