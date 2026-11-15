# Guide for admins and editors

This guide is written for people who are not technical. There are four parts:

1. [How editors edit pages](#1-how-editors-edit-pages)
2. [Adding and removing editors](#2-adding-and-removing-editors-admins)
3. [Using the address staratlasdaocouncil.com](#3-using-the-address-staratlasdaocouncilcom-admins)
4. [Moving the site to the DAO's GitHub](#4-moving-the-site-to-the-daos-github-admins)

The site costs nothing to run. GitHub hosts it for free, and the visual editor (Pages CMS) is free.

---

## 1. How editors edit pages

Editing happens in a visual editor that looks like a simple word processor. There is no code, and nothing to "merge".

1. Go to **https://app.pagescms.org** and sign in (with GitHub, or with the email address you were invited with).
2. Open **dao-knowledge-base**.
3. Click **Pages** on the left. You see the same folders as the site's sidebar (Overview, Governance, Archive, ...).
4. Click a page to open it. Change the text, add headings, lists, links or images with the toolbar.
5. Click **Save**. The live site updates by itself in one to two minutes.

Good to know:

- **Add a page:** open the folder it belongs in and click **Add an entry**. Give it a title and write the content. It appears at the bottom of that section in the sidebar.
- **Add an image:** use the image button in the toolbar and upload a picture.
- **A page that has sub-pages** is stored in a folder, and the page itself is the entry called **index** inside that folder.
- **Cover image:** every page already gets a Star Atlas artwork banner chosen by its section. To use a different picture on one page, upload it in that page's optional **Cover image** field.
- **Note boxes:** use the quote button and start the text with an emoji. ℹ️ makes a blue note, 💡 or ✅ a green one, ⚠️ an amber warning and 🚫 a red one. A quote without an emoji stays a normal quote.
- **Link cards:** a line that contains only ➡️ followed by a link to another page turns into a card. Several such lines in a row become a grid of cards.
- **Automatic parts:** the banner with the page title, the cards for sub-pages on section pages, and the home page's banner and section cards are made automatically. You never have to edit them.
- **Undo a mistake:** every save is kept forever in the history. Ask an admin to restore an earlier version (on GitHub: open the file, click **History**).
- **Change the order of pages in the sidebar** or the name of a section: ask an admin. The order lives in small files called `.nav.yml` inside each folder of `docs/`.

---

## 2. Adding and removing editors (admins)

Only people you approve can edit. Everyone else can only read the public site. There are two ways to give someone access. Use whichever suits the person.

### Option A: invite by email (easiest, no GitHub account needed)

1. Go to **https://app.pagescms.org**, sign in with GitHub and open **dao-knowledge-base**.
2. Open **Collaborators** in the menu on the left.
3. Type the person's email address and send the invitation. They get an email with a sign-in link.
4. **To remove someone:** go to the same list and remove them.

People invited this way can edit pages and upload images. They cannot change settings or invite others.

### Option B: add them on GitHub (for co-admins)

Use this for people who should be able to manage the site with you.

1. On GitHub, open the repository, then **Settings**, then **Collaborators** (later, in the DAO organization, use a team with **Write** access instead).
2. Click **Add people**, enter their GitHub username and send the invitation.
3. Once they accept, they sign in at https://app.pagescms.org with GitHub and can edit.
4. **To remove someone:** go to the same list and click **Remove**.

### One-time setup of the editor (the repository owner does this once)

1. Go to **https://app.pagescms.org** and sign in with GitHub.
2. When asked, **install the Pages CMS GitHub App**. Choose **Only select repositories** and pick **dao-knowledge-base**.
3. Open **dao-knowledge-base** in Pages CMS. You are ready to edit and invite people.

---

## 3. Using the address staratlasdaocouncil.com (admins)

Until this is done, the site lives at `https://<github-owner>.github.io/dao-knowledge-base/`. These steps point your own address at it. Do them in this order.

### Step 1: Cloudflare

1. Log in to Cloudflare, click **staratlasdaocouncil.com**, then **DNS**, then **Records**.
2. If there are already records of type **A**, **AAAA** or **CNAME** with the name `@` (or `staratlasdaocouncil.com`) or `www`, delete them. Leave everything else alone, especially **MX** and **TXT** records (those are for email).
3. Click **Add record** and add these five records. For each one, switch **Proxy status** off so it shows a grey cloud and says **DNS only**.

| Type | Name | Content / Target |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `<github-owner>.github.io` |

Replace `<github-owner>` with the GitHub account that owns the repository, in lower case. Today that is `jupus-soul`, so the target is `jupus-soul.github.io`.

### Step 2: GitHub

1. Open the repository on GitHub, then **Settings**, then **Pages**.
2. Under **Custom domain**, type `staratlasdaocouncil.com` and click **Save**.
3. Wait until the check turns green. This usually takes a few minutes and can take up to a day.
4. Tick **Enforce HTTPS** once the box becomes available.

That's all. The site notices its new address by itself the next time anything is saved.

---

## 4. Moving the site to the DAO's GitHub (admins)

Everything moves with the repository: pages, images, history and settings. Nothing in it mentions the old owner.

### Before you start

You need to be allowed to create repositories in the DAO's GitHub organization (an owner of the organization can do the transfer with you or grant you that right).

### The transfer

1. On GitHub, open the repository, then **Settings**. Scroll to the bottom, to the **Danger Zone**.
2. Click **Transfer**, choose the DAO organization as the new owner, and confirm.

### Checklist right after the transfer

1. **Publishing:** in the repository, open **Settings**, then **Pages**. Check that **Source** says **GitHub Actions**. If it does not, select it.
2. **Custom domain:** on the same page, check that **Custom domain** still says `staratlasdaocouncil.com`. If it is empty, type it in again and save, then tick **Enforce HTTPS**.
3. **Cloudflare:** change the `www` record's target from `jupus-soul.github.io` to `<dao-organization-name>.github.io`. The four **A** records stay as they are.
4. **Visual editor:** an owner of the DAO organization goes to https://app.pagescms.org, signs in with GitHub and installs the Pages CMS GitHub App on the organization, for this repository only (the same one-time setup as in part 2).
5. **Editors:** check the Collaborators list in Pages CMS and invite again anyone who is missing. People added on GitHub (Option B) need to be added again in the organization.
6. **Test:** make a small edit in the visual editor, save, and check that it appears on the site after a minute or two. If it does not, open the **Actions** tab on GitHub, click **Publish site**, then **Run workflow**.

Old links to the repository on GitHub keep redirecting to the new place.

---

## If something looks wrong

- **A change does not appear on the site:** wait two minutes and refresh. Then look at the **Actions** tab on GitHub. A red cross means the last publish failed. Click it to see which page caused the problem, usually a link to a page that was renamed or deleted.
