#!/usr/bin/env python3
"""
Literature Review to GitHub Pages Converter
Converts JSON literature review output to HTML and Markdown for GitHub Pages
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class LiteratureReviewConverter:
    """Convert JSON literature review to HTML/Markdown for GitHub Pages"""
    
    def __init__(self, json_file: str):
        """Initialize with JSON file path"""
        self.json_file = json_file
        self.data = self.load_json()
    
    def load_json(self) -> Dict:
        """Load the JSON literature review file"""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Could not find {self.json_file}")
            print("Make sure you've run the literature agent first!")
            exit(1)
    
    def generate_markdown(self) -> str:
        """Generate Markdown content"""
        
        md = []
        
        # Header
        md.append("# Genomic LLM Literature Review")
        md.append("## Research Gaps for Rice and Cereal Crops")
        md.append("")
        
        # Metadata
        meta = self.data.get('metadata', {})
        md.append("---")
        md.append("")
        md.append(f"**Generated:** {meta.get('generated_date', 'N/A')[:10]}")
        md.append(f"**Total Publications:** {meta.get('total_publications', 0)}")
        md.append("")
        md.append("---")
        md.append("")
        
        # Table of Contents
        md.append("## 📚 Table of Contents")
        md.append("")
        md.append("- [Overview](#overview)")
        md.append("- [Target Models](#target-models)")
        md.append("- [Research Gaps](#research-gaps)")
        md.append("  - [Understudied Crops](#understudied-crops)")
        md.append("  - [Missing Applications](#missing-applications)")
        md.append("  - [Dataset Gaps](#dataset-gaps)")
        md.append("  - [Methodological Gaps](#methodological-gaps)")
        md.append("  - [Rice-Specific Gaps](#rice-specific-gaps)")
        md.append("- [Publications](#publications)")
        md.append("- [Recommendations](#recommendations)")
        md.append("")
        md.append("---")
        md.append("")
        
        # Overview
        md.append("## 🎯 Overview")
        md.append("")
        md.append("This literature review analyzes the current state of genomic language models (LLMs) ")
        md.append("and their application to plant genomics, with a specific focus on identifying ")
        md.append("research opportunities for rice and other cereal crops.")
        md.append("")
        
        # Target Models
        md.append("## 🤖 Target Models")
        md.append("")
        target_models = meta.get('target_models', [])
        if target_models:
            for i, model in enumerate(target_models, 1):
                md.append(f"{i}. **{model}**")
        md.append("")
        
        # Research Gaps
        md.append("## 🔍 Research Gaps")
        md.append("")
        
        gaps = self.data.get('research_gaps', {})
        
        # Understudied Crops
        md.append("### 🌾 Understudied Crops")
        md.append("")
        understudied = gaps.get('understudied_crops', [])
        if understudied:
            md.append("The following cereal crops have limited coverage in genomic LLM research:")
            md.append("")
            for crop in understudied:
                md.append(f"- **{crop.capitalize()}**")
            md.append("")
        else:
            md.append("*All target crops have adequate coverage.*")
            md.append("")
        
        # Missing Applications
        md.append("### 🎯 Missing Applications")
        md.append("")
        applications = gaps.get('missing_applications', [])
        if applications:
            md.append("Key application areas that need more research:")
            md.append("")
            for app in applications:
                md.append(f"- {app}")
            md.append("")
        
        # Dataset Gaps
        md.append("### 📊 Dataset Gaps")
        md.append("")
        dataset_gaps = gaps.get('dataset_gaps', [])
        if dataset_gaps:
            md.append("Missing or insufficient datasets:")
            md.append("")
            for gap in dataset_gaps:
                md.append(f"- {gap}")
            md.append("")
        
        # Methodological Gaps
        md.append("### 🔬 Methodological Gaps")
        md.append("")
        method_gaps = gaps.get('methodological_gaps', [])
        if method_gaps:
            md.append("Technical and methodological challenges:")
            md.append("")
            for gap in method_gaps:
                md.append(f"- {gap}")
            md.append("")
        
        # Rice-Specific Gaps
        md.append("### 🍚 Rice-Specific Gaps")
        md.append("")
        rice_gaps = gaps.get('rice_specific_gaps', [])
        if rice_gaps:
            md.append("Opportunities specific to rice genomics:")
            md.append("")
            for gap in rice_gaps:
                md.append(f"- {gap}")
            md.append("")
        else:
            md.append("*No specific rice gaps identified. This may indicate good coverage or need for deeper analysis.*")
            md.append("")
        
        # Publications
        md.append("## 📖 Publications")
        md.append("")
        
        publications = self.data.get('publications', [])
        
        if publications:
            md.append(f"**Total Publications Found:** {len(publications)}")
            md.append("")
            
            # Group by year
            pubs_by_year = {}
            for pub in publications:
                year = pub.get('year', 'Unknown')
                if year not in pubs_by_year:
                    pubs_by_year[year] = []
                pubs_by_year[year].append(pub)
            
            for year in sorted(pubs_by_year.keys(), reverse=True):
                md.append(f"### {year}")
                md.append("")
                
                for pub in pubs_by_year[year]:
                    title = pub.get('title', 'Untitled')
                    url = pub.get('url', '#')
                    source = pub.get('source', 'Unknown')
                    
                    md.append(f"#### [{title}]({url})")
                    md.append("")
                    
                    # Authors
                    authors = pub.get('authors', [])
                    if authors:
                        md.append(f"**Authors:** {', '.join(authors[:5])}")
                        if len(authors) > 5:
                            md.append(f" *et al.*")
                        md.append("")
                    
                    md.append(f"**Source:** {source}")
                    md.append("")
                    
                    # Model name (if analyzed)
                    model_name = pub.get('model_name', '')
                    if model_name:
                        md.append(f"**Model:** {model_name}")
                        md.append("")
                    
                    # Crop focus (if analyzed)
                    crop_focus = pub.get('crop_focus', [])
                    if crop_focus:
                        md.append(f"**Crops:** {', '.join(crop_focus)}")
                        md.append("")
                    
                    # Key findings (if analyzed)
                    key_findings = pub.get('key_findings', [])
                    if key_findings:
                        md.append("**Key Findings:**")
                        for finding in key_findings:
                            md.append(f"- {finding}")
                        md.append("")
                    
                    # Abstract (truncated)
                    abstract = pub.get('abstract', '')
                    if abstract:
                        truncated = abstract[:300] + "..." if len(abstract) > 300 else abstract
                        md.append(f"**Abstract:** {truncated}")
                        md.append("")
                    
                    md.append("---")
                    md.append("")
        else:
            md.append("*No publications found. Run the literature agent first.*")
            md.append("")
        
        # Recommendations
        md.append("## 💡 Recommendations")
        md.append("")
        
        recommendations = self.data.get('recommendations', [])
        if recommendations:
            md.append("Based on the identified gaps, we recommend:")
            md.append("")
            for i, rec in enumerate(recommendations, 1):
                md.append(f"{i}. {rec}")
            md.append("")
        
        # Footer
        md.append("---")
        md.append("")
        md.append("*This literature review was generated using an AI agent for genomic LLM research analysis.*")
        md.append("")
        md.append(f"*Last updated: {datetime.now().strftime('%B %d, %Y')}*")
        
        return "\n".join(md)
    
    def generate_html(self) -> str:
        """Generate HTML content with Bootstrap styling"""
        
        html = []
        
        # HTML Header
        html.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genomic LLM Literature Review</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px 0;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: 20px;
            margin-bottom: 40px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }
        h2 {
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 5px solid #3498db;
            padding-left: 15px;
        }
        h3 {
            color: #5a6c7d;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        .badge-model {
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            margin: 3px;
            display: inline-block;
        }
        .badge-crop {
            background: #27ae60;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            margin: 3px;
            display: inline-block;
        }
        .gap-item {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .publication-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #3498db;
            transition: transform 0.2s;
        }
        .publication-card:hover {
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }
        .recommendation {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .toc {
            background: #e9ecef;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .toc a {
            color: #3498db;
            text-decoration: none;
            display: block;
            padding: 5px 0;
        }
        .toc a:hover {
            color: #2980b9;
            text-decoration: underline;
        }
    </style>
</head>
<body>""")
        
        meta = self.data.get('metadata', {})
        
        # Container start
        html.append('<div class="container">')
        
        # Title
        html.append('<h1><i class="bi bi-book"></i> Genomic LLM Literature Review</h1>')
        html.append('<p class="lead">Research Gaps for Rice and Cereal Crops</p>')
        
        # Stats
        html.append('<div class="row mt-4">')
        html.append('  <div class="col-md-4">')
        html.append('    <div class="stat-box">')
        html.append(f'      <span class="stat-number">{meta.get("total_publications", 0)}</span>')
        html.append('      <span>Publications Analyzed</span>')
        html.append('    </div>')
        html.append('  </div>')
        
        gaps = self.data.get('research_gaps', {})
        total_gaps = sum(len(v) for v in gaps.values() if isinstance(v, list))
        
        html.append('  <div class="col-md-4">')
        html.append('    <div class="stat-box">')
        html.append(f'      <span class="stat-number">{total_gaps}</span>')
        html.append('      <span>Research Gaps Identified</span>')
        html.append('    </div>')
        html.append('  </div>')
        
        html.append('  <div class="col-md-4">')
        html.append('    <div class="stat-box">')
        html.append(f'      <span class="stat-number">{len(meta.get("target_models", []))}</span>')
        html.append('      <span>Models Reviewed</span>')
        html.append('    </div>')
        html.append('  </div>')
        html.append('</div>')
        
        # Table of Contents
        html.append('<div class="toc mt-4">')
        html.append('  <h4><i class="bi bi-list-ul"></i> Table of Contents</h4>')
        html.append('  <a href="#overview">Overview</a>')
        html.append('  <a href="#models">Target Models</a>')
        html.append('  <a href="#gaps">Research Gaps</a>')
        html.append('  <a href="#publications">Publications</a>')
        html.append('  <a href="#recommendations">Recommendations</a>')
        html.append('</div>')
        
        # Overview
        html.append('<h2 id="overview"><i class="bi bi-info-circle"></i> Overview</h2>')
        html.append('<p>This literature review analyzes the current state of genomic language models (LLMs) ')
        html.append('and their application to plant genomics, with a specific focus on identifying ')
        html.append('research opportunities for rice and other cereal crops.</p>')
        
        # Target Models
        html.append('<h2 id="models"><i class="bi bi-cpu"></i> Target Models</h2>')
        html.append('<div class="mt-3">')
        for model in meta.get('target_models', []):
            html.append(f'  <span class="badge-model">{model}</span>')
        html.append('</div>')
        
        # Research Gaps
        html.append('<h2 id="gaps"><i class="bi bi-search"></i> Research Gaps</h2>')
        
        # Understudied Crops
        html.append('<h3><i class="bi bi-seedling"></i> Understudied Crops</h3>')
        understudied = gaps.get('understudied_crops', [])
        if understudied:
            for crop in understudied:
                html.append(f'<div class="gap-item"><strong>{crop.capitalize()}</strong> - Limited genomic LLM research coverage</div>')
        else:
            html.append('<p><em>All target crops have adequate coverage.</em></p>')
        
        # Missing Applications
        html.append('<h3><i class="bi bi-lightbulb"></i> Missing Applications</h3>')
        applications = gaps.get('missing_applications', [])
        if applications:
            html.append('<ul>')
            for app in applications:
                html.append(f'  <li>{app}</li>')
            html.append('</ul>')
        
        # Dataset Gaps
        html.append('<h3><i class="bi bi-database"></i> Dataset Gaps</h3>')
        dataset_gaps = gaps.get('dataset_gaps', [])
        if dataset_gaps:
            html.append('<ul>')
            for gap in dataset_gaps:
                html.append(f'  <li>{gap}</li>')
            html.append('</ul>')
        
        # Methodological Gaps
        html.append('<h3><i class="bi bi-gear"></i> Methodological Gaps</h3>')
        method_gaps = gaps.get('methodological_gaps', [])
        if method_gaps:
            html.append('<ul>')
            for gap in method_gaps:
                html.append(f'  <li>{gap}</li>')
            html.append('</ul>')
        
        # Rice-Specific Gaps
        html.append('<h3><i class="bi bi-star"></i> Rice-Specific Gaps</h3>')
        rice_gaps = gaps.get('rice_specific_gaps', [])
        if rice_gaps:
            html.append('<ul>')
            for gap in rice_gaps:
                html.append(f'  <li>{gap}</li>')
            html.append('</ul>')
        else:
            html.append('<p><em>No specific rice gaps identified.</em></p>')
        
        # Publications
        html.append('<h2 id="publications"><i class="bi bi-journal"></i> Publications</h2>')
        
        publications = self.data.get('publications', [])
        
        if publications:
            # Group by year
            pubs_by_year = {}
            for pub in publications:
                year = pub.get('year', 'Unknown')
                if year not in pubs_by_year:
                    pubs_by_year[year] = []
                pubs_by_year[year].append(pub)
            
            for year in sorted(pubs_by_year.keys(), reverse=True):
                html.append(f'<h3>{year}</h3>')
                
                for pub in pubs_by_year[year]:
                    html.append('<div class="publication-card">')
                    
                    title = pub.get('title', 'Untitled')
                    url = pub.get('url', '#')
                    source = pub.get('source', 'Unknown')
                    
                    html.append(f'  <h4><a href="{url}" target="_blank">{title}</a></h4>')
                    
                    # Authors
                    authors = pub.get('authors', [])
                    if authors:
                        author_str = ', '.join(authors[:5])
                        if len(authors) > 5:
                            author_str += ' <em>et al.</em>'
                        html.append(f'  <p><strong>Authors:</strong> {author_str}</p>')
                    
                    html.append(f'  <p><strong>Source:</strong> {source}</p>')
                    
                    # Model and crops
                    model_name = pub.get('model_name', '')
                    crop_focus = pub.get('crop_focus', [])
                    
                    if model_name or crop_focus:
                        html.append('  <div class="mt-2">')
                        if model_name:
                            html.append(f'    <span class="badge-model">{model_name}</span>')
                        for crop in crop_focus:
                            html.append(f'    <span class="badge-crop">{crop}</span>')
                        html.append('  </div>')
                    
                    # Key findings
                    key_findings = pub.get('key_findings', [])
                    if key_findings:
                        html.append('  <div class="mt-3">')
                        html.append('    <strong>Key Findings:</strong>')
                        html.append('    <ul>')
                        for finding in key_findings:
                            html.append(f'      <li>{finding}</li>')
                        html.append('    </ul>')
                        html.append('  </div>')
                    
                    html.append('</div>')
        
        # Recommendations
        html.append('<h2 id="recommendations"><i class="bi bi-check2-circle"></i> Recommendations</h2>')
        
        recommendations = self.data.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                html.append(f'<div class="recommendation"><strong>{i}.</strong> {rec}</div>')
        
        # Footer
        html.append('<hr class="mt-5">')
        html.append(f'<p class="text-muted text-center"><em>Generated: {datetime.now().strftime("%B %d, %Y")}</em></p>')
        
        # Close container and body
        html.append('</div>')
        html.append('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>')
        html.append('</body>')
        html.append('</html>')
        
        return "\n".join(html)
    
    def save_markdown(self, output_file: str = "index.md"):
        """Save markdown to file"""
        content = self.generate_markdown()
        
        # Create output directory
        output_dir = "github_pages"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Markdown saved to: {output_path}")
        return output_path
    
    def save_html(self, output_file: str = "index.html"):
        """Save HTML to file"""
        content = self.generate_html()
        
        # Create output directory
        output_dir = "github_pages"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML saved to: {output_path}")
        return output_path
    
    def convert_all(self):
        """Convert to both Markdown and HTML"""
        print("\n" + "="*70)
        print("📄 CONVERTING LITERATURE REVIEW TO GITHUB PAGES")
        print("="*70)
        print(f"\nInput: {self.json_file}")
        print(f"Publications: {self.data.get('metadata', {}).get('total_publications', 0)}")
        print("\n" + "="*70)
        
        md_path = self.save_markdown()
        html_path = self.save_html()
        
        print("\n" + "="*70)
        print("✨ CONVERSION COMPLETE!")
        print("="*70)
        print("\n📁 Output files in 'github_pages/' directory:")
        print(f"  • {md_path}")
        print(f"  • {html_path}")
        print("\n🚀 To publish on GitHub Pages:")
        print("  1. Create a new GitHub repository")
        print("  2. Upload files from 'github_pages/' folder")
        print("  3. Go to Settings > Pages")
        print("  4. Set source to 'main' branch")
        print("  5. Choose 'index.html' or 'index.md' as source")
        print("\n" + "="*70)


def main():
    """Main execution"""
    
    import sys
    
    # Get JSON file path
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # Default to the standard output location
        json_file = "output_reports/literature_review.json"
    
    # Check if file exists
    if not os.path.exists(json_file):
        print(f"\n❌ Error: File not found: {json_file}")
        print("\nUsage:")
        print(f"  python3 {sys.argv[0]} [path/to/literature_review.json]")
        print("\nDefault path: output_reports/literature_review.json")
        print("\nMake sure you've run the genomic_llm_literature_agent.py first!")
        sys.exit(1)
    
    # Convert
    converter = LiteratureReviewConverter(json_file)
    converter.convert_all()


if __name__ == "__main__":
    main()
