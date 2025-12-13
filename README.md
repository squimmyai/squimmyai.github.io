# squimmyai.github.io

A minimal static site generator for a personal blog, built with Python and deployed via GitHub Actions.

## Project Structure

```
├── posts/                      # Blog posts (markdown)
│   └── <slug>/
│       └── article.md
├── templates/                  # Jinja2 HTML templates
│   ├── index.html              # Homepage listing all posts
│   └── post.html               # Individual post page
├── build.py                    # Build script
├── serve.py                    # Local development server
├── pyproject.toml              # Python dependencies (managed by uv)
└── .github/workflows/deploy.yml
```

## Writing Posts

Create a new directory in `posts/` with a URL-friendly slug name, then add an `article.md` file:

```
posts/
└── my-new-post/
    └── article.md
```

### Frontmatter

Each post requires YAML frontmatter at the top:

```yaml
---
title: "My Post Title"
date: 2024-11-14
category: Technology        # optional
subtitle: "A brief tagline" # optional, shown below the title
excerpt: "Summary text shown on the homepage listing."
---

Your markdown content here...
```

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | The post title |
| `date` | Yes | Publication date (YYYY-MM-DD) |
| `category` | No | Category label shown as a tag |
| `subtitle` | No | Italicized text below the title on the post page |
| `excerpt` | Yes | Summary shown on the homepage |

### Custom Syntax

#### Post Links

Link to other posts using wiki-style syntax:

```
Read more in [[sqlite-is-probably-fine]].
Or with custom text: [[sqlite-is-probably-fine|my previous post]].
```

- `[[slug]]` — renders as a link with the post's title
- `[[slug|custom text]]` — renders as a link with custom text

The build will warn if you link to a non-existent slug.

#### Note Tooltips

Add inline tooltips that appear on hover:

```
This is an {note: RFC}(Request for Comments — a document proposing technical decisions.) for review.
```

This renders as dashed-underlined text that shows a tooltip on hover.

## Local Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Setup

```bash
# Install dependencies
uv sync
```

### Build and Preview

```bash
# Build the site (outputs to dist/)
uv run build.py

# Start local server at http://localhost:8000
uv run serve.py
```

The typical workflow while writing:

1. Edit your markdown in `posts/<slug>/article.md`
2. Run `uv run build.py` to rebuild
3. Run `uv run serve.py` and open http://localhost:8000
4. Refresh the browser to see changes

## Deployment

The site is automatically deployed to GitHub Pages when you push to `main`.

### How it Works

1. Push triggers the GitHub Actions workflow (`.github/workflows/deploy.yml`)
2. The workflow installs uv and dependencies
3. Runs `build.py` to generate the site in `dist/`
4. Uploads `dist/` as a Pages artifact
5. Deploys to GitHub Pages

### First-Time Setup

1. Go to your repository Settings → Pages
2. Under "Build and deployment", set Source to **GitHub Actions**
3. Push to `main` — the workflow will handle the rest

The `dist/` folder is gitignored; it only exists during the CI build.

## Dependencies

Managed via uv in `pyproject.toml`:

- **jinja2** — HTML templating
- **markdown** — Markdown to HTML conversion
- **pyyaml** — Frontmatter parsing

## Customization

### Templates

Edit the files in `templates/`:

- `index.html` — Homepage with post listing
- `post.html` — Individual post layout

Both templates use Jinja2 syntax. The build script passes:

**index.html:**
- `posts` — List of all posts, sorted by date (newest first)

**post.html:**
- `post.title`
- `post.date_formatted` (e.g., "Nov 14, 2024")
- `post.category`
- `post.subtitle`
- `post.excerpt`
- `post.content_html` — Rendered markdown content

### Styling

CSS is embedded in the templates. The design uses:

- **JetBrains Mono** — UI elements, code blocks
- **Source Serif 4** — Body text, headings
- Warm sepia color palette
