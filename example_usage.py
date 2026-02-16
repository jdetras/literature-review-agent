#!/usr/bin/env python3
"""
Example Usage Scripts for Genomic LLM Literature Review Agent
Demonstrates various use cases and workflows
"""

import json
from genomic_llm_literature_agent import GenomicLLMAgent, Publication


def example_1_basic_search():
    """Example 1: Basic literature search without AI analysis"""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Literature Search")
    print("="*70)
    
    # Initialize agent
    agent = GenomicLLMAgent()
    
    # Run search
    publications = agent.run_literature_search(use_claude=False)
    
    # Generate report
    report = agent.generate_literature_review_report(
        output_file="basic_literature_review.json"
    )
    
    print(f"\n✅ Found {len(publications)} publications")
    print(f"✅ Report saved")


def example_2_search_with_claude():
    """Example 2: Enhanced search with Claude AI analysis"""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Search with Claude AI Analysis")
    print("="*70)
    
    # Set your API key here or via environment variable
    api_key = "your-anthropic-api-key-here"  # Replace with actual key
    
    if api_key == "your-anthropic-api-key-here":
        print("⚠️  Please set your Anthropic API key to run this example")
        return
    
    # Initialize agent with Claude
    agent = GenomicLLMAgent(anthropic_api_key=api_key)
    
    # Run search with AI analysis
    publications = agent.run_literature_search(use_claude=True)
    
    # Generate report
    report = agent.generate_literature_review_report(
        output_file="enhanced_literature_review.json"
    )
    
    print(f"\n✅ Analyzed {len(publications)} publications with Claude")


def example_3_targeted_search():
    """Example 3: Search specific model (AgroNT) for rice"""
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Targeted Search - AgroNT for Rice")
    print("="*70)
    
    agent = GenomicLLMAgent()
    
    # Search specific sources
    print("\nSearching bioRxiv...")
    biorxiv_pubs = agent.search_biorxiv("AgroNT rice genome", max_results=15)
    
    print("\nSearching PubMed Central...")
    pmc_pubs = agent.search_pubmed_central("AgroNT Oryza sativa", max_results=15)
    
    print("\nSearching arXiv...")
    arxiv_pubs = agent.search_arxiv("AgroNT transformer agriculture", max_results=15)
    
    # Combine results
    agent.publications = biorxiv_pubs + pmc_pubs + arxiv_pubs
    
    # Remove duplicates
    unique_pubs = {pub.title: pub for pub in agent.publications if pub.title}
    agent.publications = list(unique_pubs.values())
    
    print(f"\n✅ Found {len(agent.publications)} unique publications on AgroNT & Rice")
    
    # Generate report
    agent.generate_literature_review_report(
        output_file="agront_rice_review.json"
    )


def example_4_custom_analysis():
    """Example 4: Custom gap analysis for specific crops"""
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Gap Analysis for Wheat & Barley")
    print("="*70)
    
    agent = GenomicLLMAgent()
    
    # Customize crops of interest
    agent.cereal_crops = ["wheat", "barley", "Triticum", "Hordeum"]
    
    # Run search
    publications = agent.run_literature_search(use_claude=False)
    
    # Custom gap analysis
    gaps = agent.identify_research_gaps()
    
    print("\n📊 Custom Gap Analysis Results:")
    print(f"  Wheat coverage: {sum(1 for p in publications if 'wheat' in str(p.crop_focus).lower())} papers")
    print(f"  Barley coverage: {sum(1 for p in publications if 'barley' in str(p.crop_focus).lower())} papers")
    
    # Generate report
    agent.generate_literature_review_report(
        output_file="wheat_barley_review.json"
    )


