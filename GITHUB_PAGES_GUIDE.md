# GitHub Pages Conversion Guide

## 🎯 Overview

This guide shows you how to convert your literature review JSON into beautiful HTML and Markdown pages for GitHub Pages.

## 🚀 Quick Start

### Step 1: Run the Literature Agent
```bash
python3 genomic_llm_literature_agent.py
```

This creates: `output_reports/literature_review.json`

### Step 2: Convert to GitHub Pages Format
```bash
python3 convert_to_github_pages.py
```

This creates in `github_pages/` folder:
- `index.html` - Beautiful styled HTML page
- `index.md` - Clean Markdown format

## 📁 Output Files

### index.html
- **Beautiful Bootstrap-styled page**
- Interactive navigation
- Color-coded badges for models and crops
- Responsive design (mobile-friendly)
- Hover effects and animations
- **Best for:** Professional presentation

### index.md
- **Clean Markdown format**
- Perfect for GitHub README
- Table of contents with anchors
- Compatible with Jekyll
- **Best for:** GitHub Pages with Jekyll theme

## 🌐 Publishing to GitHub Pages

### Option A: Using HTML (Recommended)

1. **Create a new repository on GitHub:**
   - Repository name: `genomic-llm-review` (or your choice)
   - Make it public
   - Don't initialize with README

2. **Upload your files:**
   ```bash
   cd github_pages
   git init
   git add index.html
   git commit -m "Add literature review"
   git branch -M main
   git remote add origin https://github.com/yourusername/genomic-llm-review.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `main` → `/ (root)`
   - Click Save

4. **View your page:**
   - URL: `https://yourusername.github.io/genomic-llm-review/`
   - Wait 1-2 minutes for deployment

### Option B: Using Markdown with Jekyll

1. **Create repository** (same as above)

2. **Upload files:**
   ```bash
   cd github_pages
   git init
   git add index.md
   git commit -m "Add literature review"
   git branch -M main
   git remote add origin https://github.com/yourusername/genomic-llm-review.git
   git push -u origin main
   ```

3. **Add Jekyll theme** (optional):
   
   Create `_config.yml`:
   ```yaml
   theme: jekyll-theme-cayman
   title: Genomic LLM Literature Review
   description: Research gaps for rice and cereal crops
   ```

4. **Enable GitHub Pages** (same as Option A)

## 🎨 Customization

### HTML Styling

Edit `index.html` to change:

**Colors:**
```css
/* In the <style> section */
.stat-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change to your preferred gradient */
}

.badge-model {
    background: #3498db; /* Blue for models */
}

.badge-crop {
    background: #27ae60; /* Green for crops */
}
```

**Fonts:**
```css
body {
    font-family: 'Your Preferred Font', sans-serif;
}
```

### Markdown Front Matter

Add to top of `index.md` for Jekyll:
```yaml
---
layout: default
title: Genomic LLM Literature Review
---
```

## 📊 What You Get

### HTML Page Features:
- ✅ **Statistics Dashboard** - Publications, gaps, models count
- ✅ **Table of Contents** - Quick navigation
- ✅ **Color-Coded Badges** - Models (blue) and crops (green)
- ✅ **Interactive Cards** - Hover effects on publications
- ✅ **Responsive Design** - Works on all devices
- ✅ **Professional Layout** - Bootstrap styling

### Markdown Features:
- ✅ **Clean Structure** - Headers and sections
- ✅ **Anchor Links** - Jump to any section
- ✅ **Lists and Tables** - Well-formatted data
- ✅ **GitHub Compatible** - Renders perfectly
- ✅ **Jekyll Ready** - Works with themes

## 🔧 Advanced Usage

### Custom Output Location
```bash
python3 convert_to_github_pages.py /path/to/your/review.json
```

### Multiple Reviews
```bash
# Convert different reviews
python3 convert_to_github_pages.py rice_only_review.json
python3 convert_to_github_pages.py wheat_review.json

# Rename outputs
mv github_pages/index.html github_pages/rice.html
mv github_pages/index.md github_pages/rice.md
```

### Add Custom Sections

Edit the converter script to add:

```python
# In generate_html() or generate_markdown()
html.append('<h2>Custom Analysis</h2>')
html.append('<p>Your custom content here</p>')
```

## 📱 Preview Locally

### HTML Preview:
```bash
# Open in browser
open github_pages/index.html
# or
python3 -m http.server 8000
# Then visit: http://localhost:8000/github_pages/
```

### Markdown Preview:
```bash
# Install grip (GitHub README preview)
pip install grip

# Preview
grip github_pages/index.md
# Then visit: http://localhost:6419
```

## 🐛 Troubleshooting

### "File not found" error
- Make sure you ran `genomic_llm_literature_agent.py` first
- Check that `output_reports/literature_review.json` exists

### GitHub Pages not showing
- Wait 2-3 minutes after pushing
- Check Settings → Pages for error messages
- Ensure repository is public
- Verify branch and folder are correct

### HTML looks unstyled
- Check internet connection (needs CDN for Bootstrap)
- View page source to ensure HTML is complete
- Try clearing browser cache

### Markdown not rendering
- Ensure file is named `index.md` or `README.md`
- Check for YAML front matter issues
- Verify Jekyll theme is compatible

## 💡 Tips

1. **Update Regularly:**
   - Re-run agent monthly
   - Convert and push updates
   - GitHub Pages auto-updates

2. **Add Analytics:**
   ```html
   <!-- Add before </head> -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
   ```

3. **SEO Optimization:**
   ```html
   <meta name="description" content="Comprehensive literature review of genomic LLMs">
   <meta name="keywords" content="genomic, LLM, rice, cereals, agriculture">
   ```

4. **Social Sharing:**
   ```html
   <meta property="og:title" content="Genomic LLM Literature Review">
   <meta property="og:description" content="Research gaps for rice and cereal crops">
   ```

## 🌟 Examples

### Example Repository Structure:
```
genomic-llm-review/
├── index.html          # Main page
├── index.md           # Markdown version
├── _config.yml        # Jekyll config (optional)
├── assets/            # Images/CSS (optional)
│   └── style.css
└── README.md          # Repository info
```

### Example URL:
`https://yourusername.github.io/genomic-llm-review/`

## 📚 Resources

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Jekyll Themes](https://jekyllthemes.io/)
- [Bootstrap Docs](https://getbootstrap.com/)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Happy Publishing! 🚀**

Your literature review will look professional and be easily shareable!
