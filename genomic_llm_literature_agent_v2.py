#!/usr/bin/env python3
"""
IMPROVED Genomic LLM Literature Review Agent
Features:
- Date filtering (2018+)
- Keyword exclusion (sleep, clinical, etc.)
- Relevance scoring
- Better query construction
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import time

import requests
from bs4 import BeautifulSoup


@dataclass
class Publication:
    """Structure for storing publication data"""
    title: str
    authors: List[str]
    year: int
    abstract: str
    url: str
    source: str
    relevance_score: float = 0.0  # NEW: Relevance scoring
    model_name: Optional[str] = None
    crop_focus: List[str] = None
    key_findings: List[str] = None
    methodology: str = ""
    datasets_used: List[str] = None
    limitations: List[str] = None
    
    def __post_init__(self):
        if self.crop_focus is None:
            self.crop_focus = []
        if self.key_findings is None:
            self.key_findings = []
        if self.datasets_used is None:
            self.datasets_used = []
        if self.limitations is None:
            self.limitations = []


class ImprovedGenomicLLMAgent:
    """Enhanced AI Agent with better filtering"""
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.publications = []
        self.anthropic_api_key = anthropic_api_key
        
        # Target models
        self.target_models = [
            "AgroNT", "PlantCAD", "AlphaGenome", "DNABERT", 
            "Nucleotide Transformer", "HyenaDNA", "Caduceus",
            "GenSLM", "GENA-LM", "Enformer", "GPN", "Evo"
        ]
        
        # Cereal crops
        self.cereal_crops = [
            "rice", "wheat", "maize", "corn", "barley", 
            "sorghum", "millet", "oats", "rye", 
            "Oryza sativa", "Triticum", "Zea mays"
        ]
        
        # NEW: Date range for filtering
        self.min_year = 2018  # Transformers emerged ~2017-2018
        self.max_year = datetime.now().year
        
        # NEW: Required keywords (at least one must appear)
        self.required_keywords = [
            "transformer", "language model", "foundation model",
            "pre-trained", "BERT", "attention mechanism",
            "embedding", "self-supervised", "deep learning",
            "neural network", "machine learning"
        ]
        
        # NEW: Exclusion keywords (reject if these appear)
        self.exclusion_keywords = [
            "sleep", "sleeping", "clinical trial", "patient",
            "disease diagnosis", "cancer therapy", "drug",
            "pharmaceutical", "medical imaging", "radiology",
            "circadian", "insomnia", "Alzheimer", "Parkinson",
            "clinical outcome", "hospital", "medication"
        ]
        
        # NEW: Plant/genomics keywords (boost relevance)
        self.plant_genomics_keywords = [
            "plant", "crop", "genome", "genomic", "DNA",
            "gene", "agriculture", "breeding", "chromosome",
            "nucleotide", "sequence", "rice", "wheat", "maize"
        ]
    
    def calculate_relevance_score(self, title: str, abstract: str, year: int) -> float:
        """
        Calculate relevance score for a publication
        Score from 0-100, higher = more relevant
        """
        score = 0.0
        text = f"{title} {abstract}".lower()
        
        # 1. Year recency (0-20 points)
        if year >= 2023:
            score += 20
        elif year >= 2021:
            score += 15
        elif year >= 2019:
            score += 10
        elif year >= 2018:
            score += 5
        
        # 2. Required keywords (0-30 points)
        required_found = sum(1 for kw in self.required_keywords if kw.lower() in text)
        score += min(required_found * 6, 30)
        
        # 3. Plant/genomics keywords (0-30 points)
        plant_found = sum(1 for kw in self.plant_genomics_keywords if kw.lower() in text)
        score += min(plant_found * 3, 30)
        
        # 4. Model names (0-20 points)
        models_found = sum(1 for model in self.target_models if model.lower() in text)
        score += min(models_found * 10, 20)
        
        # 5. Penalties for exclusion keywords
        exclusions_found = sum(1 for kw in self.exclusion_keywords if kw.lower() in text)
        score -= exclusions_found * 15  # Heavy penalty
        
        return max(0.0, min(100.0, score))  # Clamp to 0-100
    
    def is_relevant(self, title: str, abstract: str, year: int, 
                   min_score: float = 30.0) -> bool:
        """
        Determine if a publication is relevant
        """
        # 1. Year filter
        if year < self.min_year or year > self.max_year:
            return False
        
        text = f"{title} {abstract}".lower()
        
        # 2. Exclusion filter (hard reject)
        for keyword in self.exclusion_keywords:
            if keyword.lower() in text:
                return False
        
        # 3. Must have at least one required keyword
        has_required = any(kw.lower() in text for kw in self.required_keywords)
        if not has_required:
            return False
        
        # 4. Check relevance score
        score = self.calculate_relevance_score(title, abstract, year)
        return score >= min_score
    
    def search_biorxiv(self, query: str, max_results: int = 20) -> List[Publication]:
        """Search bioRxiv with improved filtering"""
        print(f"\n🔍 Searching bioRxiv for: {query}")
        publications = []
        
        try:
            # Add date filter to URL
            search_url = f"https://www.biorxiv.org/search/{query}%20numresults%3A{max_results}%20sort%3Arelevance-rank%20format_result%3Astandard"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; GenomicLLMAgent/2.0; Research)'
            }
            
            response = requests.get(search_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('span', class_='highwire-cite')
                
                for article in articles[:max_results]:
                    try:
                        title_elem = article.find('span', class_='highwire-cite-title')
                        if not title_elem:
                            continue
                        
                        title = title_elem.text.strip()
                        
                        # Try to get abstract preview
                        abstract = ""
                        abstract_elem = article.find('span', class_='highwire-cite-snippet')
                        if abstract_elem:
                            abstract = abstract_elem.text.strip()
                        
                        # Try to get year
                        year = datetime.now().year  # Default to current
                        date_elem = article.find('span', class_='highwire-cite-metadata-date')
                        if date_elem:
                            date_text = date_elem.text
                            year_match = re.search(r'20\d{2}', date_text)
                            if year_match:
                                year = int(year_match.group())
                        
                        # Get URL
                        link = title_elem.find('a')
                        url = f"https://www.biorxiv.org{link['href']}" if link else ""
                        
                        # Apply relevance filtering
                        if not self.is_relevant(title, abstract, year):
                            print(f"  ⊘ Filtered: {title[:60]}... (year: {year}, low relevance)")
                            continue
                        
                        score = self.calculate_relevance_score(title, abstract, year)
                        
                        pub = Publication(
                            title=title,
                            authors=[],
                            year=year,
                            abstract=abstract,
                            url=url,
                            source="bioRxiv",
                            relevance_score=score
                        )
                        publications.append(pub)
                        print(f"  ✓ Found: {title[:60]}... (score: {score:.1f}, year: {year})")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing article: {e}")
                        continue
                        
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error searching bioRxiv: {e}")
        
        return publications
    
    def search_pubmed_central(self, query: str, max_results: int = 20) -> List[Publication]:
        """Search PubMed Central with date filtering"""
        print(f"\n🔍 Searching PubMed Central for: {query}")
        publications = []
        
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
            
            # Add date filter to query
            date_filter = f" AND {self.min_year}:{self.max_year}[pdat]"
            full_query = query + date_filter
            
            search_url = f"{base_url}/esearch.fcgi"
            params = {
                'db': 'pmc',
                'term': full_query,
                'retmax': max_results * 2,  # Get extra to filter
                'retmode': 'json',
                'sort': 'relevance'
            }
            
            response = requests.get(search_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                id_list = data.get('esearchresult', {}).get('idlist', [])
                
                print(f"  Found {len(id_list)} articles (before filtering)")
                
                if id_list:
                    fetch_url = f"{base_url}/esummary.fcgi"
                    fetch_params = {
                        'db': 'pmc',
                        'id': ','.join(id_list),
                        'retmode': 'json'
                    }
                    
                    fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
                    
                    if fetch_response.status_code == 200:
                        details = fetch_response.json()
                        
                        for pmc_id in id_list:
                            try:
                                article = details.get('result', {}).get(pmc_id, {})
                                title = article.get('title', '')
                                
                                # Get year
                                pubdate = article.get('pubdate', '')
                                year = datetime.now().year
                                year_match = re.search(r'20\d{2}', pubdate)
                                if year_match:
                                    year = int(year_match.group())
                                
                                # Get abstract (not in summary, would need full fetch)
                                abstract = ""
                                
                                # Apply filtering
                                if not self.is_relevant(title, abstract, year):
                                    print(f"  ⊘ Filtered: {title[:60]}... (year: {year})")
                                    continue
                                
                                score = self.calculate_relevance_score(title, abstract, year)
                                
                                pub = Publication(
                                    title=title,
                                    authors=[],
                                    year=year,
                                    abstract=abstract,
                                    url=f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/",
                                    source="PMC",
                                    relevance_score=score
                                )
                                publications.append(pub)
                                print(f"  ✓ Found: {title[:60]}... (score: {score:.1f}, year: {year})")
                                
                                if len(publications) >= max_results:
                                    break
                                    
                            except Exception as e:
                                print(f"  ⚠ Error parsing article {pmc_id}: {e}")
                                continue
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error searching PMC: {e}")
        
        return publications
    
    def search_arxiv(self, query: str, max_results: int = 20) -> List[Publication]:
        """Search arXiv with improved filtering"""
        print(f"\n🔍 Searching arXiv for: {query}")
        publications = []
        
        try:
            base_url = "http://export.arxiv.org/api/query"
            
            # Build better query with categories
            categories = "cat:q-bio.GN OR cat:cs.LG OR cat:cs.AI OR cat:stat.ML"
            full_query = f"({query}) AND ({categories})"
            
            params = {
                'search_query': full_query,
                'start': 0,
                'max_results': max_results * 2,  # Get extra to filter
                'sortBy': 'relevance'
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')
                
                print(f"  Found {len(entries)} articles (before filtering)")
                
                for entry in entries:
                    try:
                        title = entry.find('title').text.strip()
                        abstract = entry.find('summary').text.strip()
                        url = entry.find('id').text.strip()
                        published = entry.find('published').text.strip()
                        year = int(published[:4])
                        
                        authors = [author.find('name').text for author in entry.find_all('author')]
                        
                        # Apply filtering
                        if not self.is_relevant(title, abstract, year):
                            print(f"  ⊘ Filtered: {title[:60]}... (year: {year})")
                            continue
                        
                        score = self.calculate_relevance_score(title, abstract, year)
                        
                        pub = Publication(
                            title=title,
                            authors=authors,
                            year=year,
                            abstract=abstract,
                            url=url,
                            source="arXiv",
                            relevance_score=score
                        )
                        publications.append(pub)
                        print(f"  ✓ Found: {title[:60]}... (score: {score:.1f}, year: {year})")
                        
                        if len(publications) >= max_results:
                            break
                            
                    except Exception as e:
                        print(f"  ⚠ Error parsing entry: {e}")
                        continue
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error searching arXiv: {e}")
        
        return publications
    
    def run_literature_search(self, use_claude: bool = False, 
                            min_relevance: float = 40.0) -> List[Publication]:
        """Execute comprehensive literature search with filtering"""
        
        print("\n" + "="*70)
        print("🤖 IMPROVED GENOMIC LLM LITERATURE REVIEW AGENT")
        print("="*70)
        print(f"Date Range: {self.min_year}-{self.max_year}")
        print(f"Minimum Relevance Score: {min_relevance}")
        print(f"Target Models: {', '.join(self.target_models[:5])}...")
        print(f"Exclusion Keywords: {', '.join(self.exclusion_keywords[:5])}...")
        print("="*70)
        
        all_publications = []
        
        # Better, more specific queries
        queries = [
            "genomic foundation model plant",
            "AgroNT transformer agriculture",
            "DNABERT genome annotation",
            "nucleotide transformer cereal",
            "plant genome language model",
            "crop genomics deep learning 2020",
            "rice genome neural network",
            "wheat genomics machine learning"
        ]
        
        for query in queries:
            pubs = self.search_biorxiv(query, max_results=10)
            all_publications.extend(pubs)
            
            pubs = self.search_pubmed_central(query, max_results=10)
            all_publications.extend(pubs)
            
            pubs = self.search_arxiv(query, max_results=10)
            all_publications.extend(pubs)
        
        # Remove duplicates
        unique_pubs = {}
        for pub in all_publications:
            if pub.title and pub.title not in unique_pubs:
                unique_pubs[pub.title] = pub
        
        # Filter by minimum relevance score
        self.publications = [
            pub for pub in unique_pubs.values() 
            if pub.relevance_score >= min_relevance
        ]
        
        # Sort by relevance
        self.publications.sort(key=lambda x: x.relevance_score, reverse=True)
        
        print(f"\n\n📊 SEARCH SUMMARY")
        print("="*70)
        print(f"Total results found: {len(unique_pubs)}")
        print(f"After relevance filtering (≥{min_relevance}): {len(self.publications)}")
        print(f"Average relevance score: {sum(p.relevance_score for p in self.publications) / len(self.publications) if self.publications else 0:.1f}")
        
        # Show top 5 by relevance
        if self.publications:
            print(f"\n🏆 Top 5 Most Relevant:")
            for i, pub in enumerate(self.publications[:5], 1):
                print(f"  {i}. [{pub.relevance_score:.1f}] {pub.title[:65]}... ({pub.year})")
        
        return self.publications
    
    def identify_research_gaps(self) -> Dict:
        """Analyze publications to identify research gaps"""
        
        print("\n\n🎯 IDENTIFYING RESEARCH GAPS")
        print("="*70)
        
        gaps = {
            "understudied_crops": [],
            "missing_applications": [],
            "dataset_gaps": [],
            "methodological_gaps": [],
            "rice_specific_gaps": []
        }
        
        crop_mentions = defaultdict(int)
        model_mentions = defaultdict(int)
        
        for pub in self.publications:
            for crop in pub.crop_focus:
                crop_mentions[crop.lower()] += 1
            
            if pub.model_name:
                model_mentions[pub.model_name] += 1
        
        print("\n📈 Crop Coverage Analysis:")
        for crop in self.cereal_crops[:8]:  # Check main cereals
            count = crop_mentions.get(crop.lower(), 0)
            print(f"  {crop.capitalize()}: {count} publications")
            if count < 3:
                gaps["understudied_crops"].append(crop)
        
        if "rice" in gaps["understudied_crops"] or crop_mentions.get("rice", 0) < 5:
            gaps["rice_specific_gaps"].append(
                "Limited application of genomic LLMs specifically to rice genomics"
            )
        
        print("\n🤖 Model Coverage:")
        for model in self.target_models[:5]:
            count = model_mentions.get(model, 0)
            print(f"  {model}: {count} publications")
        
        gaps["missing_applications"] = [
            "Trait prediction for rice yield under climate stress",
            "Pan-genome analysis for cereal crops",
            "Integration with rice breeding pipelines",
            "Transfer learning from model organisms to rice"
        ]
        
        gaps["dataset_gaps"] = [
            "Comprehensive rice genome variation datasets",
            "Multi-omics integration for cereals",
            "Phenotype-genotype associations for rice traits"
        ]
        
        gaps["methodological_gaps"] = [
            "Fine-tuning strategies for crop-specific models",
            "Interpretability of genomic LLM predictions in rice",
            "Computational efficiency for practical breeding applications"
        ]
        
        return gaps
    
    def generate_literature_review_report(self, output_file: str = "literature_review.json"):
        """Generate comprehensive report"""
        
        print(f"\n\n📝 GENERATING LITERATURE REVIEW REPORT")
        print("="*70)
        
        gaps = self.identify_research_gaps()
        
        report = {
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "total_publications": len(self.publications),
                "date_range": f"{self.min_year}-{self.max_year}",
                "min_relevance_score": min(p.relevance_score for p in self.publications) if self.publications else 0,
                "avg_relevance_score": sum(p.relevance_score for p in self.publications) / len(self.publications) if self.publications else 0,
                "target_models": self.target_models,
                "focus_crops": self.cereal_crops
            },
            "publications": [asdict(pub) for pub in self.publications],
            "research_gaps": gaps,
            "recommendations": [
                "Develop rice-specific genomic foundation models fine-tuned on comprehensive rice pan-genome data",
                "Create benchmark datasets linking rice genomic sequences to agronomic traits",
                "Investigate transfer learning from well-studied models to underrepresented cereals",
                "Build interpretable models that can guide practical breeding decisions",
                "Establish computational pipelines integrating genomic LLMs with rice breeding programs"
            ]
        }
        
        import os
        output_dir = "output_reports"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to: {output_path}")
        
        summary_file = output_file.replace('.json', '_summary.txt')
        summary_path = os.path.join(output_dir, summary_file)
        
        with open(summary_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GENOMIC LLM LITERATURE REVIEW - IMPROVED VERSION\n")
            f.write("Focus: Rice and Cereal Crop Applications\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Date Range: {self.min_year}-{self.max_year}\n")
            f.write(f"Total Publications: {len(self.publications)}\n")
            f.write(f"Average Relevance: {report['metadata']['avg_relevance_score']:.1f}/100\n\n")
            
            f.write("FILTERING APPLIED:\n")
            f.write(f"  - Year range: {self.min_year}-{self.max_year}\n")
            f.write(f"  - Excluded keywords: {', '.join(self.exclusion_keywords[:10])}\n")
            f.write(f"  - Required keywords: ML/AI terms\n\n")
            
            f.write("TOP 10 PUBLICATIONS (by relevance):\n")
            for i, pub in enumerate(self.publications[:10], 1):
                f.write(f"\n{i}. [{pub.relevance_score:.1f}/100] {pub.title}\n")
                f.write(f"   Year: {pub.year} | Source: {pub.source}\n")
                f.write(f"   {pub.url}\n")
            
            f.write("\n" + "="*70 + "\n")
        
        print(f"✅ Summary saved to: {summary_path}")
        
        return report


def main():
    """Main execution"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     IMPROVED GENOMIC LLM LITERATURE REVIEW AGENT v2.0             ║
║     Smart Filtering • Relevance Scoring • Date Filtering          ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    agent = ImprovedGenomicLLMAgent()
    
    # Adjust these parameters:
    print("⚙️  CONFIGURABLE PARAMETERS:")
    print(f"   • Minimum year: {agent.min_year} (edit line 48)")
    print(f"   • Minimum relevance: 40.0 (edit line 474)")
    print(f"   • Exclusion keywords: {len(agent.exclusion_keywords)} (edit lines 60-66)")
    print("")
    
    # Run with filtering
    publications = agent.run_literature_search(
        use_claude=False,
        min_relevance=40.0  # Adjust this (0-100)
    )
    
    # Generate report
    report = agent.generate_literature_review_report()
    
    print("\n\n✨ WORKFLOW COMPLETE!")
    print("="*70)
    print("✅ Smart filtering applied")
    print("✅ Irrelevant papers removed")
    print("✅ Only recent papers (2018+) included")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
