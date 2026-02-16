# Quick Start Guide
## Genomic LLM Literature Review Agent

### ⚡ 5-Minute Setup

#### Step 1: Install Dependencies
```bash
pip install requests beautifulsoup4 lxml --break-system-packages
```

#### Step 2: Run the Agent
```bash
python3 genomic_llm_literature_agent.py
```

That's it! The agent will:
- Search bioRxiv, PubMed Central, and arXiv
- Find papers on genomic LLMs
- Identify research gaps for rice/cereals
- Generate two reports in `/mnt/user-data/outputs/`

---

## 📋 What You Get

### Output Files

**1. literature_review.json**
- Complete publication database
- Structured data for each paper
- Research gap analysis
- Actionable recommendations

**2. literature_review_summary.txt**
- Human-readable overview
- Gap categories with details
- Quick reference guide

---

## 🎯 Common Use Cases

### Use Case 1: Find All Papers on a Specific Model
```python
from genomic_llm_literature_agent import GenomicLLMAgent

agent = GenomicLLMAgent()
pubs = agent.search_biorxiv("AgroNT", max_results=30)
pubs.extend(agent.search_pubmed_central("AgroNT", max_results=30))

print(f"Found {len(pubs)} papers on AgroNT")
```

### Use Case 2: Focus on Rice Only
```python
agent = GenomicLLMAgent()
agent.cereal_crops = ["rice", "Oryza sativa"]
publications = agent.run_literature_search()
agent.generate_literature_review_report(output_file="rice_only.json")
```

### Use Case 3: Analyze Existing Results
```python
import json

with open('/mnt/user-data/outputs/literature_review.json') as f:
    data = json.load(f)

# Count publications by year
years = {}
for pub in data['publications']:
    year = pub['year']
    years[year] = years.get(year, 0) + 1

print("Publications by year:", years)
```

---

## 🔧 Customization

### Change Target Models
Edit `genomic_llm_literature_agent.py`, line ~40:
```python
self.target_models = [
    "AgroNT", "YourNewModel", "AnotherModel"
]
```

### Change Search Queries
Edit line ~190:
```python
queries = [
    "your custom query",
    "another query"
]
```

### Add More Crops
Edit line ~50:
```python
self.cereal_crops = [
    "rice", "quinoa", "amaranth"
]
```

---

## 🚀 Advanced: Using Claude AI

### Enable AI Analysis

**Option 1: Environment Variable**
```bash
export ANTHROPIC_API_KEY='your-key-here'
python3 genomic_llm_literature_agent.py
```

**Option 2: In Code**
```python
agent = GenomicLLMAgent(anthropic_api_key="your-key-here")
publications = agent.run_literature_search(use_claude=True)
```

### What Claude Does
- Extracts model names automatically
- Identifies crop species mentioned
- Summarizes key findings
- Lists datasets used
- Notes limitations

---

## 📊 Example Output Structure

```json
{
  "metadata": {
    "total_publications": 42
  },
  "publications": [
    {
      "title": "AgroNT: Transformer for Agricultural Genomics",
      "year": 2024,
      "url": "https://...",
      "model_name": "AgroNT",
      "crop_focus": ["rice", "wheat"],
      "key_findings": [
        "Achieved 95% accuracy in gene prediction",
        "Outperformed DNABERT on plant genomes"
      ]
    }
  ],
  "research_gaps": {
    "understudied_crops": ["millet", "sorghum"],
    "missing_applications": [
      "Climate stress prediction",
      "Breeding pipeline integration"
    ]
  }
}
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install requests beautifulsoup4 --break-system-packages
```

### "Connection timeout"
- Check internet connection
- Try again later (servers may be busy)
- Reduce `max_results` in search calls

### "No results found"
- Queries may be too specific
- Try broader terms like "genomic transformer"
- Check if target models have alternate names

### "Rate limit exceeded"
- Agent has built-in delays
- If still hitting limits, increase delays in code
- Run during off-peak hours

---

## 📈 Workflow Diagram

```
START
  │
  ├─→ Initialize Agent
  │     └─→ Load target models & crops
  │
  ├─→ Search Literature
  │     ├─→ bioRxiv
  │     ├─→ PubMed Central  
  │     └─→ arXiv
  │
  ├─→ [Optional] Analyze with Claude
  │     └─→ Extract structured info
  │
  ├─→ Identify Research Gaps
  │     ├─→ Count crop coverage
  │     ├─→ Analyze model distribution
  │     └─→ Detect missing areas
  │
  └─→ Generate Reports
        ├─→ JSON (machine-readable)
        └─→ TXT (human-readable)
```

---

## 💡 Pro Tips

1. **Start Broad**: Use general queries first, then narrow down
2. **Cache Results**: Save intermediate results to avoid re-scraping
3. **Batch Process**: Group related queries together
4. **Monitor Progress**: Watch console output for errors
5. **Validate Manually**: Spot-check a few papers to ensure quality

---

## 🎓 Next Steps

1. ✅ Run basic search
2. ✅ Review generated reports
3. ✅ Identify top 3 research gaps
4. ✅ Read key papers from results
5. ✅ Customize for your specific needs

---

## 📚 Learning Resources

### Understanding Genomic LLMs
- [Nucleotide Transformer Paper](https://www.biorxiv.org/content/...)
- [DNABERT Documentation](https://github.com/...)
- [HyenaDNA Blog Post](https://hazyresearch.stanford.edu/...)

### Rice Genomics
- [Rice Genome Project](http://rice.plantbiology.msu.edu/)
- [IRRI Database](https://www.irri.org/)
- [Gramene Resource](https://www.gramene.org/)

---

## ❓ FAQ

**Q: How long does a search take?**
A: 5-15 minutes for basic search (without Claude), 20-40 minutes with AI analysis

**Q: Can I search non-cereal crops?**
A: Yes! Just modify the `cereal_crops` list

**Q: Is this ethical?**
A: Yes - uses only open-access sources with respectful rate limiting

**Q: Can I use this for commercial purposes?**
A: Check individual paper licenses; agent is for research use

**Q: What if I find errors in the data?**
A: Web scraping can be imperfect - always validate important findings

---

**Ready to discover research gaps? Run the agent now!** 🚀

```bash
python3 genomic_llm_literature_agent.py
```
