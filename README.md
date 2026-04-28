# Phuket Interactive Textbook — Project Handoff

This folder is a self-contained handoff to Claude Code for building an interactive HTML textbook about Phuket.

## What's in here

| File | Purpose |
|------|---------|
| `migrations-map.html` | The working Chapter 1 — drop-in functional. Open in any browser. |
| `BRIEF.md` | The main project brief — vision, structure, technical constraints. **Start here.** |
| `DESIGN_NOTES.md` | Visual reference — colors, typography, components, recurring patterns. |
| `CHAPTER_IDEAS.md` | Expanded notes on each proposed chapter. |
| `README.md` | This file. |

## How to hand this off to Claude Code

1. Save this entire folder somewhere on your computer (e.g. `~/projects/phuket-textbook/`).
2. Open a terminal in that folder.
3. Start Claude Code: `claude`
4. Paste the prompt below.

## Suggested first prompt for Claude Code

> I'm building an interactive HTML textbook about Phuket. The folder you're in contains everything you need to get oriented:
>
> - Read `BRIEF.md` first — it explains the project, the design philosophy, and what I'd like you to do.
> - `DESIGN_NOTES.md` is the visual reference. Match these patterns.
> - `CHAPTER_IDEAS.md` is the expanded chapter outline.
> - `migrations-map.html` is the working Chapter 1. Open it to see the aesthetic and interaction patterns I want to carry through.
>
> I'm a coding beginner, so please explain your changes plainly and don't refactor heavily without asking. After you've read the brief, tell me what you'd suggest as the first concrete step and ask me anything you need to know before starting.

## A note on the workflow

Claude Code can edit files, run commands, and iterate quickly — much better than this chat for a multi-file project. Once you're working with it:

- Open the HTML files directly in your browser (double-click) to preview as you go.
- Ask Claude Code to verify facts with web search before publishing anything you're unsure of.
- Phuket history has nuance — your local knowledge probably exceeds the model's. Trust your corrections.
