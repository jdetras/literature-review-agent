# Search Parameter Adjustment Guide

## 🎯 How to Fix Irrelevant Results

You identified two key problems:
1. ❌ Irrelevant papers (e.g., about "sleeping")
2. ❌ Old papers (e.g., 2004, before LLMs existed)

The **improved version (v2)** fixes both issues!

---

## 📋 What Changed in Version 2

### ✅ New Features:

1. **Date Filtering** - Only papers from 2018+ (when transformers emerged)
2. **Keyword Exclusion** - Automatically rejects papers about sleep, clinical medicine, etc.
3. **Relevance Scoring** - Each paper gets a score 0-100
4. **Smart Filtering** - Must have ML/AI keywords AND plant/genomics keywords
5. **Better Queries** - More specific search terms

---

## ⚙️ Adjustable Parameters

### 1. **Date Range** (Line 48-49)

```python
self.min_year = 2018  # Change this!
self.max_year = datetime.now().year
```

**Options:**
- `2018` - Include early transformer papers
- `2020` - Only COVID-era onwards (more mature LLMs)
- `2022` - Only very recent work
- `2015` - If you want pre-transformer deep learning too

**Recommendation:** Keep at `2018` for genomic LLMs

---

### 2. **Exclusion Keywords** (Lines 60-66)

```python
self.exclusion_keywords = [
    "sleep", "sleeping", "clinical trial", "patient",
    "disease diagnosis", "cancer therapy", "drug",
    "pharmaceutical", "medical imaging", "radiology",
    "circadian", "insomnia", "Alzheimer", "Parkinson",
    "clinical outcome", "hospital", "medication"
]
```

**How to Add More:**
```python
self.exclusion_keywords = [
    "sleep", "sleeping",  # Already there
    "neuroscience",       # ADD: if getting brain papers
    "psychology",         # ADD: if getting behavior papers
    "COVID-19",          # ADD: if getting pandemic papers
    "protein folding",   # ADD: if want only DNA/RNA (not proteins)
    # Add any terms from unwanted papers!
]
```

**How It Works:**
- If **ANY** exclusion keyword appears → paper is **rejected**
- Case-insensitive matching

---

### 3. **Required Keywords** (Lines 51-57)

```python
self.required_keywords = [
    "transformer", "language model", "foundation model",
    "pre-trained", "BERT", "attention mechanism",
    "embedding", "self-supervised", "deep learning",
    "neural network", "machine learning"
]
```

**How to Adjust:**
```python
# Make MORE strict (fewer false positives):
self.required_keywords = [
    "transformer", "language model", "foundation model",
    "pre-trained", "BERT"
]

# Make LESS strict (more results):
self.required_keywords = [
    "transformer", "language model", "deep learning",
    "neural network", "machine learning", "AI"
]
```

**How It Works:**
- Paper must have **at least ONE** of these keywords
- Otherwise rejected

---

### 4. **Minimum Relevance Score** (Line 474)

```python
publications = agent.run_literature_search(
    use_claude=False,
    min_relevance=40.0  # Change this!
)
```

**Options:**
- `30.0` - More permissive (more papers, some may be tangential)
- `40.0` - **Recommended** (good balance)
- `50.0` - Stricter (fewer but more relevant papers)
- `60.0` - Very strict (only highly relevant papers)

**Relevance Score Breakdown:**
```
0-20 points:  Recent publication (2023+ = 20 pts)
0-30 points:  ML/AI keywords found
0-30 points:  Plant/genomics keywords found
0-20 points:  Target model names found
Penalties:    -15 per exclusion keyword
```

---

### 5. **Search Queries** (Lines 461-468)

```python
queries = [
    "genomic foundation model plant",
    "AgroNT transformer agriculture",
    "DNABERT genome annotation",
    # ... add more here
]
```

**How to Customize:**
```python
# For RICE-SPECIFIC search:
queries = [
    "rice genome language model",
    "Oryza sativa transformer",
    "rice genomics neural network",
    "paddy genome deep learning"
]

# For SPECIFIC MODELS:
queries = [
    "AgroNT",
    "PlantCAD",
    "DNABERT plant",
    "Nucleotide Transformer cereal"
]

# For BROADER COVERAGE:
queries = [
    "plant genomics transformer",
    "crop genome foundation model",
    "agricultural AI language model"
]
```

---

### 6. **Results Per Query** (Lines 462-468)

```python
pubs = self.search_biorxiv(query, max_results=10)  # Change this!
```

**Options:**
- `max_results=5` - Faster, fewer results
- `max_results=10` - **Recommended**
- `max_results=20` - More results, slower
- `max_results=50` - Comprehensive but very slow

---

## 🔧 Common Adjustments

### Problem: "Still getting irrelevant papers"

