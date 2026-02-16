# Complete Workflow: From Literature Search to GitHub Pages

## 📋 Full Process Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: LITERATURE SEARCH                     │
│                                                                   │
│  Run: python3 genomic_llm_literature_agent.py                   │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   bioRxiv   │  │     PMC     │  │    arXiv    │            │
│  │   Search    │  │   Search    │  │   Search    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                 │                 │                    │
│         └─────────────────┴─────────────────┘                    │
│                           │                                      │
│                           ▼                                      │
│              ┌─────────────────────────┐                        │
│              │  Aggregate & Deduplicate │                        │
│              └─────────────────────────┘                        │
│                           │                                      │
│                           ▼                                      │
│              ┌─────────────────────────┐                        │
│              │  [Optional] AI Analysis  │                        │
│              │  with Claude API         │                        │
│              └─────────────────────────┘                        │
│                           │                                      │
│                           ▼                                      │
│              ┌─────────────────────────┐                        │
│              │  Identify Research Gaps  │                        │
│              └─────────────────────────┘                        │
│                           │                                      │
│                           ▼                                      │
│  OUTPUT: output_reports/literature_review.json                  │
│          output_reports/literature_review_summary.txt           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 STEP 2: CONVERT TO WEB PAGES                     │
│                                                                   │
│  Run: python3 convert_to_github_pages.py                        │
│                                                                   │
│              ┌─────────────────────────┐                        │
│              │  Read JSON Data         │                        │
│              └─────────────────────────┘                        │
│                     │           │                                │
│          ┌──────────┘           └──────────┐                    │
│          ▼                                  ▼                    │
│  ┌───────────────┐                  ┌───────────────┐          │
│  │   Generate    │                  │   Generate    │          │
│  │   Markdown    │                  │     HTML      │          │
│  │   (index.md)  │                  │  (index.html) │          │
│  └───────────────┘                  └───────────────┘          │
│          │                                  │                    │
│          │                                  │                    │
│  OUTPUT: github_pages/index.md                                  │
│          github_pages/index.html                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 3: PUBLISH TO WEB                         │
│                                                                   │
│  Method A: GitHub Pages                                          │
│  ┌─────────────────────────────────────────┐                   │
│  │ 1. Create GitHub repository             │                   │
│  │ 2. Upload files from github_pages/      │                   │
│  │ 3. Enable GitHub Pages in Settings      │                   │
│  │ 4. Access at: username.github.io/repo/  │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                   │
│  Method B: Local Preview                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │ Open index.html in browser              │                   │
│  │ or run: python3 -m http.server          │                   │
│  └─────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Complete Command Sequence

### Basic Workflow (No Claude):
```bash
# Step 1: Search literature
python3 genomic_llm_literature_agent.py

# Step 2: Convert to web pages
python3 convert_to_github_pages.py

# Step 3: Preview locally
cd github_pages
python3 -m http.server 8000
# Open browser to: http://localhost:8000
```

### Advanced Workflow (With Claude):
```bash
# Step 1: Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Step 2: Search with AI analysis
python3 genomic_llm_literature_agent.py
# (Edit script to set use_claude=True)

# Step 3: Convert to web pages
python3 convert_to_github_pages.py

# Step 4: Publish to GitHub
cd github_pages
git init
git add .
git commit -m "Initial literature review"
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

## 📁 Directory Structure After All Steps

```
your-project/
├── genomic_llm_literature_agent.py    # Main search agent
├── convert_to_github_pages.py         # Converter script
├── example_usage.py                   # Example scenarios
├── config.json                        # Configuration
├── requirements.txt                   # Dependencies
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── ARCHITECTURE.md                    # Technical docs
├── GITHUB_PAGES_GUIDE.md             # Publishing guide
│
├── output_reports/                    # Agent outputs
│   ├── literature_review.json         # ← Main data file
│   └── literature_review_summary.txt  # ← Human summary
│
└── github_pages/                      # Web outputs
    ├── index.html                     # ← Styled webpage
    └── index.md                       # ← Markdown page
```

## 🔄 Update Workflow

When you want to refresh your review:

```bash
# 1. Search for new publications
python3 genomic_llm_literature_agent.py

# 2. Regenerate web pages
python3 convert_to_github_pages.py

# 3. Update GitHub Pages
cd github_pages
git add .
git commit -m "Update literature review - $(date +%Y-%m-%d)"
git push
```

## 📊 Output Comparison

### JSON Output (Raw Data):
```json
{
  "metadata": {...},
  "publications": [...],
  "research_gaps": {...}
}
```
**Purpose:** Machine-readable, data processing

### Markdown Output:
```markdown
# Genomic LLM Literature Review

## Publications

### 2024
- Paper title...
```
**Purpose:** GitHub README, Jekyll themes, simple viewing

### HTML Output:
```html
<!DOCTYPE html>
<html>
  <head>
    <link href="bootstrap.css">
  </head>
  <body>
    <div class="publication-card">...</div>
  </body>
</html>
```
**Purpose:** Professional presentation, interactive features

## 🎨 Customization Points

### 1. Search Customization
**File:** `genomic_llm_literature_agent.py`
**Edit:**
- Line ~40: `target_models` list
- Line ~50: `cereal_crops` list
- Line ~190: `queries` list

### 2. Output Customization
**File:** `convert_to_github_pages.py`
**Edit:**
- Line ~300+: HTML styling (CSS)
- Line ~180+: Markdown structure
- Add custom sections as needed

### 3. Configuration
**File:** `config.json`
**Edit:**
- Data sources
- Search filters
- Rate limiting
- Output settings

## 🚀 Publishing Options

### Option 1: GitHub Pages (Free, Public)
✅ Free hosting
✅ Custom domain support
✅ Auto-deploy on push
❌ Repository must be public (for free tier)

### Option 2: GitHub Pages (Paid, Private)
✅ Private repository
✅ All GitHub Pages features
💰 Requires GitHub Pro/Team

### Option 3: Self-Hosted
✅ Full control
✅ Can be private
❌ Need own server
📝 Use `index.html` directly

### Option 4: Netlify/Vercel
✅ Free tier available
✅ Continuous deployment
✅ Custom domains
📝 Connect to GitHub repo

## 📈 Analytics & SEO

Add to `index.html` for tracking:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>

<!-- SEO Meta Tags -->
<meta name="description" content="Your description">
<meta property="og:title" content="Genomic LLM Review">
<meta property="og:image" content="preview.png">
```

## 🔗 Sharing Your Review

After publishing, share via:
- Direct link: `https://username.github.io/repo/`
- QR code (generate from URL)
- Social media with preview image
- Academic profile (ResearchGate, Academia.edu)
- Embed in lab website

## ✅ Quality Checklist

Before publishing:
- [ ] Run literature search successfully
- [ ] Review JSON output for completeness
- [ ] Convert to HTML/Markdown
- [ ] Preview locally in browser
- [ ] Check all links work
- [ ] Verify formatting is correct
- [ ] Test on mobile device
- [ ] Push to GitHub
- [ ] Verify GitHub Pages builds
- [ ] Share with colleagues for feedback

---

**End of Complete Workflow Guide**

You now have everything needed to:
1. ✅ Search genomic LLM literature
2. ✅ Analyze research gaps
3. ✅ Generate beautiful web pages
4. ✅ Publish to the world!
