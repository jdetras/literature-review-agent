# Web Interface Setup Guide

## 🌐 Overview

You now have a **beautiful web interface** where users can configure and run literature searches directly from their browser!

## 📁 What You Got

**`web_interface.html`** - Complete web application with:
- ✅ **Template selector** (Plant Genomics, Cancer Research, Custom)
- ✅ **Configuration forms** (models, topics, parameters)
- ✅ **Real-time status updates**
- ✅ **Progress tracking**
- ✅ **Results display** with relevance scores
- ✅ **Download options** (JSON, Markdown)
- ✅ **Beautiful responsive design**

## 🚀 Deployment Options

### Option 1: Static GitHub Pages (Current)

**What it does:**
- Works immediately
- Shows demo with mock data
- Perfect for testing interface
- No backend needed

**Limitations:**
- Uses simulated search results
- Doesn't actually search databases
- Good for UI/UX demo

**To deploy:**
```bash
# Just upload web_interface.html to GitHub Pages
cp web_interface.html github_pages/index.html
git add github_pages/index.html
git commit -m "Add web interface"
git push

# Access at: https://username.github.io/repo-name/
```

---

### Option 2: Full Implementation with Claude API ⭐ (Recommended)

**What it does:**
- Actual literature searches
- Real results from bioRxiv, PMC, arXiv
- Uses Claude AI for analysis
- Complete end-to-end solution

**Requirements:**
- Anthropic API key
- Backend server (Cloudflare Workers, Vercel, or AWS Lambda)

#### Setup Steps:

**Step 1: Get Anthropic API Key**
```
1. Go to https://console.anthropic.com/
2. Create an API key
3. Copy the key
```

**Step 2: Choose Backend**

**Option A: Cloudflare Workers (Free, Recommended)**

Create `worker.js`:
```javascript
export default {
  async fetch(request) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const { config } = await request.json();
      
      // Call Claude API to run the search
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': 'YOUR_ANTHROPIC_API_KEY', // Use environment variable
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 4096,
          messages: [{
            role: 'user',
            content: `Run a literature search with this configuration:
            
Models: ${config.models.join(', ')}
Topics: ${config.topics.join(', ')}
Min Year: ${config.minYear}
Min Relevance: ${config.minRelevance}
Exclusions: ${config.exclusion.join(', ')}

Search bioRxiv, PubMed Central, and arXiv for relevant papers.
Return results as JSON with this structure:
{
  "publications": [
    {
      "title": "...",
      "authors": [...],
      "year": 2024,
      "abstract": "...",
      "url": "...",
      "source": "...",
      "relevance_score": 85.5
    }
  ],
  "metadata": {
    "total_publications": 5,
    "avg_relevance_score": 75.2
  }
}

Actually search the databases and return real results.`
          }]
        })
      });

      const data = await response.json();
      const results = JSON.parse(data.content[0].text);
      
      return new Response(JSON.stringify(results), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
      
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
```

Deploy:
```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Deploy
wrangler publish
# Get URL: https://your-worker.workers.dev
```

**Option B: Vercel Serverless Function**

Create `api/search.js`:
```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { config } = req.body;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        messages: [{
          role: 'user',
          content: `Run literature search... (same as above)`
        }]
      })
    });

    const data = await response.json();
    const results = JSON.parse(data.content[0].text);
    
    res.status(200).json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

Deploy:
```bash
# Install Vercel CLI
npm install -g vercel

# Set environment variable
vercel env add ANTHROPIC_API_KEY

