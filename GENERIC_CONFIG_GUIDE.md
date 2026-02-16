# Generic Literature Review Agent - Configuration Guide

## 🎯 Overview

The Generic Literature Review Agent is **fully configurable via text files**. You can use it for:
- 🌾 **Plant genomics** (default configuration)
- 🧬 **Cancer research** 
- 🤖 **AI/ML research**
- 🧪 **Any research domain**

**No code changes needed!** Just edit 3 text files.

---

## 📁 Configuration Files

### 1. `config_models.txt` - Target Models/Methods
Define what models, methods, or tools you want to track.

**Format:**
```
# Comments start with #
Model1
Model2
AnotherModel
```

**Examples by Domain:**

**Plant Genomics:**
```
AgroNT
DNABERT
PlantCAD
Nucleotide Transformer
```

**Cancer Research:**
```
AlphaFold
BioBERT
CancerBERT
OncoKB
```

**Computer Vision:**
```
ResNet
YOLO
ViT
CLIP
SAM
```

**NLP:**
```
GPT-4
Claude
BERT
T5
LLaMA
```

---

### 2. `config_topics.txt` - Research Topics/Subjects
Define your research domain, organisms, diseases, or focus areas.

**Format:**
```
# One topic per line
Topic 1
Scientific Name
Alternative Name
```

**Examples by Domain:**

**Plant Genomics:**
```
rice
Oryza sativa
wheat
maize
drought tolerance
```

**Cancer Research:**
```
breast cancer
immunotherapy
tumor microenvironment
PD-L1
metastasis
```

**Climate Science:**
```
climate change
global warming
carbon sequestration
extreme weather
sea level rise
```

**Materials Science:**
```
graphene
perovskite
superconductor
battery technology
quantum materials
```

---

### 3. `config_search.txt` - Search Parameters
Control search behavior, filters, and quality thresholds.

**Key Parameters:**

#### Date Range
```
min_year = 2018          # Oldest papers to include
max_year = current       # 'current' or specific year
```

**Recommendations:**
- AI/ML: `2017` (when Transformers emerged)
- Cancer: `2015` (immunotherapy era)
- Climate: `2010` (recent IPCC cycles)
- Your field: Year of major breakthrough

#### Quality Filters
```
min_relevance = 40.0              # Minimum score 0-100
max_results_per_query = 10        # Results per search
```

**Recommendations:**
- Exploratory: `30` (more results, some noise)
- Balanced: `40` (good quality/quantity)
- Strict: `55` (high quality, fewer results)

#### Required Keywords
Papers **must** contain at least ONE:
```
[required_keywords]
machine learning
deep learning
neural network
artificial intelligence
```

**Customize for your domain:**
- Genomics: `genome`, `DNA`, `sequence`, `gene`
- Cancer: `cancer`, `tumor`, `oncology`, `malignancy`
- Climate: `climate`, `atmospheric`, `temperature`, `emissions`

#### Exclusion Keywords
Papers with **any** of these are rejected:
```
[exclusion_keywords]
sleep
clinical trial
patient
```

**Add domain-specific noise:**
- Genomics: `sleep`, `clinical`, `pharmaceutical`
- Cancer: `agriculture`, `plant`, `crop`
- ML: `clinical`, `patient`, `hospital`

#### Boost Keywords
Papers with these get higher scores:
```
[boost_keywords]
genome
DNA
sequence
plant
```

**Customize for domain:**
- Cancer: `cancer`, `tumor`, `therapy`, `biomarker`
- AI: `model`, `algorithm`, `accuracy`, `performance`
- Climate: `warming`, `emission`, `atmospheric`, `carbon`

#### Custom Queries
Define specific search terms:
```
[custom_queries]
{model} transformer
{topic} prediction
cancer {model} detection
```

**Placeholders:**
- `{model}` → Replaced with each model from config_models.txt
- `{topic}` → Replaced with each topic from config_topics.txt

---