def example_5_load_and_analyze():
    """Example 5: Load existing report and perform additional analysis"""
    
    print("\n" + "="*70)
    print("EXAMPLE 5: Load & Analyze Existing Report")
    print("="*70)
    
    # Load existing report
    try:
        with open('/mnt/user-data/outputs/literature_review.json', 'r') as f:
            report = json.load(f)
        
        pubs = report['publications']
        
        print(f"\n📚 Loaded {len(pubs)} publications")
        
        # Analyze by year
        year_counts = {}
        for pub in pubs:
            year = pub.get('year', 'Unknown')
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print("\n📅 Publications by Year:")
        for year in sorted(year_counts.keys(), reverse=True):
            print(f"  {year}: {year_counts[year]} publications")
        
        # Analyze by model
        model_counts = {}
        for pub in pubs:
            model = pub.get('model_name', 'Unknown')
            if model and model != 'Unknown':
                model_counts[model] = model_counts.get(model, 0) + 1
        
        print("\n🤖 Publications by Model:")
        for model, count in sorted(model_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: {count} publications")
        
        # Analyze crops
        crop_mentions = {}
        for pub in pubs:
            crops = pub.get('crop_focus', [])
            for crop in crops:
                crop_mentions[crop] = crop_mentions.get(crop, 0) + 1
        
        print("\n🌾 Crop Mentions:")
        for crop, count in sorted(crop_mentions.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {crop}: {count} mentions")
        
    except FileNotFoundError:
        print("❌ No existing report found. Run a search first!")


def example_6_comparative_analysis():
    """Example 6: Compare models across different crops"""
    
    print("\n" + "="*70)
    print("EXAMPLE 6: Comparative Model Analysis")
    print("="*70)
    
    agent = GenomicLLMAgent()
    
    # Define models to compare
    models_to_compare = ["AgroNT", "DNABERT", "Nucleotide Transformer"]
    
    results = {}
    
    for model in models_to_compare:
        print(f"\n🔍 Searching for {model}...")
        
        # Search each source
        pubs = []
        pubs.extend(agent.search_biorxiv(f"{model} plant", max_results=10))
        pubs.extend(agent.search_pubmed_central(f"{model} genomics", max_results=10))
        pubs.extend(agent.search_arxiv(f"{model} sequence", max_results=10))
        
        # Remove duplicates
        unique = {p.title: p for p in pubs if p.title}
        
        results[model] = {
            'count': len(unique),
            'publications': list(unique.values())
        }
        
        print(f"  ✓ Found {len(unique)} publications")
    
    # Compare results
    print("\n📊 Comparative Analysis:")
    for model, data in results.items():
        print(f"\n{model}:")
        print(f"  Total publications: {data['count']}")
        
        # Analyze crop focus
        crop_counts = {}
        for pub in data['publications']:
            for crop in agent.cereal_crops:
                # Simple text search in title/abstract
                text = f"{pub.title} {pub.abstract}".lower()
                if crop.lower() in text:
                    crop_counts[crop] = crop_counts.get(crop, 0) + 1
        
        if crop_counts:
            print(f"  Crop coverage:")
            for crop, count in sorted(crop_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {crop}: {count}")
        else:
            print(f"  Crop coverage: Limited data")
    
    # Save comparison
    comparison_report = {
        'models_compared': models_to_compare,
        'results': results,
        'generated': str(datetime.now())
    }
    
    output_path = "/mnt/user-data/outputs/model_comparison.json"
    with open(output_path, 'w') as f:
        json.dump(comparison_report, f, indent=2, default=str)
    
    print(f"\n✅ Comparison report saved to {output_path}")


def example_7_rice_specific_analysis():
    """Example 7: Deep dive into rice genomics literature"""
    
    print("\n" + "="*70)
    print("EXAMPLE 7: Rice-Specific Deep Dive")
    print("="*70)
    
    agent = GenomicLLMAgent()
    
    # Focus exclusively on rice
    rice_queries = [
        "genomic language model rice",
        "transformer Oryza sativa",
        "foundation model rice genome",
        "deep learning rice breeding",
        "machine learning rice trait prediction",
        "neural network rice pan-genome"
    ]
    
    all_pubs = []
    
    for query in rice_queries:
        print(f"\n🔍 Searching: {query}")
        pubs = agent.search_biorxiv(query, max_results=10)
        pubs.extend(agent.search_pubmed_central(query, max_results=10))
        all_pubs.extend(pubs)
    
    # Remove duplicates
    unique_pubs = {p.title: p for p in all_pubs if p.title}
    agent.publications = list(unique_pubs.values())
    
    print(f"\n✅ Found {len(agent.publications)} unique rice genomics publications")
    
    # Rice-specific gap analysis
    print("\n🌾 Rice-Specific Research Gaps:")
    
    rice_gaps = {
        "breeding_applications": [
            "Integration with molecular breeding programs",
            "Trait prediction for climate resilience",
            "Yield optimization under stress conditions"
        ],
        "genomic_resources": [
            "Pan-genome representation learning",
            "Rare variety genomic coverage",
            "Multi-omics data integration"
        ],
        "practical_deployment": [
            "Computational efficiency for field use",
            "Farmer-accessible tools",
            "Real-time variety recommendation"
        ]
    }
    
    for category, gaps in rice_gaps.items():
        print(f"\n  {category.replace('_', ' ').title()}:")
        for gap in gaps:
            print(f"    - {gap}")
    
    # Generate rice-specific report
    agent.generate_literature_review_report(
        output_file="rice_genomics_review.json"
    )


def main():
    """Run selected examples"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║              EXAMPLE USAGE SCRIPTS                                 ║
║     Genomic LLM Literature Review Agent                            ║
╚═══════════════════════════════════════════════════════════════════╝

Available Examples:
1. Basic literature search (no AI)
2. Enhanced search with Claude AI analysis
3. Targeted search for AgroNT & Rice
4. Custom gap analysis for Wheat & Barley
5. Load and analyze existing report
6. Comparative model analysis
7. Rice-specific deep dive

Enter example number (1-7) or 'all' to run all examples:
""")
    
    choice = input().strip()
    
    if choice == '1':
        example_1_basic_search()
    elif choice == '2':
        example_2_search_with_claude()
    elif choice == '3':
        example_3_targeted_search()
    elif choice == '4':
        example_4_custom_analysis()
    elif choice == '5':
        example_5_load_and_analyze()
    elif choice == '6':
        example_6_comparative_analysis()
    elif choice == '7':
        example_7_rice_specific_analysis()
    elif choice.lower() == 'all':
        example_1_basic_search()
        example_3_targeted_search()
        example_4_custom_analysis()
        example_5_load_and_analyze()
        example_6_comparative_analysis()
        example_7_rice_specific_analysis()
        print("\n⚠️  Skipping Example 2 (requires API key)")
    else:
        print("Invalid choice. Please run again and select 1-7 or 'all'")


if __name__ == "__main__":
    from datetime import datetime
    main()