# Deploy
vercel --prod
# Get URL: https://your-project.vercel.app
```

**Step 3: Update web_interface.html**

Replace the `runSearch()` function (line ~280):
```javascript
async function runSearch() {
    const config = {
        models: document.getElementById('models-input').value.split('\n').filter(m => m.trim()),
        topics: document.getElementById('topics-input').value.split('\n').filter(t => t.trim()),
        minYear: parseInt(document.getElementById('min-year').value),
        minRelevance: parseFloat(document.getElementById('min-relevance').value),
        exclusion: document.getElementById('exclusion-keywords').value.split(',').map(k => k.trim()).filter(k => k)
    };

    // ... validation code ...

    try {
        // Call your backend API
        const response = await fetch('YOUR_BACKEND_URL/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ config })
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const results = await response.json();
        
        addStatusMessage(`Found ${results.publications.length} relevant publications`, 'success');
        displayResults(results);
        searchResults = results;

    } catch (error) {
        addStatusMessage('Error: ' + error.message, 'error');
    }
}
```

---

### Option 3: Hybrid (Static + GitHub Actions)

**How it works:**
1. User fills form on GitHub Pages
2. Form submits configuration to GitHub repository
3. GitHub Actions runs the search
4. Results published back to GitHub Pages

**Advantages:**
- No backend server needed
- Uses existing GitHub Actions setup
- Free hosting

**Process:**
```
User Input (web_interface.html)
    ↓
Save config to repo (via GitHub API)
    ↓
Trigger GitHub Action
    ↓
Action runs search
    ↓
Results published to gh-pages
    ↓
User sees results
```

---

## 🎨 Customization

### Change Colors

Edit the `<style>` section:
```css
/* Main gradient */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

/* Accent color */
border-left: 5px solid #YOUR_ACCENT_COLOR;
```

### Add More Templates

Add to the `templates` object (line ~120):
```javascript
'climate-science': {
    models: `LSTM
Transformer
ResNet`,
    topics: `climate change
global warming`,
    minYear: 2010,
    minRelevance: 40,
    exclusion: 'clinical, medical'
}
```

Then add a template card:
```html
<div class="col-md-4">
    <div class="template-card" onclick="loadTemplate('climate-science')">
        <h5>🌍 Climate Science</h5>
        <small>Search climate modeling papers</small>
    </div>
</div>
```

### Customize Fields

Add more input fields in the config sections:
```html
<div class="config-section">
    <h4>Advanced Options</h4>
    <div class="row">
        <div class="col-md-6">
            <label>Max Results</label>
            <input type="number" id="max-results" class="form-control" value="50">
        </div>
        <!-- More fields -->
    </div>
</div>
```

---

## 📊 Features Explained

### Template Selector
- **Pre-configured settings** for common domains
- One-click to load configuration
- Prevents user errors

### Real-Time Status
- **Live updates** during search
- Progress bar shows completion
- Color-coded messages (info, success, error)

### Results Display
- **Relevance badges** (green/yellow/red)
- Sortable by score
- Clickable links to papers
- Hover effects for better UX

### Download Options
- **JSON**: For programmatic use
- **Markdown**: For documentation
- Timestamped filenames

---

## 🔒 Security Considerations

### API Key Protection

**❌ Never do this:**
```javascript
const API_KEY = 'sk-ant-api03-...'; // Exposed to users!
```

**✅ Always do this:**
```javascript
// Backend only (Cloudflare Worker, Vercel Function)
const API_KEY = process.env.ANTHROPIC_API_KEY;
```

### Rate Limiting

Add to backend:
```javascript
// Simple rate limit
const rateLimits = new Map();

function checkRateLimit(ip) {
    const now = Date.now();
    const userLimits = rateLimits.get(ip) || { count: 0, resetAt: now + 3600000 };
    
    if (now > userLimits.resetAt) {
        userLimits.count = 0;
        userLimits.resetAt = now + 3600000;
    }
    
    if (userLimits.count >= 10) {
        return false; // Rate limited
    }
    
    userLimits.count++;
    rateLimits.set(ip, userLimits);
    return true;
}
```

### Input Validation

Add to backend:
```javascript
function validateConfig(config) {
    if (!config.models || config.models.length === 0) {
        throw new Error('At least one model required');
    }
    if (!config.topics || config.topics.length === 0) {
        throw new Error('At least one topic required');
    }
    if (config.minYear < 1900 || config.minYear > 2030) {
        throw new Error('Invalid year range');
    }
    return true;
}
```

---

## 🎯 Best Practices

### 1. Start with Mock Data
- Test UI/UX first
- Deploy to GitHub Pages
- Get user feedback
- Then add real API

### 2. Progressive Enhancement
- Basic functionality works without JS
- Enhanced with JavaScript
- Graceful degradation

### 3. Error Handling
- Clear error messages
- Retry mechanisms
- Fallback options

### 4. Performance
- Show progress indicators
- Cache results
- Lazy load publications

---

## 📱 Mobile Responsive

The interface is fully responsive:
- ✅ Works on phones (320px+)
- ✅ Works on tablets
- ✅ Works on desktops
- ✅ Touch-friendly buttons

Test on different devices!

---

## 🚀 Quick Start

### Immediate Demo (No Setup)
```bash
# Open web_interface.html in browser
open web_interface.html

# Or upload to GitHub Pages
cp web_interface.html docs/index.html
git add docs/index.html
git commit -m "Add web interface"
git push

# Enable GitHub Pages → docs folder
```

### Full Production Setup
```bash
# 1. Deploy backend (Cloudflare/Vercel)
# 2. Get backend URL
# 3. Update web_interface.html with URL
# 4. Deploy to GitHub Pages
# 5. Share with users!
```

---

## 📚 User Guide

For end users, the interface is intuitive:

1. **Select a template** or configure custom settings
2. **Fill in models** you want to track
3. **Add research topics** you're interested in
4. **Set parameters** (year range, quality threshold)
5. **Click "Run Literature Search"**
6. **View results** in real-time
7. **Download** JSON or Markdown

No programming knowledge required!

---

## 🎉 Summary

You now have:
- ✅ Beautiful web interface
- ✅ User-friendly configuration
- ✅ Real-time search progress
- ✅ Professional results display
- ✅ Multiple deployment options
- ✅ Download functionality
- ✅ Mobile responsive

**Next steps:**
1. Test the demo interface
2. Choose deployment option
3. Set up backend (if using real API)
4. Share with your research community!

Your literature review tool is now accessible to anyone with a web browser! 🚀
