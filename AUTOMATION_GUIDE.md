# GitHub Automation Setup Guide

## 🤖 Make Your Literature Review Fully Autonomous

This guide shows you how to set up **automatic weekly updates** that run without any manual intervention.

---

## 🎯 What You'll Get

### Automated Features:
- ✅ **Weekly automatic searches** (every Monday at 9 AM)
- ✅ **Auto-commit results** to your repository
- ✅ **Auto-update GitHub Pages** (always current)
- ✅ **Self-improving agent** (learns from each run)
- ✅ **Email notifications** (if search fails)
- ✅ **Manual triggers** (run anytime you want)
- ✅ **Progress tracking** (see improvements over time)

### Agentic Capabilities:
- 🧠 **Analyzes previous results** and adapts strategy
- 🧠 **Identifies coverage gaps** (models/crops)
- 🧠 **Generates targeted queries** to fill gaps
- 🧠 **Adjusts parameters** based on result quality
- 🧠 **Learns over time** (gets better with each run)

---

## 📋 Setup Steps

### Step 1: Prepare Your Repository

Create a new GitHub repository:

```bash
# On your local machine
mkdir genomic-llm-auto-review
cd genomic-llm-auto-review

# Initialize git
git init
git branch -M main
```

### Step 2: Add Files

Copy these files to your repository:

```
genomic-llm-auto-review/
├── .github/
│   └── workflows/
│       └── literature-review.yml          # ← GitHub Actions workflow
├── genomic_llm_literature_agent_v2.py     # ← Search agent
├── convert_to_github_pages.py             # ← Web converter
├── agentic_orchestrator.py                # ← Autonomous orchestrator
├── requirements.txt                       # ← Dependencies
├── config.json                            # ← Configuration
└── README.md                              # ← Documentation
```

### Step 3: Create GitHub Repository

```bash
# Create repository on GitHub (via web interface)
# Then link it:

git remote add origin https://github.com/YOUR_USERNAME/genomic-llm-auto-review.git
git add .
git commit -m "Initial setup for automated literature review"
git push -u origin main
```

### Step 4: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions":
   - ✅ Select **Read and write permissions**
   - ✅ Check **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### Step 5: (Optional) Add Anthropic API Key

For AI-powered analysis:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: `your-api-key-here`
5. Click **Add secret**

### Step 6: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → `github_pages/` folder
4. Click **Save**

Your page will be at: `https://YOUR_USERNAME.github.io/genomic-llm-auto-review/`

---

## ⚙️ Configuration

### Automated Schedule

Edit `.github/workflows/literature-review.yml` (line 5):

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  
# Other options:
# - cron: '0 9 * * *'     # Every day at 9 AM
# - cron: '0 9 1 * *'     # First day of every month
# - cron: '0 9 */2 * *'   # Every 2 days at 9 AM
# - cron: '0 9 * * 1,4'   # Monday and Thursday
```

### Search Parameters

Edit `config.json`:

```json
{
  "min_year": 2018,
  "min_relevance": 40.0,
  "max_results_per_query": 10,
  "adaptive_mode": true,
  "auto_refine_queries": true,
  "learning_rate": 0.1,
  "target_publications_per_run": 30
}
```

**Parameter Meanings:**
- `min_year`: Only papers from this year onwards
- `min_relevance`: Minimum quality score (0-100)
- `max_results_per_query`: How many results per search
- `adaptive_mode`: Let agent adjust parameters automatically
- `auto_refine_queries`: Generate smart queries based on gaps
- `learning_rate`: How aggressively to adapt (0.1 = cautious, 0.5 = aggressive)
- `target_publications_per_run`: Aim for this many papers

---

## 🚀 Usage

### Automatic Runs

**No action needed!** The workflow runs automatically every Monday.

You'll receive an email if it fails.

### Manual Runs

1. Go to **Actions** tab on GitHub
2. Click **Automated Literature Review** workflow
3. Click **Run workflow**
4. (Optional) Adjust parameters:
   - Minimum relevance score
   - Minimum year
5. Click **Run workflow**

### Check Results

After each run:
- View **Actions** tab to see progress
- Check `LATEST_UPDATE.md` for summary
- Check `AGENT_PROGRESS.md` for learning progress
- Visit your GitHub Pages site for full review

---

## 🧠 How the Agentic System Works

### Run Cycle:

```
1. ANALYZE PREVIOUS RESULTS
   ├─→ Were results good quality?
   ├─→ Were there enough results?
   └─→ What gaps exist?
   
2. ADJUST STRATEGY
   ├─→ If low quality → Increase strictness
   ├─→ If too few results → Expand search
   └─→ If optimal → Maintain current strategy
   
3. IDENTIFY GAPS
   ├─→ Which models have <3 papers?
   ├─→ Which crops have <5 papers?
   └─→ Generate targeted queries for gaps
   
4. EXECUTE SEARCH
   ├─→ Use adaptive queries
   ├─→ Apply current parameters
   └─→ Filter and rank results
   
5. LEARN & RECORD
   ├─→ Save run metrics
   ├─→ Compare to previous runs
   └─→ Prepare for next iteration
