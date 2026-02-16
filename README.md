# Genomic LLM Literature Review Agent

An AI-powered workflow for automatically scraping and analyzing open-access publications on genomic language models (LLMs) like AgroNT, PlantCAD, AlphaGenome, and others. The agent identifies research gaps applicable to rice and cereal crops.

## 🎯 Purpose

This agent helps researchers:
- **Automate literature discovery** across multiple open-access databases
- **Extract structured information** from genomic LLM papers
- **Identify research gaps** in rice and cereal crop genomics
- **Generate comprehensive reports** for literature reviews

## 🤖 Target Models

The agent searches for publications related to:
- **AgroNT** - Agricultural Nucleotide Transformer
- **PlantCAD** - Plant Crop Analysis and Design
- **AlphaGenome** - DeepMind's genomic prediction model
- **DNABERT** - DNA sequence language model
- **Nucleotide Transformer** - General-purpose genomic LLM
- **HyenaDNA** - Long-context genomic model
- **Caduceus** - Bidirectional genomic model
- **GenSLM** - Genomic Sequence Language Model
- **GENA-LM** - Gene Analysis Language Model
- **Enformer** - Gene expression prediction transformer

## 🌾 Focus Crops

Special attention to:
- Rice (primary focus)
- Wheat
- Maize/Corn
- Barley
- Sorghum
- Millet
- Oats
- Rye

## 📚 Data Sources

The agent searches across:
1. **bioRxiv** - Preprint server for biology
2. **PubMed Central (PMC)** - Open-access repository
3. **arXiv** - Preprint archive for quantitative biology
4. **PLOS** - Open-access journals (extensible)

## 🚀 Installation

### Prerequisites

```bash
# Python 3.8 or higher required
python3 --version
```

### Install Dependencies

```bash
# Install required Python packages
pip install requests beautifulsoup4 anthropic biopython lxml --break-system-packages

# Or using requirements.txt (see below)
pip install -r requirements.txt --break-system-packages
```

### Optional: Enable AI Analysis

To use Claude for advanced publication analysis:

1. Get an Anthropic API key from https://console.anthropic.com/
2. Set it in the code or as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## 📖 Usage

### Basic Usage

```bash
# Run the literature review agent
python3 genomic_llm_literature_agent.py
```

### Advanced Usage with Claude Analysis

```python
from genomic_llm_literature_agent import GenomicLLMAgent

# Initialize with Claude API key
agent = GenomicLLMAgent(anthropic_api_key="your-key-here")

# Run comprehensive search with AI analysis
publications = agent.run_literature_search(use_claude=True)

# Generate report
report = agent.generate_literature_review_report()
```

### Custom Search Queries

```python
# Search specific model
pubs = agent.search_biorxiv("AgroNT rice genome", max_results=20)

# Search PMC for plant genomics
pubs = agent.search_pubmed_central("plant genomic transformer", max_results=30)

# Search arXiv for ML papers
pubs = agent.search_arxiv("foundation model crop genomics", max_results=15)
```

## 📊 Output Files

The agent generates two main outputs:

### 1. `literature_review.json`
Comprehensive JSON report containing:
```json
{
  "metadata": {
    "generated_date": "2026-02-16T...",
    "total_publications": 45,
    "target_models": [...],
    "focus_crops": [...]
  },
  "publications": [
    {
      "title": "...",
      "authors": [...],
      "year": 2024,
      "abstract": "...",
      "url": "...",
      "model_name": "AgroNT",
      "crop_focus": ["rice", "wheat"],
      "key_findings": [...],
      "datasets_used": [...],
      "limitations": [...]
    }
  ],
  "research_gaps": {
    "understudied_crops": [...],
    "missing_applications": [...],
    "dataset_gaps": [...],
    "methodological_gaps": [...],
    "rice_specific_gaps": [...]
  },
  "recommendations": [...]
}
```

### 2. `literature_review_summary.txt`
Human-readable summary with:
- Publication statistics
- Target models coverage
- Identified research gaps by category
- Actionable recommendations

## 🎯 Research Gap Analysis

The agent identifies gaps in 5 categories:

### 1. Understudied Crops
Cereal crops with limited genomic LLM research coverage

### 2. Missing Applications
Potential use cases not yet explored:
- Trait prediction for yield under climate stress
- Pan-genome analysis for cereals
- Integration with breeding pipelines
- Transfer learning strategies

### 3. Dataset Gaps
Missing data resources:
- Comprehensive rice genome variation datasets
- Multi-omics integration
- Phenotype-genotype associations

### 4. Methodological Gaps
Technical challenges:
- Fine-tuning strategies for crops
- Model interpretability
- Computational efficiency

