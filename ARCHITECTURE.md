# AI Agent Workflow Architecture
## Genomic LLM Literature Review System

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ CLI Script   │  │ Python API   │  │ Config File  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT CORE LAYER                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │            GenomicLLMAgent (Main Controller)              │ │
│  │  • Query Planning                                         │ │
│  │  • Source Selection                                       │ │
│  │  • Result Aggregation                                     │ │
│  │  • Gap Analysis                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA ACQUISITION LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  bioRxiv    │  │    PMC      │  │   arXiv     │            │
│  │  Scraper    │  │  E-Utils    │  │    API      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                 │                 │                    │
│         └─────────────────┴─────────────────┘                    │
│                           │                                      │
│                           ▼                                      │
│                  ┌─────────────────┐                            │
│                  │  Rate Limiter   │                            │
│                  │  Error Handler  │                            │
│                  └─────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PROCESSING & ANALYSIS LAYER                      │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │  Publication Parser  │  │   Deduplicator       │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                │                      │                          │
│                └──────────┬───────────┘                          │
│                           ▼                                      │
│            ┌─────────────────────────────┐                      │
│            │   [Optional] Claude AI      │                      │
│            │   • Extract model names     │                      │
│            │   • Identify crops          │                      │
│            │   • Summarize findings      │                      │
│            │   • List datasets           │                      │
│            │   • Note limitations        │                      │
│            └─────────────────────────────┘                      │
│                           │                                      │
│                           ▼                                      │
│            ┌─────────────────────────────┐                      │
│            │   Gap Analyzer              │                      │
│            │   • Coverage analysis       │                      │
│            │   • Trend detection         │                      │
│            │   • Opportunity mapping     │                      │
│            └─────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT GENERATION LAYER                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  JSON Report   │  │  Text Summary  │  │  CSV Export    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflow Sequence

### Phase 1: Initialization
```
1. Load Configuration
   ├─→ Read target models list
   ├─→ Read cereal crops list
   ├─→ Load search queries
   └─→ Configure data sources

2. Initialize API Clients
   ├─→ Setup HTTP session with headers
   ├─→ Configure rate limiting
   └─→ [Optional] Initialize Claude API
```

### Phase 2: Literature Search
```
For each search query:
  │
  ├─→ bioRxiv Search
  │   ├─→ Construct search URL
  │   ├─→ Send HTTP request
  │   ├─→ Parse HTML response
  │   ├─→ Extract article metadata
  │   └─→ Rate limit delay (1-2s)
  │
  ├─→ PubMed Central Search
  │   ├─→ Query esearch API
  │   ├─→ Get PMC IDs
  │   ├─→ Fetch article summaries
  │   ├─→ Extract metadata
  │   └─→ Rate limit delay
  │
  └─→ arXiv Search
      ├─→ Query arXiv API
      ├─→ Parse XML response
      ├─→ Extract paper details
      └─→ Rate limit delay
```

### Phase 3: Data Processing
```
1. Deduplication
   ├─→ Create title-based hash
   ├─→ Compare with existing entries
   └─→ Keep unique publications

2. [Optional] AI Enhancement
   For each publication:
   ├─→ Prepare analysis prompt
   ├─→ Call Claude API
   ├─→ Parse JSON response
   ├─→ Update publication object
   └─→ Rate limit delay

3. Validation
   ├─→ Check required fields
   ├─→ Validate URLs
   └─→ Flag incomplete records
```

### Phase 4: Gap Analysis
```
1. Coverage Analysis
   ├─→ Count publications per model
   ├─→ Count publications per crop
   └─→ Identify underrepresented areas

2. Trend Detection
   ├─→ Analyze publication years
   ├─→ Identify emerging models
   └─→ Track research momentum

3. Gap Identification
   ├─→ Compare vs. threshold (3 pubs)
   ├─→ Identify missing applications
   ├─→ List dataset gaps
   ├─→ Note methodological gaps
   └─→ Highlight rice-specific opportunities
```

