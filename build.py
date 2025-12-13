#!/usr/bin/env python3
"""
Static site generator for squimmyai.github.io

Converts markdown posts to HTML using Jinja2 templates.
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
import markdown
from jinja2 import Environment, FileSystemLoader


# Paths
ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "dist"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()
    return frontmatter or {}, body


def process_notes(html: str) -> str:
    """
    Convert custom note syntax to HTML tooltips.

    Syntax: {note: visible text}(tooltip content)
    Output: <span class="note">visible text<span class="note-content">tooltip content</span></span>
    """
    pattern = r'\{note:\s*([^}]+)\}\(([^)]+)\)'

    def replace_note(match):
        visible_text = match.group(1).strip()
        tooltip_content = match.group(2).strip()
        return f'<span class="note">{visible_text}<span class="note-content">{tooltip_content}</span></span>'

    return re.sub(pattern, replace_note, html)


def render_markdown(content: str) -> str:
    """Convert markdown to HTML with extensions."""
    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    html = md.convert(content)
    html = process_notes(html)
    return html


def load_posts() -> list[dict]:
    """Load all posts from the posts directory."""
    posts = []

    if not POSTS_DIR.exists():
        return posts

    for post_dir in POSTS_DIR.iterdir():
        if not post_dir.is_dir():
            continue

        article_path = post_dir / "article.md"
        if not article_path.exists():
            continue

        content = article_path.read_text()
        frontmatter, body = parse_frontmatter(content)

        # Required fields
        if "title" not in frontmatter or "date" not in frontmatter:
            print(f"Warning: Skipping {post_dir.name} - missing title or date")
            continue

        # Parse date
        date = frontmatter["date"]
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        elif isinstance(date, datetime):
            pass
        else:
            # yaml parses dates as datetime.date
            date = datetime.combine(date, datetime.min.time())

        posts.append({
            "slug": post_dir.name,
            "title": frontmatter["title"],
            "date": date,
            "date_formatted": date.strftime("%b %d, %Y"),
            "category": frontmatter.get("category"),
            "subtitle": frontmatter.get("subtitle"),
            "excerpt": frontmatter.get("excerpt", ""),
            "content_html": render_markdown(body),
        })

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build():
    """Build the static site."""
    print("Building site...")

    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    index_template = env.get_template("index.html")
    post_template = env.get_template("post.html")

    # Load posts
    posts = load_posts()
    print(f"Found {len(posts)} posts")

    # Render index page
    index_html = index_template.render(posts=posts)
    (OUTPUT_DIR / "index.html").write_text(index_html)
    print("Generated index.html")

    # Render each post
    for post in posts:
        post_dir = OUTPUT_DIR / post["slug"]
        post_dir.mkdir(parents=True)

        post_html = post_template.render(post=post)
        (post_dir / "index.html").write_text(post_html)
        print(f"Generated {post['slug']}/index.html")

    # Create .nojekyll file
    (OUTPUT_DIR / ".nojekyll").write_text("")

    print(f"Build complete! Output in {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