### 5. Rice-Specific Gaps
Opportunities for rice genomics research

## 🔧 Customization

### Add New Target Models

```python
agent.target_models.append("YourNewModel")
```

### Add New Crops

```python
agent.cereal_crops.append("quinoa")
```

### Add New Data Sources

```python
def search_custom_source(self, query: str) -> List[Publication]:
    # Implement your search logic
    pass

agent.search_custom_source = search_custom_source
```

### Customize Search Queries

Edit the `queries` list in `run_literature_search()`:

```python
queries = [
    "your custom query 1",
    "your custom query 2",
    # ...
]
```

## 🧠 AI Analysis Features (with Claude)

When Claude API is enabled, the agent can:

1. **Extract Model Information** - Identify which genomic LLMs are discussed
2. **Categorize Crops** - Determine crop species focus
3. **Summarize Findings** - Extract 3-5 key discoveries
4. **Parse Methodology** - Understand experimental approaches
5. **List Datasets** - Identify data resources used
6. **Identify Limitations** - Extract stated gaps and challenges

## ⚠️ Rate Limiting & Ethics

The agent implements:
- **Respectful delays** between requests (1-2 seconds)
- **Proper User-Agent** identification
- **API limits** compliance
- **Open-access only** - respects copyright

### Recommendations:
- Run during off-peak hours
- Don't abuse public APIs
- Cache results to avoid duplicate requests
- Respect robots.txt files

## 🔬 Example Workflow

```bash
# 1. Run initial search
python3 genomic_llm_literature_agent.py

# 2. Review outputs
cat /mnt/user-data/outputs/literature_review_summary.txt

# 3. Analyze specific publications
python3 -c "
import json
with open('/mnt/user-data/outputs/literature_review.json') as f:
    data = json.load(f)
    rice_pubs = [p for p in data['publications'] if 'rice' in str(p['crop_focus']).lower()]
    print(f'Rice-focused publications: {len(rice_pubs)}')
"

# 4. Use gaps to guide research
# Review research_gaps section in JSON output
```

## 📈 Extending the Agent

### Add Custom Analysis

```python
def analyze_citations(self, publication: Publication) -> int:
    """Count citations for a publication"""
    # Implement citation counting
    return citation_count

agent.analyze_citations = analyze_citations
```

### Export to Different Formats

```python
def export_to_csv(self):
    """Export publications to CSV"""
    import csv
    with open('publications.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'year', 'model_name'])
        writer.writeheader()
        for pub in self.publications:
            writer.writerow(asdict(pub))
```

### Add Visualization

```python
import matplotlib.pyplot as plt

def visualize_gaps(gaps):
    """Create bar chart of research gaps"""
    categories = list(gaps.keys())
    counts = [len(gaps[cat]) for cat in categories]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts)
    plt.title('Research Gaps in Genomic LLMs for Cereals')
    plt.xlabel('Gap Category')
    plt.ylabel('Number of Gaps')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('research_gaps.png')
```

## 🐛 Troubleshooting

### Connection Errors
- Check internet connectivity
- Verify API endpoints are accessible
- Use VPN if institutional firewall blocks access

### No Results Found
- Try broader search queries
- Check if target models have alternate names
- Verify publication date ranges

### Claude API Issues
- Confirm API key is valid
- Check rate limits
- Verify account has credits

### Parsing Errors
- Some papers may have unusual formatting
- Agent logs warnings but continues
- Check logs for specific error messages

## 📚 References

### Key Papers on Genomic LLMs:
1. **Nucleotide Transformer**: Dalla-Torre et al. (2023)
2. **DNABERT**: Ji et al. (2021)
3. **HyenaDNA**: Nguyen et al. (2023)
4. **Enformer**: Avsec et al. (2021)

### Rice Genomics Resources:
- [Rice Genome Annotation Project](http://rice.plantbiology.msu.edu/)
- [Gramene](https://www.gramene.org/)
- [International Rice Research Institute](https://www.irri.org/)

## 🤝 Contributing

To improve this agent:
1. Add new data sources
2. Enhance parsing logic
3. Improve gap analysis algorithms
4. Add visualization features
5. Create specialized analyses

## 📄 License

This is a research tool intended for academic use. Please respect:
- API terms of service
- Copyright and open access licenses
- Ethical web scraping practices

## 🙏 Acknowledgments

This agent helps researchers efficiently navigate the rapidly growing field of genomic AI to advance cereal crop improvement and food security.

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review error logs
3. Verify API credentials
4. Test with smaller queries first

---

**Happy Research! 🌾🤖**