### Phase 5: Report Generation
```
1. Compile Data
   ├─→ Aggregate all publications
   ├─→ Structure gap analysis
   └─→ Generate recommendations

2. Create JSON Report
   ├─→ Format metadata
   ├─→ Serialize publications
   ├─→ Include gap analysis
   └─→ Write to file

3. Create Text Summary
   ├─→ Generate human-readable overview
   ├─→ Format statistics
   ├─→ List key findings
   └─→ Write to file
```

---

## 🎯 Component Details

### GenomicLLMAgent Class

**Responsibilities:**
- Orchestrate entire workflow
- Manage data sources
- Coordinate searches
- Perform gap analysis
- Generate reports

**Key Methods:**
```python
search_biorxiv(query, max_results)
search_pubmed_central(query, max_results)
search_arxiv(query, max_results)
analyze_publication_with_claude(publication)
run_literature_search(use_claude)
identify_research_gaps()
generate_literature_review_report(output_file)
```

### Publication Data Structure

```python
@dataclass
class Publication:
    title: str              # Paper title
    authors: List[str]      # Author list
    year: int              # Publication year
    abstract: str          # Full abstract
    url: str               # Direct link
    source: str            # Data source (bioRxiv/PMC/arXiv)
    model_name: str        # Genomic LLM discussed
    crop_focus: List[str]  # Crops mentioned
    key_findings: List[str] # Main discoveries
    methodology: str       # Experimental approach
    datasets_used: List[str] # Data resources
    limitations: List[str]  # Stated gaps
```

### Search Strategy

**Multi-Source Approach:**
1. **bioRxiv**: Biology preprints, latest research
2. **PMC**: Peer-reviewed open access papers
3. **arXiv**: CS/ML papers on genomic models

**Query Construction:**
- Combine model names with crop terms
- Include synonyms (e.g., "corn" and "maize")
- Add domain keywords ("genomic", "transformer")

**Pagination:**
- Request 10-20 results per query
- Multiple queries cover broader space
- Deduplication ensures uniqueness

---

## 🔬 AI Analysis Pipeline (Optional)

### When Claude is Enabled:

```
For each publication:
  │
  ├─→ Prepare Structured Prompt
  │   ├─→ Include title & abstract
  │   ├─→ Specify extraction format (JSON)
  │   └─→ Define target fields
  │
  ├─→ Call Anthropic API
  │   ├─→ Model: claude-sonnet-4
  │   ├─→ Max tokens: 1000
  │   └─→ Temperature: 0.3 (for consistency)
  │
  ├─→ Parse Response
  │   ├─→ Extract JSON from text
  │   ├─→ Validate field types
  │   └─→ Handle parsing errors
  │
  └─→ Update Publication
      ├─→ Set model_name
      ├─→ Set crop_focus
      ├─→ Set key_findings
      ├─→ Set methodology
      ├─→ Set datasets_used
      └─→ Set limitations
```

### Example Claude Prompt:

```
Analyze this genomic LLM research paper:

Title: [TITLE]
Abstract: [ABSTRACT]

Extract:
1. Genomic LLM model(s) discussed
2. Crop species focus (especially cereals)
3. Key findings (3-5 main points)
4. Methodology used
5. Datasets mentioned
6. Stated limitations

Return as JSON: {
  "model_name": "...",
  "crop_focus": [...],
  "key_findings": [...],
  "methodology": "...",
  "datasets_used": [...],
  "limitations": [...]
}
```

---

## 📊 Gap Analysis Algorithm

### Step 1: Count Coverage
```python
crop_mentions = defaultdict(int)
model_mentions = defaultdict(int)

for publication in publications:
    for crop in publication.crop_focus:
        crop_mentions[crop] += 1
    
    if publication.model_name:
        model_mentions[publication.model_name] += 1
```

### Step 2: Identify Gaps
```python
threshold = 3  # Minimum publications

for crop in target_crops:
    if crop_mentions[crop] < threshold:
        gaps["understudied_crops"].append(crop)
```

