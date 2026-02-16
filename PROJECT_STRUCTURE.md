# 📁 Project Structure

## Complete File Overview

```
literature-review-agent/
│
├── 🐍 Python Scripts (Main)
│   ├── generic_literature_agent.py          ⭐ RECOMMENDED - Fully configurable via text files
│   ├── genomic_llm_literature_agent_v2.py   📊 Advanced filtering & relevance scoring
│   ├── agentic_orchestrator.py              🤖 Self-improving autonomous agent
│   ├── convert_to_github_pages.py           📄 JSON → HTML/Markdown converter
│   └── example_usage.py                     📚 7 example scenarios
│
├── ⚙️ Configuration Files
│   ├── config_models.txt                    🎯 Target models (one per line)
│   ├── config_topics.txt                    📖 Research topics (one per line)
│   ├── config_search.txt                    🔧 Search parameters & filters
│   └── requirements.txt                     📦 Python dependencies
│
├── 🌐 Web Interface
│   └── web_interface.html                   💻 Browser-based configuration & search
│
├── 🤖 GitHub Actions
│   └── .github/workflows/
│       └── literature-review.yml            ⏰ Automated weekly searches
│
├── 📚 Documentation
│   ├── README.md                            📖 Main documentation
│   ├── QUICKSTART.md                        ⚡ 5-minute setup guide
│   ├── GENERIC_CONFIG_GUIDE.md              🎯 How to configure for any domain
│   ├── PARAMETER_GUIDE.md                   🔧 Adjust search parameters
│   ├── AUTOMATION_GUIDE.md                  🤖 GitHub Actions setup
│   ├── WEB_INTERFACE_GUIDE.md               🌐 Web deployment guide
│   ├── GITHUB_PAGES_GUIDE.md                📄 Publishing to web
│   ├── COMPLETE_WORKFLOW.md                 🔄 Full process overview
│   ├── ARCHITECTURE.md                      🏗️ Technical details
│   ├── AGENTIC_SYSTEM_SUMMARY.md            🧠 AI agent features
│   ├── VERSION_COMPARISON.md                📊 v1 vs v2 differences
│   ├── GENERIC_COMPARISON.md                🔄 Hardcoded vs configurable
│   └── DEMO_PREVIEW.md                      👀 Web interface preview
│
└── 📁 Examples
    └── cancer_research/                     🧬 Example: Cancer research config
        ├── config_models.txt
        └── config_topics.txt
```

## 🚀 Quick Start - Choose Your Path

### Path 1: Immediate Use (5 minutes) ⭐
**Best for:** First-time users, testing

```bash
# 1. Install dependencies
pip install requests beautifulsoup4 lxml --break-system-packages

# 2. Run with default plant genomics config
python3 generic_literature_agent.py

# 3. View results
cat output_reports/literature_review_summary.txt
```

### Path 2: Web Interface (2 minutes) 🌐
**Best for:** Non-technical users, sharing

```bash
# Just open in browser
open web_interface.html

# Or test locally
python3 -m http.server 8000
# Visit: http://localhost:8000/web_interface.html
```

### Path 3: Automation (30 minutes) 🤖
**Best for:** Regular updates, hands-off operation

```bash
# 1. Push to GitHub
# 2. Enable GitHub Actions
# 3. Set up GitHub Pages
# See: AUTOMATION_GUIDE.md
```

## 📖 Documentation Guide

### For New Users
1. **README.md** - Start here
2. **QUICKSTART.md** - Get running in 5 minutes
3. **GENERIC_CONFIG_GUIDE.md** - Customize for your domain

### For Configuration
1. **PARAMETER_GUIDE.md** - Adjust search filters
2. **GENERIC_CONFIG_GUIDE.md** - Domain-specific examples
3. **config_*.txt files** - Edit these directly

### For Web Interface
1. **WEB_INTERFACE_GUIDE.md** - Deploy web version
2. **DEMO_PREVIEW.md** - See what users will see
3. **web_interface.html** - The actual interface

### For Automation
1. **AUTOMATION_GUIDE.md** - GitHub Actions setup
2. **AGENTIC_SYSTEM_SUMMARY.md** - How AI agent works
3. **.github/workflows/literature-review.yml** - Workflow config