```

### Example Adaptation:

**Week 1:**
- Config: `min_relevance=40, max_results=10`
- Result: 15 publications, avg quality 38
- Analysis: Low quality
- **Action:** Increase `min_relevance` to 45

**Week 2:**
- Config: `min_relevance=45, max_results=10`
- Result: 35 publications, avg quality 52
- Analysis: Good balance
- **Action:** Maintain strategy

**Week 3:**
- Config: `min_relevance=45, max_results=10`
- Result: 8 publications, avg quality 68
- Analysis: Too few results
- **Action:** Decrease `min_relevance` to 42, increase `max_results` to 12

---

## 📊 Monitoring Progress

### View Run History

Check `AGENT_PROGRESS.md` after each run:

```markdown
# Autonomous Literature Review Progress

## Run History

| Run | Date | Publications | Avg Quality | Strategy |
|-----|------|--------------|-------------|----------|
| 1 | 2024-01-08 | 25 | 42.3 | Default |
| 2 | 2024-01-15 | 32 | 48.7 | Maintain |
| 3 | 2024-01-22 | 38 | 51.2 | Expand |

## Trends
- 📈 Publication count **increasing**
- 📈 Quality score **improving**
```

### GitHub Actions Dashboard

1. Go to **Actions** tab
2. Click on any workflow run
3. Expand steps to see detailed logs:
   - `📊 Analyzing Previous Results`
   - `⚙️ Adjusting Search Parameters`
   - `🔍 Identifying Coverage Gaps`
   - `🎯 Generating Adaptive Queries`
   - `🔎 Executing Literature Search`

---

## 🎛️ Advanced Configuration

### Customize Workflow Triggers

Edit `.github/workflows/literature-review.yml`:

```yaml
on:
  # Automatic schedule
  schedule:
    - cron: '0 9 * * 1'
  
  # Manual trigger with custom inputs
  workflow_dispatch:
    inputs:
      min_relevance:
        description: 'Min relevance score'
        default: '40'
      min_year:
        description: 'Min publication year'
        default: '2018'
      focus_crop:
        description: 'Focus on specific crop (optional)'
        default: ''
      focus_model:
        description: 'Focus on specific model (optional)'
        default: ''
  
  # Run on config changes
  push:
    paths:
      - 'config.json'
      - 'genomic_llm_literature_agent_v2.py'
```

### Email Notifications

GitHub automatically sends emails on workflow failures.

For custom notifications, add to workflow:

```yaml
    - name: Send success notification
      if: success()
      uses: dawidd6/action-send-mail@v3
      with:
        server_address: smtp.gmail.com
        server_port: 465
        username: ${{ secrets.EMAIL_USERNAME }}
        password: ${{ secrets.EMAIL_PASSWORD }}
        subject: "✅ Literature Review Updated"
        body: "New publications found! Check GitHub Pages."
        to: your.email@example.com
```

### Slack Notifications

```yaml
    - name: Notify Slack
      if: success()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "📚 Literature review updated with new publications!"
          }
```

---

## 🔧 Troubleshooting

### Workflow Fails

**Check:**
1. Logs in Actions tab
2. Permissions (should be read/write)
3. Secrets (if using Anthropic API)
4. Dependencies (all packages installed?)

**Common Issues:**
- `Permission denied` → Check workflow permissions
- `Module not found` → Check requirements.txt
- `API rate limit` → Add delays between requests

### No New Publications

**Possible Causes:**
1. Too strict parameters → Lower `min_relevance`
2. No new papers published → Normal, try next week
3. Queries too specific → Check `AGENT_PROGRESS.md` for suggested queries

### Agent Not Adapting

**Check:**
1. `adaptive_mode: true` in config.json
2. `agent_history.json` is being created
3. Sufficient run history (needs 2+ runs to adapt)

---

## 💡 Best Practices

### 1. Start Conservative
- Run manually first to test
- Review first few automated runs
- Adjust schedule based on publication frequency

### 2. Monitor Quality
- Check `AGENT_PROGRESS.md` weekly
- Review `LATEST_UPDATE.md` summaries
- Verify GitHub Pages updates correctly

### 3. Let It Learn
- Don't manually adjust config too often
- Give agent 3-4 runs to stabilize
- Only intervene if consistently poor results

### 4. Backup Data
- Agent automatically saves history
- Consider backing up `output_reports/` folder
- Git history tracks all changes

### 5. Customize Gradually
- Start with defaults
- Make one change at a time
- Document what works in README

---

## 📈 Expected Results

### Week 1-2: Initial Phase
- Agent explores different strategies
- Results may vary as it learns
- Normal to see some failed experiments

### Week 3-5: Stabilization
- Agent finds optimal parameters
- Consistent result quality
- Fewer drastic changes

### Week 6+: Maintenance
- Minor adjustments only
- Fills specific gaps
- Maintains quality

---

## 🎯 Success Metrics

Your automation is working well if:
- ✅ Runs complete successfully every week
- ✅ 25-40 publications per run
- ✅ Average quality score 45-60
- ✅ GitHub Pages updates automatically
- ✅ Coverage gaps decrease over time
- ✅ No manual intervention needed

---

## 🚀 Quick Start Checklist

- [ ] Create GitHub repository
- [ ] Add all files
- [ ] Enable GitHub Actions (read/write)
- [ ] (Optional) Add Anthropic API key
- [ ] Enable GitHub Pages
- [ ] Push to main branch
- [ ] Verify first automated run works
- [ ] Check GitHub Pages is accessible
- [ ] Review AGENT_PROGRESS.md
- [ ] Set up notifications (optional)

---

## 📚 Additional Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Cron Schedule Examples](https://crontab.guru/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)

---

**Your literature review is now fully autonomous!** 🎉

Set it up once, and it runs forever, getting smarter over time.