### Step 3: Detect Missing Applications
```python
# Check for absence of key application areas
applications = [
    "climate stress prediction",
    "yield optimization",
    "disease resistance",
    "pan-genome analysis",
    "breeding integration"
]

for app in applications:
    app_count = count_application_mentions(publications, app)
    if app_count < threshold:
        gaps["missing_applications"].append(app)
```

### Step 4: Rice-Specific Analysis
```python
rice_pub_count = crop_mentions.get("rice", 0)
rice_models = models_applied_to_rice(publications)

if rice_pub_count < 5:
    gaps["rice_specific_gaps"].append(
        "Limited genomic LLM research specifically for rice"
    )

if len(rice_models) < 3:
    gaps["rice_specific_gaps"].append(
        "Few models fine-tuned on rice genomic data"
    )
```

---

## ⚙️ Configuration Options

### Rate Limiting
```json
{
  "rate_limiting": {
    "requests_per_minute": 30,
    "delay_between_requests": 2.0,
    "retry_attempts": 3,
    "retry_delay": 5.0
  }
}
```

### Search Filters
```json
{
  "search_filters": {
    "min_year": 2020,
    "max_year": 2026,
    "languages": ["en"],
    "open_access_only": true
  }
}
```

### Output Settings
```json
{
  "output_settings": {
    "output_directory": "/mnt/user-data/outputs",
    "json_filename": "literature_review.json",
    "summary_filename": "literature_review_summary.txt",
    "include_abstracts": true,
    "pretty_print": true
  }
}
```

---

## 🔐 Error Handling

### Network Errors
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error(f"Network error: {e}")
    retry_with_exponential_backoff()
```

### Parsing Errors
```python
try:
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('title').text
except AttributeError:
    logger.warning(f"Could not parse title from {url}")
    continue  # Skip to next result
```

### API Errors
```python
try:
    response = anthropic_client.messages.create(...)
except APIError as e:
    logger.error(f"Claude API error: {e}")
    # Continue without AI analysis
```

---

## 📈 Performance Considerations

### Speed Optimization
- **Parallel Requests**: Can implement concurrent searches
- **Caching**: Store results to avoid re-scraping
- **Batch Processing**: Group API calls

### Resource Usage
- **Memory**: ~100MB for 500 publications
- **Network**: 1-5 MB per search query
- **Time**: 
  - Without Claude: ~10 minutes for 100 publications
  - With Claude: ~30 minutes for 100 publications

### Scalability
- **Publications**: Tested up to 1000 publications
- **Queries**: Can handle 50+ search queries
- **Sources**: Extensible to additional databases

---

## 🚀 Future Enhancements

### Potential Improvements
1. **Full-Text Analysis**: Extract from PDF papers
2. **Citation Network**: Build citation graphs
3. **Collaboration Detection**: Identify research groups
4. **Trend Forecasting**: Predict emerging topics
5. **Automated Alerts**: Notify on new publications
6. **Interactive Dashboard**: Web UI for exploration
7. **Export Formats**: BibTeX, EndNote, Zotero

### Additional Data Sources
- **Google Scholar**: Broader coverage
- **Semantic Scholar**: Better metadata
- **Europe PMC**: European publications
- **DOAJ**: Directory of Open Access Journals

---

## 📚 Integration Possibilities

### With Research Tools
```python
# Export to reference manager
def export_to_bibtex(publications):
    # Generate .bib file

# Link to Zotero
def sync_with_zotero(publications, api_key):
    # Upload to Zotero library
```

### With Analysis Tools
```python
# Network analysis
import networkx as nx
G = build_citation_network(publications)

# Topic modeling
from sklearn.decomposition import LatentDirichletAllocation
topics = lda.fit_transform(abstracts)
```

### With Visualization
```python
import plotly.express as px

# Timeline visualization
fig = px.timeline(publications, x_start="year", color="model_name")

# Geographic distribution
fig = px.scatter_geo(publications, locations="institution_country")
```

---

**End of Architecture Document**

This agent provides a comprehensive foundation for automated literature review in genomic AI research. The modular design allows for easy customization and extension based on specific research needs.