### For Technical Details
1. **ARCHITECTURE.md** - System design
2. **VERSION_COMPARISON.md** - Feature evolution
3. **COMPLETE_WORKFLOW.md** - End-to-end process

## 🎯 File Usage by Scenario

### Scenario 1: One-Time Search (Plant Genomics)
**Files needed:**
- `generic_literature_agent.py`
- `config_models.txt` (default)
- `config_topics.txt` (default)
- `config_search.txt` (default)
- `requirements.txt`

**Steps:**
```bash
pip install -r requirements.txt --break-system-packages
python3 generic_literature_agent.py
```

### Scenario 2: Different Domain (Cancer Research)
**Files needed:**
- `generic_literature_agent.py`
- `examples/cancer_research/config_models.txt`
- `examples/cancer_research/config_topics.txt`
- `config_search.txt` (edit parameters)

**Steps:**
```bash
cp examples/cancer_research/*.txt .
nano config_search.txt  # Adjust parameters
python3 generic_literature_agent.py
```

### Scenario 3: Share with Team (Web)
**Files needed:**
- `web_interface.html`

**Steps:**
```bash
# Upload to GitHub Pages
cp web_interface.html docs/index.html
git add docs/index.html
git commit -m "Add web interface"
git push
```

### Scenario 4: Automated Weekly Updates
**Files needed:**
- `generic_literature_agent.py`
- `convert_to_github_pages.py`
- `config_*.txt`
- `.github/workflows/literature-review.yml`
- All documentation

**Steps:**
```bash
# Push everything to GitHub
git add .
git commit -m "Setup automated literature review"
git push

# Enable GitHub Actions in Settings
# Enable GitHub Pages
```

## 🔧 Configuration Files Explained

### config_models.txt
```
# One model per line
AgroNT
DNABERT
PlantCAD
```
**Edit this to:** Track different AI models/methods

### config_topics.txt
```
# One topic per line
rice
wheat
Oryza sativa
```
**Edit this to:** Change research domain/subjects

### config_search.txt
```
min_year = 2018
min_relevance = 40.0
[required_keywords]
transformer
deep learning
```
**Edit this to:** Adjust filters and quality thresholds

## 📊 Output Files (Generated)

After running, you'll get:

```
output_reports/
├── literature_review.json              # Machine-readable results
└── literature_review_summary.txt       # Human-readable summary

github_pages/
├── index.html                          # Styled web page
└── index.md                            # Markdown version

agent_history.json                      # Learning history (if using orchestrator)
AGENT_PROGRESS.md                       # Progress tracking (if using orchestrator)
```

## 🎓 Learning Path

### Beginner (Day 1)
1. Read **QUICKSTART.md**
2. Run `generic_literature_agent.py` with defaults
3. Review output files
4. Open **web_interface.html** to see demo

### Intermediate (Day 2-3)
1. Read **GENERIC_CONFIG_GUIDE.md**
2. Edit `config_*.txt` for your domain
3. Run searches with custom configs
4. Try different parameter combinations

### Advanced (Week 1)
1. Read **AUTOMATION_GUIDE.md**
2. Set up GitHub Actions
3. Deploy web interface with backend
4. Configure agentic orchestrator

### Expert (Week 2+)
1. Read **ARCHITECTURE.md**
2. Customize Python scripts
3. Add new data sources
4. Build custom visualizations

## 💡 Tips

### Keep It Simple
- Start with defaults
- Make one change at a time
- Test before sharing

### Organization
- Use `examples/` for different domains
- Keep backups of working configs
- Document your changes

### Troubleshooting
- Check `PARAMETER_GUIDE.md` first
- Look at example configs
- Start with broader queries, then narrow

## 🚀 Next Steps

After unpacking:

1. **Read:** README.md
2. **Try:** QUICKSTART.md instructions
3. **Customize:** Edit config_*.txt files
4. **Share:** Deploy web_interface.html
5. **Automate:** Set up GitHub Actions

## 📞 Support

- **Issues?** Check troubleshooting in guides
- **Questions?** Review relevant documentation
- **Ideas?** Customize and extend!

---

**Everything you need is included. Ready to start!** 🎉
