# 🌐 Web Interface Preview

## What Users Will See

### 1. Landing Page
```
╔══════════════════════════════════════════════════════════════╗
║                  📚 Literature Review Agent                  ║
║   Configure and run automated literature searches           ║
║         directly in your browser                             ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│                  Quick Start Templates                        │
├──────────────┬──────────────┬────────────────────────────────┤
│ 🌾 Plant     │ 🧬 Cancer    │ ⚙️ Custom                      │
│ Genomics     │ Research     │                                │
│              │              │                                │
│ Search       │ Search AI    │ Configure                      │
│ genomic LLMs │ models for   │ your own                       │
│ for rice,    │ cancer and   │ search                         │
│ wheat, and   │ immuno-      │ parameters                     │
│ cereals      │ therapy      │                                │
└──────────────┴──────────────┴────────────────────────────────┘
```

### 2. Configuration Section
```
┌──────────────────────────────────────────────────────────────┐
│ 🖥️  Target Models/Methods                                    │
│ Enter models or methods to track (one per line)              │
│                                                               │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ AgroNT                                                  │  │
│ │ DNABERT                                                 │  │
│ │ PlantCAD                                                │  │
│ │ Nucleotide Transformer                                  │  │
│ │ HyenaDNA                                                │  │
│ └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 📖  Research Topics                                           │
│ Enter your research topics (one per line)                    │
│                                                               │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ rice                                                    │  │
│ │ wheat                                                   │  │
│ │ maize                                                   │  │
│ │ Oryza sativa                                            │  │
│ └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🎚️  Search Parameters                                        │
│                                                               │
│ Minimum Year:        [2018  ▼]                               │
│ Min Relevance Score: [40    ▼]  (0-100)                      │
│                                                               │
│ Exclusion Keywords (optional):                               │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ sleep, clinical trial, patient                          │  │
│ └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

                    ╔════════════════════════╗
                    ║ 🔍 Run Literature      ║
                    ║    Search              ║
                    ╚════════════════════════╝
```

### 3. Progress & Status
```
┌──────────────────────────────────────────────────────────────┐
│ ████████████████████████████░░░░ 70%                         │
│                   Searching PubMed Central...                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Status Log:                                                   │
│                                                               │
│ ℹ️  Starting literature search...                            │
│ ℹ️  Configuration: 5 models, 4 topics                        │
│ ℹ️  Generating search queries...                             │
│ ℹ️  Searching bioRxiv...                                     │
│ ℹ️  Searching PubMed Central...                              │
│ ✅ Found 38 relevant publications                            │
│ ✅ Search complete! Results displayed below.                 │
└──────────────────────────────────────────────────────────────┘
```

### 4. Results Display
```
╔══════════════════════════════════════════════════════════════╗
║              📊 Search Results                               ║
╚══════════════════════════════════════════════════════════════╝

┌────────────┐  ┌────────────┐  ┌────────────┐
│     38     │  │    72.5    │  │    2024    │
│            │  │            │  │            │
│Publications│  │   Average  │  │Most Recent │
│   Found    │  │  Relevance │  │    Year    │
└────────────┘  └────────────┘  └────────────┘

───────────────────────────────────────────────────────────────

┌──────────────────────────────────────────────────────────────┐
│ [85.5] AgroNT: A Foundation Model for Agricultural          │
│        Genome Analysis                                        │
│                                                               │
│ Authors: Smith J, Chen L, Kumar R | Year: 2024 | bioRxiv    │
│                                                               │
│ We present AgroNT, a transformer-based foundation model      │
│ specifically designed for agricultural genome analysis...     │
│                                                               │
│ [🔗 View Paper]                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ [78.3] Deep Learning Approaches for Rice Genome              │
│        Annotation Using DNABERT                               │
│                                                               │
│ Authors: Wang X, Lee S, Park M | Year: 2023 | PMC           │
│                                                               │
│ This study applies DNABERT architecture to rice genome       │
│ annotation tasks, achieving state-of-the-art results...      │
│                                                               │
│ [🔗 View Paper]                                              │
└──────────────────────────────────────────────────────────────┘

... (more results) ...

              [📥 Download JSON]  [📄 Download Markdown]
```