## 🚀 Quick Start Examples

### Example 1: Plant Genomics (Default)

**config_models.txt:**
```
AgroNT
DNABERT
PlantCAD
```

**config_topics.txt:**
```
rice
wheat
maize
```

**config_search.txt:**
```
min_year = 2018
min_relevance = 40.0
[required_keywords]
transformer
language model
deep learning
[exclusion_keywords]
sleep
clinical
patient
```

**Run:**
```bash
python3 generic_literature_agent.py
```

---

### Example 2: Cancer Research

**config_models.txt:**
```
AlphaFold
BioBERT
CancerBERT
OncoKB
```

**config_topics.txt:**
```
breast cancer
lung cancer
immunotherapy
PD-L1
```

**config_search.txt:**
```
min_year = 2015
min_relevance = 45.0
[required_keywords]
machine learning
deep learning
artificial intelligence
prediction
[exclusion_keywords]
agriculture
plant
crop
veterinary
[boost_keywords]
cancer
tumor
oncology
therapy
biomarker
```

---

### Example 3: Climate Science

**config_models.txt:**
```
LSTM
Transformer
ResNet
U-Net
GAN
```

**config_topics.txt:**
```
climate change
global warming
extreme weather
sea level rise
carbon emissions
```

**config_search.txt:**
```
min_year = 2010
min_relevance = 35.0
[required_keywords]
machine learning
deep learning
neural network
prediction
modeling
[exclusion_keywords]
clinical
patient
medical
[boost_keywords]
climate
temperature
atmospheric
carbon
warming
```

---

### Example 4: Computer Vision

**config_models.txt:**
```
YOLO
ResNet
ViT
CLIP
SAM
Mask R-CNN
```

**config_topics.txt:**
```
object detection
image segmentation
scene understanding
autonomous driving
medical imaging
```

**config_search.txt:**
```
min_year = 2015
min_relevance = 40.0
[required_keywords]
computer vision
deep learning
convolutional
neural network
[exclusion_keywords]
genomics
DNA
protein
[boost_keywords]
image
vision
detection
segmentation
visual
```

---

## 🔧 Advanced Configuration

### Adaptive Learning
```
adaptive_mode = true              # Auto-adjust parameters
auto_refine_queries = true        # Generate smart queries
learning_rate = 0.1               # 0.1=cautious, 0.5=aggressive
target_publications_per_run = 30  # Target papers per search
```

### Custom Queries with Logic
```
[custom_queries]
{model} AND {topic}
({model} OR deep learning) AND {topic}
"{model}" prediction {topic}
{topic} {model} 2023
```

---

## 📊 Testing Your Configuration

### 1. Test with Small Limits
```
max_results_per_query = 5  # Start small
```

### 2. Check Filtered Papers
Look at console output:
```
⊘ Filtered: Paper title... (reason)
✓ Found: Paper title... (score: 78.5)
```

### 3. Adjust Parameters
- Too many irrelevant? → Add exclusion keywords
- Too few results? → Lower `min_relevance`
- Wrong papers? → Adjust required/boost keywords

### 4. Iterate
```bash
# Run → Review → Adjust → Repeat
python3 generic_literature_agent.py
# Check output_reports/literature_review_summary.txt
# Edit config files
# Run again
```

---

## 🎯 Domain-Specific Recommendations

### Genomics/Biology
```
min_year = 2018
required_keywords = genome, DNA, sequence, gene
exclusion_keywords = sleep, clinical, pharmaceutical
boost_keywords = genome, DNA, plant, crop, species
```

### Medicine/Healthcare
```
min_year = 2015
required_keywords = patient, clinical, disease, treatment
exclusion_keywords = agriculture, plant, animal
boost_keywords = patient, therapy, diagnosis, clinical
```

### Computer Science/AI
```
min_year = 2017
required_keywords = algorithm, model, network, learning
exclusion_keywords = clinical, patient, medical
boost_keywords = accuracy, performance, state-of-the-art
```