**Solution 1: Add more exclusion keywords**
```python
# Check the irrelevant paper titles
# Add those keywords to exclusion_keywords list
self.exclusion_keywords.append("unwanted_term")
```

**Solution 2: Increase minimum relevance**
```python
min_relevance=50.0  # Instead of 40.0
```

**Solution 3: Make queries more specific**
```python
queries = [
    "genomic foundation model rice cereal",  # Added "rice cereal"
    "plant genome transformer 2020",         # Added year
]
```

---

### Problem: "Not enough results"

**Solution 1: Lower minimum year**
```python
self.min_year = 2015  # Instead of 2018
```

**Solution 2: Lower relevance threshold**
```python
min_relevance=30.0  # Instead of 40.0
```

**Solution 3: Add more queries**
```python
queries = [
    # ... existing queries ...
    "crop genomics AI",
    "plant breeding machine learning",
    "agricultural deep learning"
]
```

**Solution 4: Increase max_results**
```python
pubs = self.search_biorxiv(query, max_results=20)
```

---

### Problem: "Missing important papers I know exist"

**Solution 1: Search for specific paper**
```python
# Add very specific query
queries.append("exact title of the paper")
```

**Solution 2: Check if it's being filtered**
```python
# Temporarily disable filtering to debug
# Comment out the relevance filter
# if not self.is_relevant(title, abstract, year):
#     continue
```

**Solution 3: Lower all thresholds**
```python
self.min_year = 2015
min_relevance=25.0
```

---

## 📊 Example Configurations

### Configuration 1: "Very Strict" (High Quality Only)
```python
self.min_year = 2020
self.exclusion_keywords = [...]  # All of them
min_relevance = 55.0
queries = [
    "rice genome foundation model",
    "AgroNT rice",
    "wheat genome transformer"
]
```
**Result:** ~10-20 highly relevant papers

---

### Configuration 2: "Balanced" (Recommended)
```python
self.min_year = 2018
self.exclusion_keywords = [...]  # All of them
min_relevance = 40.0
queries = [
    "genomic foundation model plant",
    "crop genome language model",
    # 6-8 queries total
]
```
**Result:** ~30-50 relevant papers

---

### Configuration 3: "Comprehensive" (Cast Wide Net)
```python
self.min_year = 2016
self.exclusion_keywords = ["sleep", "clinical", "patient"]  # Fewer
min_relevance = 30.0
queries = [
    "plant genomics deep learning",
    "agricultural AI",
    # 10+ queries
]
```
**Result:** ~50-100 papers (more noise)

---

### Configuration 4: "Rice Only"
```python
self.cereal_crops = ["rice", "Oryza sativa"]  # Focus crops
self.min_year = 2018
min_relevance = 35.0
queries = [
    "rice genome language model",
    "Oryza sativa transformer",
    "rice genomics BERT",
    "paddy genome neural network"
]
```
**Result:** ~15-30 rice-specific papers

---

## 🎯 Quick Reference Table

| Parameter | Default | More Results | Higher Quality |
|-----------|---------|--------------|----------------|
| min_year | 2018 | 2015 | 2020 |
| min_relevance | 40.0 | 30.0 | 55.0 |
| max_results | 10 | 20 | 5 |
| exclusion_keywords | 14 | 5 | 20+ |
| queries | 8 | 15+ | 4-6 specific |

---

## 💡 Best Practices

1. **Start Strict, Then Relax**
   - Begin with default settings
   - If too few results, lower thresholds gradually

2. **Examine Filtered Papers**
   - Look at the "⊘ Filtered:" messages in output
   - See if legitimate papers are being rejected
   - Adjust exclusion keywords accordingly

3. **Test Individual Queries**
   - Run one query at a time
   - See which queries produce best results
   - Focus on those

4. **Check Relevance Scores**
   - Review the top papers by score
   - If scores are all 40-45, lower threshold to 35
   - If scores are all 70-90, you can raise threshold

5. **Iterate**
   - Run → Review → Adjust → Repeat
   - 2-3 iterations usually gets optimal results

---

## 🚀 How to Use v2

```bash
# Download the new improved version
# Then run:
python3 genomic_llm_literature_agent_v2.py
```

**Output will show:**
```
⊘ Filtered: Circadian rhythm and sleep... (year: 2019, low relevance)
⊘ Filtered: Clinical outcomes in cancer... (year: 2004)
✓ Found: AgroNT: Foundation Model for Plant Genomes... (score: 78.5, year: 2023)
```

---

## 📝 Making Permanent Changes

Edit `genomic_llm_literature_agent_v2.py`:

1. **Line 48** - Change `self.min_year`
2. **Lines 60-66** - Add to `self.exclusion_keywords`
3. **Lines 461-468** - Modify `queries` list
4. **Line 474** - Change `min_relevance` parameter

Save and re-run!

---

**The v2 agent solves your issues!** No more sleep papers, no more 2004 papers! 🎉