## 🎨 Visual Features

### Color-Coded Relevance Badges
- **Green (70-100)**: High relevance - matches perfectly
- **Yellow (50-69)**: Medium relevance - good match
- **Red (0-49)**: Low relevance - tangential

### Hover Effects
- Cards lift and shift on hover
- Buttons change color and shadow
- Smooth transitions everywhere

### Responsive Design
- **Desktop**: Full layout with side-by-side stats
- **Tablet**: Stacked stats, readable cards
- **Mobile**: Single column, touch-friendly buttons

### Real-Time Feedback
- Progress bar animates
- Status messages appear instantly
- Results fade in smoothly

## 🖱️ User Interaction Flow

```
1. User lands on page
   ↓
2. Clicks template (e.g., "Plant Genomics")
   ↓
3. Form auto-fills with template config
   ↓
4. User reviews/edits configuration
   ↓
5. Clicks "Run Literature Search"
   ↓
6. Progress bar shows 0% → 100%
   ↓
7. Status messages stream in real-time:
   "Searching bioRxiv..."
   "Found 15 papers..."
   "Searching PMC..."
   ↓
8. Results appear below with:
   - Statistics boxes
   - Sorted publication cards
   - Clickable links
   ↓
9. User can:
   - Read abstracts
   - Click to view full papers
   - Download JSON/Markdown
   - Run new search with different config
```

## 📱 Mobile Experience

```
┌─────────────────┐
│ 📚 Literature   │
│ Review Agent    │
├─────────────────┤
│                 │
│ Quick Templates │
│                 │
│ ┌─────────────┐ │
│ │🌾 Plant     │ │
│ │  Genomics   │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │🧬 Cancer    │ │
│ │  Research   │ │
│ └─────────────┘ │
│                 │
│ Models:         │
│ ┌─────────────┐ │
│ │ AgroNT      │ │
│ │ DNABERT     │ │
│ └─────────────┘ │
│                 │
│ Topics:         │
│ ┌─────────────┐ │
│ │ rice        │ │
│ │ wheat       │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │🔍 Run Search│ │
│ └─────────────┘ │
│                 │
│ Results:        │
│ ┌─────────────┐ │
│ │[85.5] Paper │ │
│ │Title Here   │ │
│ └─────────────┘ │
└─────────────────┘
```

## 🎯 Key Benefits

### For Researchers
- ✅ No installation required
- ✅ Works on any device
- ✅ Save/share configurations
- ✅ Instant results
- ✅ Export to any format

### For Lab Groups
- ✅ Share via URL
- ✅ Multiple people can use simultaneously
- ✅ Consistent interface
- ✅ No training needed

### For Institutions
- ✅ Host on GitHub Pages (free)
- ✅ Customize branding
- ✅ Track usage (via analytics)
- ✅ Easy to update

## 🚀 Deployment Preview

### Local Testing
```bash
# Just open in browser
open web_interface.html

# Or use Python server
python3 -m http.server 8000
# Visit: http://localhost:8000/web_interface.html
```

### GitHub Pages
```bash
# Copy to docs folder
cp web_interface.html docs/index.html

# Commit and push
git add docs/index.html
git commit -m "Add web interface"
git push

# Enable GitHub Pages in settings
# → Settings → Pages → Source: docs folder

# Access at: https://username.github.io/repo-name/
```

### Custom Domain
```
# Add CNAME file
echo "literature.yourlab.edu" > docs/CNAME

# Configure DNS:
# CNAME record: literature → username.github.io

# Access at: https://literature.yourlab.edu
```

## 🎉 Try It Now!

1. **Download** `web_interface.html`
2. **Open** in any web browser
3. **Click** "Plant Genomics" template
4. **Click** "Run Literature Search"
5. **See** results appear in real-time!

The interface works immediately with demo data. For production use with real searches, follow the setup guide to add backend API.

---

**Your literature review tool is now a beautiful, user-friendly web application!** 🎨✨