### Climate/Earth Science
```
min_year = 2010
required_keywords = climate, atmospheric, environmental
exclusion_keywords = clinical, medical, patient
boost_keywords = temperature, carbon, emission, warming
```

### Social Sciences
```
min_year = 2015
required_keywords = survey, study, analysis, behavior
exclusion_keywords = genome, DNA, clinical
boost_keywords = social, behavior, psychology, demographic
```

---

## 💡 Pro Tips

### 1. Start Broad, Then Narrow
```
# First run - broad
min_relevance = 30.0
exclusion_keywords = []

# Review results, then refine
min_relevance = 45.0
exclusion_keywords = [unwanted terms from results]
```

### 2. Use Scientific Names
```
# Include both common and scientific names
rice
Oryza sativa
breast cancer
mammary carcinoma
```

### 3. Include Variations
```
# Different spellings/terms
machine learning
ML
deep learning
DL
```

### 4. Test Individual Queries
Comment out all but one:
```
[custom_queries]
{model} genomics
# {topic} prediction
# cancer detection
```

### 5. Monitor Scores
Check `output_reports/literature_review_summary.txt`:
- Average score <40? → Queries too broad
- Average score >70? → Queries working well
- Average score >80? → May be too specific

---

## 🔄 Workflow

```
1. Choose your research domain
   ↓
2. Edit config_models.txt
   (list your target models/methods)
   ↓
3. Edit config_topics.txt
   (list your research topics)
   ↓
4. Edit config_search.txt
   (set parameters and keywords)
   ↓
5. Run: python3 generic_literature_agent.py
   ↓
6. Review: output_reports/literature_review_summary.txt
   ↓
7. Adjust configs if needed
   ↓
8. Re-run until satisfied
   ↓
9. Convert: python3 convert_to_github_pages.py
   ↓
10. Publish to GitHub Pages
```

---

## 📚 Real-World Examples

### Case Study 1: Rice Genomics Researcher
**Files:**
- config_models.txt: AgroNT, DNABERT, PlantCAD
- config_topics.txt: rice, Oryza sativa, yield, drought
- config_search.txt: min_year=2018, focus on plant genomics

**Result:** 38 highly relevant papers on genomic LLMs for rice

### Case Study 2: Cancer Immunotherapy Lab
**Files:**
- config_models.txt: BioBERT, CancerBERT, AlphaFold
- config_topics.txt: immunotherapy, PD-L1, checkpoint inhibitor
- config_search.txt: min_year=2015, exclude non-cancer

**Result:** 42 papers on AI in cancer immunotherapy

### Case Study 3: Climate AI Startup
**Files:**
- config_models.txt: LSTM, Transformer, GNN
- config_topics.txt: climate prediction, extreme weather
- config_search.txt: min_year=2010, focus on modeling

**Result:** 51 papers on ML for climate modeling

---

## 🚀 Ready-to-Use Templates

Templates available in `/examples/`:
- `cancer_research/` - Cancer & medical AI
- `climate_science/` - Climate & environment
- `computer_vision/` - CV & image processing
- `nlp/` - Natural language processing
- `materials_science/` - Materials & chemistry

Copy files to main directory:
```bash
cp examples/cancer_research/* .
python3 generic_literature_agent.py
```

---

## ✅ Configuration Checklist

- [ ] Edited config_models.txt (added your models)
- [ ] Edited config_topics.txt (added your topics)
- [ ] Set min_year appropriately
- [ ] Set min_relevance score
- [ ] Added required_keywords for your domain
- [ ] Added exclusion_keywords to filter noise
- [ ] Added boost_keywords for better ranking
- [ ] Tested with small max_results first
- [ ] Reviewed filtered papers
- [ ] Adjusted based on results
- [ ] Ready to run full search!

---

**Your literature review agent is now ready for ANY research domain!** 🎉

Just edit 3 text files - no coding required!
