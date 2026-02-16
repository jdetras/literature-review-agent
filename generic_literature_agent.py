#!/usr/bin/env python3
"""
GENERIC Literature Review Agent
Fully configurable via text files - works for ANY research domain
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional, Set
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
    relevance_score: float = 0.0
    model_name: Optional[str] = None
    topic_focus: List[str] = None
    key_findings: List[str] = None
    methodology: str = ""
    datasets_used: List[str] = None
    limitations: List[str] = None
    
    def __post_init__(self):
        if self.topic_focus is None:
            self.topic_focus = []
        if self.key_findings is None:
            self.key_findings = []
        if self.datasets_used is None:
            self.datasets_used = []
        if self.limitations is None:
            self.limitations = []


class ConfigLoader:
    """Load configuration from text files"""
    
    @staticmethod
    def load_list_file(filename: str, default: List[str] = None) -> List[str]:
        """Load a simple list file (one item per line, # for comments)"""
        if not os.path.exists(filename):
            print(f"⚠️  Config file not found: {filename}")
            return default or []
        
        items = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    items.append(line)
        
        return items
    
    @staticmethod
    def load_param_file(filename: str) -> Dict:
        """Load parameter file with key=value pairs and sections"""
        if not os.path.exists(filename):
            print(f"⚠️  Config file not found: {filename}")
            return {}
        
        config = {}
        current_section = None
        
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Section headers [section_name]
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    config[current_section] = []
                    continue
                
                # Key-value pairs
                if '=' in line and current_section is None:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Parse value type
                    if value.lower() == 'true':
                        config[key] = True
                    elif value.lower() == 'false':
                        config[key] = False
                    elif value == 'current':
                        config[key] = datetime.now().year
                    elif '.' in value:
                        try:
                            config[key] = float(value)
                        except ValueError:
                            config[key] = value
                    else:
                        try:
                            config[key] = int(value)
                        except ValueError:
                            config[key] = value
                
                # Section items
                elif current_section:
                    config[current_section].append(line)
        
        return config


class GenericLiteratureAgent:
    """Generic literature review agent - fully configurable"""
    
    def __init__(self, 
                 models_file: str = "config_models.txt",
                 topics_file: str = "config_topics.txt",
                 params_file: str = "config_search.txt",
                 anthropic_api_key: Optional[str] = None):
        """Initialize with configuration files"""
        
        print("\n" + "="*70)
        print("📚 GENERIC LITERATURE REVIEW AGENT")
        print("="*70)
        print("Loading configuration from files...")
        
        # Load configurations
        self.target_models = ConfigLoader.load_list_file(
            models_file, 
            default=["BERT", "Transformer", "GPT"]
        )
        print(f"✓ Loaded {len(self.target_models)} target models from {models_file}")
        
        self.target_topics = ConfigLoader.load_list_file(
            topics_file,
            default=["machine learning", "deep learning"]
        )
        print(f"✓ Loaded {len(self.target_topics)} target topics from {topics_file}")
        
        params = ConfigLoader.load_param_file(params_file)
        
        # Search parameters
        self.min_year = params.get('min_year', 2018)
        self.max_year = params.get('max_year', datetime.now().year)
        self.min_relevance = params.get('min_relevance', 40.0)
        self.max_results_per_query = params.get('max_results_per_query', 10)
        
        # Keywords
        self.required_keywords = params.get('required_keywords', [])
        self.exclusion_keywords = params.get('exclusion_keywords', [])
        self.boost_keywords = params.get('boost_keywords', [])
        
        # Adaptive settings
        self.adaptive_mode = params.get('adaptive_mode', True)
        self.auto_refine_queries = params.get('auto_refine_queries', True)
        self.learning_rate = params.get('learning_rate', 0.1)
        self.target_publications = params.get('target_publications_per_run', 30)
        
        # Custom queries
        self.custom_queries = params.get('custom_queries', [])
        
        print(f"✓ Loaded search parameters from {params_file}")
        print(f"  • Year range: {self.min_year}-{self.max_year}")
        print(f"  • Min relevance: {self.min_relevance}")
        print(f"  • Required keywords: {len(self.required_keywords)}")
        print(f"  • Exclusion keywords: {len(self.exclusion_keywords)}")
        print("="*70)
        
        self.anthropic_api_key = anthropic_api_key
        self.publications = []
    
    def calculate_relevance_score(self, title: str, abstract: str, year: int) -> float:
        """Calculate relevance score for a publication"""
        score = 0.0
        text = f"{title} {abstract}".lower()
        
        # 1. Year recency (0-20 points)
        current_year = datetime.now().year
        if year >= current_year - 1:
            score += 20
        elif year >= current_year - 3:
            score += 15
        elif year >= current_year - 5:
            score += 10
        elif year >= self.min_year:
            score += 5
        
        # 2. Required keywords (0-30 points)
        if self.required_keywords:
            required_found = sum(1 for kw in self.required_keywords if kw.lower() in text)
            score += min(required_found * 6, 30)
        else:
            score += 15  # If no required keywords, give base score
        
        # 3. Boost keywords (0-30 points)
        if self.boost_keywords:
            boost_found = sum(1 for kw in self.boost_keywords if kw.lower() in text)
            score += min(boost_found * 3, 30)
        else:
            score += 15  # If no boost keywords, give base score
        
        # 4. Target models (0-20 points)
        models_found = sum(1 for model in self.target_models if model.lower() in text)
        score += min(models_found * 10, 20)
        
        # 5. Penalties for exclusion keywords
        exclusions_found = sum(1 for kw in self.exclusion_keywords if kw.lower() in text)
        score -= exclusions_found * 15
        
        return max(0.0, min(100.0, score))
    
    def is_relevant(self, title: str, abstract: str, year: int, 
                   min_score: float = None) -> bool:
        """Determine if a publication is relevant"""
        if min_score is None:
            min_score = self.min_relevance
        
        # Year filter
        if year < self.min_year or year > self.max_year:
            return False
        
        text = f"{title} {abstract}".lower()
        
        # Exclusion filter (hard reject)
        for keyword in self.exclusion_keywords:
            if keyword.lower() in text:
                return False
        
        # Required keywords check (if specified)
        if self.required_keywords:
            has_required = any(kw.lower() in text for kw in self.required_keywords)
            if not has_required:
                return False
        
        # Relevance score check
        score = self.calculate_relevance_score(title, abstract, year)
        return score >= min_score
    
    def generate_queries(self) -> List[str]:
        """Generate search queries from configuration"""
        queries = set()
        
        # Use custom queries if provided
        if self.custom_queries:
            for query in self.custom_queries:
                # Expand placeholders
                if '{model}' in query or '{topic}' in query:
                    # Create combinations
                    for model in self.target_models[:5]:  # Top 5 models
                        q = query.replace('{model}', model)
                        queries.add(q)
                    for topic in self.target_topics[:5]:  # Top 5 topics
                        q = query.replace('{topic}', topic)
                        queries.add(q)
                else:
                    queries.add(query)
        else:
            # Auto-generate queries
            # Combine models with generic terms
            for model in self.target_models[:5]:
                queries.add(f"{model}")
                
            # Combine topics with ML terms
            for topic in self.target_topics[:5]:
                queries.add(f"{topic} machine learning")
                
            # Generic combinations
            if self.boost_keywords:
                for kw in self.boost_keywords[:3]:
                    queries.add(f"{kw} deep learning")
        
        return list(queries)
    
    def search_biorxiv(self, query: str, max_results: int = None) -> List[Publication]:
        """Search bioRxiv"""
        if max_results is None:
            max_results = self.max_results_per_query
        
        print(f"\n🔍 Searching bioRxiv for: {query}")
        publications = []
        
        try:
            search_url = f"https://www.biorxiv.org/search/{query}%20numresults%3A{max_results}%20sort%3Arelevance-rank"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; GenericLiteratureAgent/3.0; Research)'
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
                        
                        abstract = ""
                        abstract_elem = article.find('span', class_='highwire-cite-snippet')
                        if abstract_elem:
                            abstract = abstract_elem.text.strip()
                        
                        year = datetime.now().year
                        date_elem = article.find('span', class_='highwire-cite-metadata-date')
                        if date_elem:
                            date_text = date_elem.text
                            year_match = re.search(r'20\d{2}', date_text)
                            if year_match:
                                year = int(year_match.group())
                        
                        link = title_elem.find('a')
                        url = f"https://www.biorxiv.org{link['href']}" if link else ""
                        
                        if not self.is_relevant(title, abstract, year):
                            print(f"  ⊘ Filtered: {title[:60]}...")
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
                        print(f"  ✓ Found: {title[:60]}... (score: {score:.1f})")
                        
                    except Exception as e:
                        continue
                        
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        return publications
    
    def search_pubmed_central(self, query: str, max_results: int = None) -> List[Publication]:
        """Search PubMed Central"""
        if max_results is None:
            max_results = self.max_results_per_query
        
        print(f"\n🔍 Searching PubMed Central for: {query}")
        publications = []
        
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
            date_filter = f" AND {self.min_year}:{self.max_year}[pdat]"
            full_query = query + date_filter
            
            search_url = f"{base_url}/esearch.fcgi"
            params = {
                'db': 'pmc',
                'term': full_query,
                'retmax': max_results * 2,
                'retmode': 'json',
                'sort': 'relevance'
            }
            
            response = requests.get(search_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                id_list = data.get('esearchresult', {}).get('idlist', [])
                
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
                                
                                pubdate = article.get('pubdate', '')
                                year = datetime.now().year
                                year_match = re.search(r'20\d{2}', pubdate)
                                if year_match:
                                    year = int(year_match.group())
                                
                                abstract = ""
                                
                                if not self.is_relevant(title, abstract, year):
                                    print(f"  ⊘ Filtered: {title[:60]}...")
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
                                print(f"  ✓ Found: {title[:60]}... (score: {score:.1f})")
                                
                                if len(publications) >= max_results:
                                    break
                                    
                            except Exception as e:
                                continue
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        return publications
    
    def search_arxiv(self, query: str, max_results: int = None) -> List[Publication]:
        """Search arXiv"""
        if max_results is None:
            max_results = self.max_results_per_query
        
        print(f"\n🔍 Searching arXiv for: {query}")
        publications = []
        
        try:
            base_url = "http://export.arxiv.org/api/query"
            
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results * 2,
                'sortBy': 'relevance'
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')
                
                for entry in entries:
                    try:
                        title = entry.find('title').text.strip()
                        abstract = entry.find('summary').text.strip()
                        url = entry.find('id').text.strip()
                        published = entry.find('published').text.strip()
                        year = int(published[:4])
                        
                        authors = [author.find('name').text for author in entry.find_all('author')]
                        
                        if not self.is_relevant(title, abstract, year):
                            print(f"  ⊘ Filtered: {title[:60]}...")
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
                        print(f"  ✓ Found: {title[:60]}... (score: {score:.1f})")
                        
                        if len(publications) >= max_results:
                            break
                            
                    except Exception as e:
                        continue
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        return publications
    
    def run_literature_search(self) -> List[Publication]:
        """Execute comprehensive literature search"""
        
        print("\n" + "="*70)
        print("🔎 EXECUTING LITERATURE SEARCH")
        print("="*70)
        
        queries = self.generate_queries()
        print(f"\nGenerated {len(queries)} search queries")
        
        all_publications = []
        
        for query in queries[:15]:  # Limit to prevent too many requests
            pubs = self.search_biorxiv(query)
            all_publications.extend(pubs)
            
            pubs = self.search_pubmed_central(query)
            all_publications.extend(pubs)
            
            pubs = self.search_arxiv(query)
            all_publications.extend(pubs)
        
        # Deduplicate
        unique_pubs = {}
        for pub in all_publications:
            if pub.title and pub.title not in unique_pubs:
                unique_pubs[pub.title] = pub
        
        # Filter and sort
        self.publications = [
            pub for pub in unique_pubs.values()
            if pub.relevance_score >= self.min_relevance
        ]
        self.publications.sort(key=lambda x: x.relevance_score, reverse=True)
        
        print(f"\n" + "="*70)
        print(f"📊 SEARCH COMPLETE")
        print(f"="*70)
        print(f"Total found: {len(unique_pubs)}")
        print(f"After filtering: {len(self.publications)}")
        if self.publications:
            avg_score = sum(p.relevance_score for p in self.publications) / len(self.publications)
            print(f"Average relevance: {avg_score:.1f}/100")
            print(f"\n🏆 Top 5 by relevance:")
            for i, pub in enumerate(self.publications[:5], 1):
                print(f"  {i}. [{pub.relevance_score:.1f}] {pub.title[:65]}...")
        
        return self.publications
    
    def generate_report(self, output_file: str = "literature_review.json"):
        """Generate comprehensive report"""
        
        print(f"\n📝 Generating report...")
        
        report = {
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "total_publications": len(self.publications),
                "date_range": f"{self.min_year}-{self.max_year}",
                "min_relevance_score": min(p.relevance_score for p in self.publications) if self.publications else 0,
                "avg_relevance_score": sum(p.relevance_score for p in self.publications) / len(self.publications) if self.publications else 0,
                "target_models": self.target_models,
                "target_topics": self.target_topics,
                "config": {
                    "min_year": self.min_year,
                    "max_year": self.max_year,
                    "min_relevance": self.min_relevance,
                    "required_keywords": self.required_keywords[:10],
                    "exclusion_keywords": self.exclusion_keywords[:10]
                }
            },
            "publications": [asdict(pub) for pub in self.publications]
        }
        
        os.makedirs("output_reports", exist_ok=True)
        output_path = os.path.join("output_reports", output_file)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to: {output_path}")
        
        # Summary
        summary_file = output_file.replace('.json', '_summary.txt')
        summary_path = os.path.join("output_reports", summary_file)
        
        with open(summary_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GENERIC LITERATURE REVIEW - SUMMARY\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Date Range: {self.min_year}-{self.max_year}\n")
            f.write(f"Total Publications: {len(self.publications)}\n")
            f.write(f"Average Relevance: {report['metadata']['avg_relevance_score']:.1f}/100\n\n")
            
            f.write("TOP 10 PUBLICATIONS:\n")
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
║         GENERIC LITERATURE REVIEW AGENT v3.0                      ║
║         Fully Configurable via Text Files                         ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize agent (reads config files)
    agent = GenericLiteratureAgent(
        models_file="config_models.txt",
        topics_file="config_topics.txt",
        params_file="config_search.txt"
    )
    
    # Run search
    publications = agent.run_literature_search()
    
    # Generate report
    report = agent.generate_report()
    
    print("\n" + "="*70)
    print("✨ COMPLETE!")
    print("="*70)
    print("\n📄 To convert to web pages, run:")
    print("   python3 convert_to_github_pages.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
