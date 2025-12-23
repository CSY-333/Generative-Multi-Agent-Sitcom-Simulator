# Neon Society PRD Presentation

**Live Presentation:** [https://YOUR_USERNAME.github.io/YOUR_REPO/](https://YOUR_USERNAME.github.io/YOUR_REPO/)

## 🎨 Features

- **Marp Slide Deck**: Professional presentation of Project Requirements
- **Auto-Deploy**: Pushes to `main` automatically update GitHub Pages
- **Responsive**: Works on desktop and mobile

## 🚀 Deployment

### Automatic (GitHub Actions)

Every push to `main` that modifies `docs/PRD_presentation.md` triggers auto-deployment.

### Manual (Local)

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Convert to HTML
marp docs/PRD_presentation.md -o docs/index.html

# Commit and push
git add docs/index.html
git commit -m "Update presentation"
git push
```

## 📝 Editing

1. Edit `docs/PRD_presentation.md`
2. Preview: `marp -p docs/PRD_presentation.md`
3. Push to `main` → Auto-deploys!

## 🔧 GitHub Pages Setup

1. Go to **Settings** → **Pages**
2. Source: **GitHub Actions**
3. That's it! Workflow handles the rest.
