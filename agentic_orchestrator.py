#!/usr/bin/env python3
"""
Agentic Literature Review Orchestrator
Autonomously manages search strategy, adapts to results, and self-improves
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
import time

from genomic_llm_literature_agent_v2 import ImprovedGenomicLLMAgent, Publication


class AgenticOrchestrator:
    """
    Autonomous agent that:
    1. Analyzes previous results
    2. Adjusts search strategy
    3. Identifies gaps
    4. Refines queries
    5. Self-improves over time
    """
    
    def __init__(self, config_file: str = "agent_config.json"):
        self.config_file = config_file
        self.config = self.load_or_create_config()
        self.history_file = "agent_history.json"
        self.history = self.load_history()
        self.agent = ImprovedGenomicLLMAgent()
    
    def load_or_create_config(self) -> Dict:
        """Load config or create default"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        # Default adaptive config
        return {
            "min_year": 2018,
            "min_relevance": 40.0,
            "max_results_per_query": 10,
            "adaptive_mode": True,
            "auto_refine_queries": True,
            "track_model_coverage": True,
            "track_crop_coverage": True,
            "learning_rate": 0.1,  # How much to adjust based on results
            "target_publications_per_run": 30
        }
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_history(self) -> List[Dict]:
        """Load previous run history"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Save run history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def analyze_previous_results(self) -> Dict:
        """Analyze trends from previous runs"""
        if not self.history:
            return {
                "first_run": True,
                "recommendations": ["Use default strategy"]
            }
        
        last_run = self.history[-1]
        analysis = {
            "first_run": False,
            "last_total": last_run.get('total_publications', 0),
            "last_avg_score": last_run.get('avg_relevance_score', 0),
            "recommendations": []
        }
        
        # Analyze trends
        if len(self.history) >= 2:
            prev_run = self.history[-2]
            
            # Declining results?
            if last_run['total_publications'] < prev_run['total_publications'] * 0.8:
                analysis['recommendations'].append("EXPAND_SEARCH")
                analysis['trend'] = 'declining'
            
            # Too many low-quality results?
            if last_run['avg_relevance_score'] < 45:
                analysis['recommendations'].append("INCREASE_STRICTNESS")
                analysis['quality'] = 'low'
            
            # Good balance?
            if 30 <= last_run['total_publications'] <= 50 and last_run['avg_relevance_score'] >= 50:
                analysis['recommendations'].append("MAINTAIN_STRATEGY")
                analysis['status'] = 'optimal'
        
        return analysis
    
    def identify_coverage_gaps(self, publications: List[Publication]) -> Dict:
        """Identify which models/crops need more coverage"""
        gaps = {
            "underrepresented_models": [],
            "underrepresented_crops": [],
            "suggested_queries": []
        }
        
        # Count coverage
        model_counts = defaultdict(int)
        crop_counts = defaultdict(int)
        
        for pub in publications:
            if pub.model_name:
                model_counts[pub.model_name] += 1
            for crop in pub.crop_focus:
                crop_counts[crop] += 1
        
        # Identify gaps
        for model in self.agent.target_models:
            if model_counts.get(model, 0) < 3:
                gaps["underrepresented_models"].append(model)
                gaps["suggested_queries"].append(f"{model} genomics plant")
        
        for crop in ["rice", "wheat", "maize", "barley"]:
            if crop_counts.get(crop, 0) < 5:
                gaps["underrepresented_crops"].append(crop)
                gaps["suggested_queries"].append(f"{crop} genome language model")
        
        return gaps
    
    def generate_adaptive_queries(self, analysis: Dict, gaps: Dict) -> List[str]:
        """Generate queries based on analysis and gaps"""
        queries = []
        
        # Base queries (always include)
        base_queries = [
            "genomic foundation model plant",
            "crop genome language model"
        ]
        queries.extend(base_queries)
        
        # Add gap-filling queries
        if self.config.get("auto_refine_queries", True):
            # Focus on underrepresented models
            for model in gaps.get("underrepresented_models", [])[:3]:
                queries.append(f"{model} transformer")
            
            # Focus on underrepresented crops
            for crop in gaps.get("underrepresented_crops", [])[:2]:
                queries.append(f"{crop} genomics neural network")
        
        # Adjust based on previous results
        if "EXPAND_SEARCH" in analysis.get("recommendations", []):
            # Add broader queries
            queries.extend([
                "plant genomics deep learning",
                "agricultural AI transformer",
                "crop breeding machine learning"
            ])
        
        if "INCREASE_STRICTNESS" in analysis.get("recommendations", []):
            # Add more specific queries
            queries.extend([
                "plant genome pre-trained model",
                "crop genomics BERT transformer"
            ])
        
        return list(set(queries))  # Remove duplicates
    
    def adjust_parameters(self, analysis: Dict):
        """Autonomously adjust search parameters"""
        if not self.config.get("adaptive_mode", True):
            return
        
        learning_rate = self.config.get("learning_rate", 0.1)
        
        # Adjust based on recommendations
        if "EXPAND_SEARCH" in analysis.get("recommendations", []):
            # Lower thresholds to get more results
            self.config["min_relevance"] = max(30.0, self.config["min_relevance"] - 5)
            self.config["max_results_per_query"] = min(20, self.config["max_results_per_query"] + 5)
            print(f"🔧 Expanding search: relevance→{self.config['min_relevance']}, results→{self.config['max_results_per_query']}")
        
        elif "INCREASE_STRICTNESS" in analysis.get("recommendations", []):
            # Raise thresholds for better quality
            self.config["min_relevance"] = min(60.0, self.config["min_relevance"] + 5)
            print(f"🔧 Increasing strictness: relevance→{self.config['min_relevance']}")
        
        elif "MAINTAIN_STRATEGY" in analysis.get("recommendations", []):
            print(f"✅ Strategy is optimal, maintaining current parameters")
        
        self.save_config()
    
    def run_autonomous_search(self) -> Dict:
        """Execute fully autonomous search with adaptation"""
        
        print("\n" + "="*70)
        print("🤖 AGENTIC LITERATURE REVIEW ORCHESTRATOR")
        print("="*70)
        print(f"Run #{len(self.history) + 1}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Step 1: Analyze previous results
        print("\n📊 STEP 1: Analyzing Previous Results")
        analysis = self.analyze_previous_results()
        
        if analysis.get("first_run"):
            print("  ℹ️ First run - using default strategy")
        else:
            print(f"  • Last run: {analysis['last_total']} publications")
            print(f"  • Average quality: {analysis['last_avg_score']:.1f}/100")
            print(f"  • Recommendations: {', '.join(analysis.get('recommendations', []))}")
        
        # Step 2: Adjust parameters
        print("\n⚙️ STEP 2: Adjusting Search Parameters")
        self.adjust_parameters(analysis)
        print(f"  • Min year: {self.config['min_year']}")
        print(f"  • Min relevance: {self.config['min_relevance']}")
        print(f"  • Results per query: {self.config['max_results_per_query']}")
        
        # Step 3: Load previous publications to identify gaps
        print("\n🔍 STEP 3: Identifying Coverage Gaps")
        previous_pubs = []
        if os.path.exists("output_reports/literature_review.json"):
            with open("output_reports/literature_review.json", 'r') as f:
                data = json.load(f)
                previous_pubs = [
                    Publication(**pub) for pub in data.get('publications', [])
                ]
        
        gaps = self.identify_coverage_gaps(previous_pubs)
        print(f"  • Underrepresented models: {', '.join(gaps['underrepresented_models'][:5]) or 'None'}")
        print(f"  • Underrepresented crops: {', '.join(gaps['underrepresented_crops'][:5]) or 'None'}")
        
        # Step 4: Generate adaptive queries
        print("\n🎯 STEP 4: Generating Adaptive Queries")
        queries = self.generate_adaptive_queries(analysis, gaps)
        print(f"  • Generated {len(queries)} queries")
        for i, q in enumerate(queries[:5], 1):
            print(f"    {i}. {q}")
        if len(queries) > 5:
            print(f"    ... and {len(queries) - 5} more")
        
        # Step 5: Execute search
        print("\n🔎 STEP 5: Executing Literature Search")
        self.agent.min_year = self.config['min_year']
        
        all_publications = []
        for query in queries:
            pubs = self.agent.search_biorxiv(query, max_results=self.config['max_results_per_query'])
            all_publications.extend(pubs)
            
            pubs = self.agent.search_pubmed_central(query, max_results=self.config['max_results_per_query'])
            all_publications.extend(pubs)
            
            pubs = self.agent.search_arxiv(query, max_results=self.config['max_results_per_query'])
            all_publications.extend(pubs)
        
        # Deduplicate and filter
        unique_pubs = {}
        for pub in all_publications:
            if pub.title and pub.title not in unique_pubs:
                unique_pubs[pub.title] = pub
        
        filtered_pubs = [
            pub for pub in unique_pubs.values()
            if pub.relevance_score >= self.config['min_relevance']
        ]
        
        filtered_pubs.sort(key=lambda x: x.relevance_score, reverse=True)
        
        self.agent.publications = filtered_pubs
        
        print(f"\n  ✅ Search complete: {len(filtered_pubs)} relevant publications")
        
        # Step 6: Generate report
        print("\n📝 STEP 6: Generating Report")
        report = self.agent.generate_literature_review_report()
        
        # Step 7: Record this run
        print("\n💾 STEP 7: Recording Run History")
        run_record = {
            "timestamp": datetime.now().isoformat(),
            "run_number": len(self.history) + 1,
            "total_publications": len(filtered_pubs),
            "avg_relevance_score": sum(p.relevance_score for p in filtered_pubs) / len(filtered_pubs) if filtered_pubs else 0,
            "config": self.config.copy(),
            "queries_used": queries,
            "gaps_identified": gaps,
            "recommendations": analysis.get("recommendations", [])
        }
        
        self.history.append(run_record)
        self.save_history()
        
        print(f"  ✅ Run #{run_record['run_number']} recorded")
        
        # Step 8: Self-assessment
        print("\n🎓 STEP 8: Self-Assessment")
        if run_record['total_publications'] >= self.config.get('target_publications_per_run', 30):
            print("  ✅ Target publication count achieved")
        else:
            print(f"  ⚠️ Below target ({run_record['total_publications']}/{self.config.get('target_publications_per_run', 30)})")
            print("  → Will adjust strategy for next run")
        
        if run_record['avg_relevance_score'] >= 50:
            print("  ✅ High quality results")
        else:
            print("  ⚠️ Quality could be improved")
            print("  → Will refine filters for next run")
        
        print("\n" + "="*70)
        print("✨ AUTONOMOUS RUN COMPLETE")
        print("="*70)
        print(f"Next scheduled run: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}")
        print("="*70)
        
        return run_record
    
    def generate_progress_report(self):
        """Generate a markdown report showing progress over time"""
        
        if not self.history:
            return
        
        report = []
        report.append("# Autonomous Literature Review Progress")
        report.append("")
        report.append(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}")
        report.append("")
        
        report.append("## 📈 Run History")
        report.append("")
        report.append("| Run | Date | Publications | Avg Quality | Strategy |")
        report.append("|-----|------|--------------|-------------|----------|")
        
        for run in self.history:
            date = datetime.fromisoformat(run['timestamp']).strftime('%Y-%m-%d')
            pubs = run['total_publications']
            quality = run['avg_relevance_score']
            strategy = ', '.join(run.get('recommendations', ['Default']))[:30]
            
            report.append(f"| {run['run_number']} | {date} | {pubs} | {quality:.1f} | {strategy} |")
        
        report.append("")
        report.append("## 🎯 Current Configuration")
        report.append("")
        report.append(f"- **Minimum Year:** {self.config['min_year']}")
        report.append(f"- **Minimum Relevance:** {self.config['min_relevance']}")
        report.append(f"- **Results Per Query:** {self.config['max_results_per_query']}")
        report.append(f"- **Adaptive Mode:** {self.config.get('adaptive_mode', True)}")
        report.append("")
        
        if len(self.history) >= 2:
            report.append("## 📊 Trends")
            report.append("")
            
            recent = self.history[-3:]
            total_trend = [r['total_publications'] for r in recent]
            quality_trend = [r['avg_relevance_score'] for r in recent]
            
            if len(total_trend) >= 2:
                if total_trend[-1] > total_trend[-2]:
                    report.append("- 📈 Publication count **increasing**")
                elif total_trend[-1] < total_trend[-2]:
                    report.append("- 📉 Publication count **decreasing**")
                else:
                    report.append("- ➡️ Publication count **stable**")
            
            if len(quality_trend) >= 2:
                if quality_trend[-1] > quality_trend[-2]:
                    report.append("- 📈 Quality score **improving**")
                elif quality_trend[-1] < quality_trend[-2]:
                    report.append("- 📉 Quality score **declining**")
                else:
                    report.append("- ➡️ Quality score **stable**")
        
        report.append("")
        report.append("---")
        report.append("*This report is automatically generated by the Agentic Orchestrator*")
        
        # Save report
        with open("AGENT_PROGRESS.md", 'w') as f:
            f.write("\n".join(report))
        
        print("✅ Progress report saved to AGENT_PROGRESS.md")


def main():
    """Run autonomous orchestrator"""
    
    orchestrator = AgenticOrchestrator()
    
    # Run autonomous search
    run_record = orchestrator.run_autonomous_search()
    
    # Generate progress report
    orchestrator.generate_progress_report()
    
    # Also run the web converter
    print("\n📄 Converting to GitHub Pages...")
    os.system("python3 convert_to_github_pages.py")
    
    print("\n" + "="*70)
    print("🎉 FULLY AUTONOMOUS RUN COMPLETE!")
    print("="*70)
    print("\nWhat happened:")
    print("  ✅ Analyzed previous results")
    print("  ✅ Adjusted search strategy automatically")
    print("  ✅ Identified coverage gaps")
    print("  ✅ Generated adaptive queries")
    print("  ✅ Executed search")
    print("  ✅ Generated reports")
    print("  ✅ Recorded history for learning")
    print("  ✅ Created web pages")
    print("\nNext run will:")
    print("  → Learn from this run's results")
    print("  → Further refine strategy")
    print("  → Fill identified gaps")
    print("="*70)


if __name__ == "__main__":
    main()
