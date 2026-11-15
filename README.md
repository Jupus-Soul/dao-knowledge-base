# Star Atlas DAO - Knowledge Base

The source of the Star Atlas DAO Knowledge Base website. Every change saved to the `main` branch is published automatically within a minute or two.

**Editors and admins: read [GUIDE.md](GUIDE.md).** It explains, in plain language, how to edit pages, how to add or remove editors, how the custom domain works, and how to move this repository to another GitHub account.

## How it is put together

| Part | What it does |
| --- | --- |
| `docs/` | The pages (one Markdown file each), plus images and documents in `docs/assets/` |
| `docs/**/.nav.yml` | The order of pages in the sidebar |
| `.pages.yml` | Settings for the visual editor, [Pages CMS](https://app.pagescms.org) |
| `mkdocs.yml` | Site settings (name, colours, features), built with MkDocs Material |
| `hooks/site_design.py` | Builds the page banners, cards, note boxes and home page automatically. The home page texts and section icons are listed at the top of this file |
| `docs/assets/extra.css` | Colours and styling |
| `.github/workflows/publish.yml` | Builds the site and publishes it to GitHub Pages on every save |

Nothing in this repository refers to a specific GitHub owner, so it keeps working after a transfer.

## Previewing on your own computer (optional, for technical users)

```
pip install -r requirements.txt
mkdocs serve
```
