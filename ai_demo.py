"""
AI-Enhanced ETL Parser Examples
Demonstrates all AI-powered features
"""
import os
from src.ai_enhanced_validator import AIEnhancedValidator


def check_ai_availability():
    """Check if AI features are configured"""
    print("="*80)
    print("Checking AI Availability")
    print("="*80)
    
    validator = AIEnhancedValidator()
    
    if validator.is_ai_available():
        print("✓ AI features are ENABLED")
        print(f"  Model: {os.getenv('AI_MODEL', 'gpt-4')}")
        print(f"  Temperature: {os.getenv('AI_TEMPERATURE', '0.3')}")
        return True
    else:
        print("✗ AI features are DISABLED")
        print("  To enable AI features:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key to .env")
        print("  3. Set ENABLE_AI_FEATURES=true")
        print("\n  All examples will show fallback behavior.")
        return False


def demo_transformation_suggestion():
    """Demo: AI transformation suggestions"""
    print("\n" + "="*80)
    print("DEMO 1: AI Transformation Suggestions")
    print("="*80)
    
    validator = AIEnhancedValidator()
    
    examples = [
        ('phone', 'contact_phone', 'VARCHAR', 'VARCHAR'),
        ('first_name', 'full_name', 'VARCHAR', 'VARCHAR'),
        ('order_date', 'order_year', 'DATE', 'INTEGER'),
        ('price_usd', 'price_eur', 'DECIMAL', 'DECIMAL'),
    ]
    
    for source, target, src_type, tgt_type in examples:
        print(f"\n📝 Suggesting transformation:")
        print(f"   {source} ({src_type}) → {target} ({tgt_type})")
        
        suggestion = validator.suggest_transformation(
            source, target, src_type, tgt_type
        )
        
        print(f"\n   Transformation: {suggestion['transformation']}")
        print(f"   Explanation: {suggestion['explanation']}")
        print(f"   Confidence: {suggestion['confidence']}")
        print(f"   AI Generated: {suggestion['ai_generated']}")


def demo_nl_to_mapping():
    """Demo: Natural language to mapping generation"""
    print("\n" + "="*80)
    print("DEMO 2: Natural Language to Mapping")
    print("="*80)
    
    validator = AIEnhancedValidator()
    
    description = """
    Map customer table where:
    - customer_id is the primary key
    - Combine first_name and last_name into full_name
    - Convert email to lowercase
    - Remove special characters from phone number
    - Map status: A=ACTIVE, I=INACTIVE
    """
    
    print(f"\n📝 Description:")
    print(description)
    print("\n🤖 Generating mapping...")
    
    mappings = validator.generate_from_description(description)
    
    if mappings:
        print(f"\n✓ Generated {len(mappings)} mappings:")
        print("\n" + "-"*80)
        print(f"{'Source':<20} {'Target':<20} {'Transformation':<40}")
        print("-"*80)
        for m in mappings:
            print(f"{m.get('source_column', ''):<20} {m.get('target_column', ''):<20} {m.get('transformation', ''):<40}")
    else:
        print("✗ No mappings generated (AI not available)")


def demo_quality_analysis():
    """Demo: Mapping quality analysis"""
    print("\n" + "="*80)
    print("DEMO 3: Mapping Quality Analysis")
    print("="*80)
    
    validator = AIEnhancedValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    print("\n🔍 Analyzing mapping quality...")
    
    analysis = validator.analyze_mapping_quality()
    
    print(f"\n📊 Quality Score: {analysis.get('quality_score', 'N/A')}")
    
    if 'issues' in analysis and analysis['issues']:
        print(f"\n⚠️  Issues Found ({len(analysis['issues'])}):")
        for issue in analysis['issues']:
            print(f"   • {issue}")
    
    if 'recommendations' in analysis and analysis['recommendations']:
        print(f"\n💡 Recommendations ({len(analysis['recommendations'])}):")
        for rec in analysis['recommendations']:
            print(f"   • {rec}")
    
    if 'strengths' in analysis and analysis['strengths']:
        print(f"\n✓ Strengths:")
        for strength in analysis['strengths']:
            print(f"   • {strength}")


def demo_query_optimization():
    """Demo: SQL query optimization"""
    print("\n" + "="*80)
    print("DEMO 4: SQL Query Optimization")
    print("="*80)
    
    validator = AIEnhancedValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    print("\n🔧 Generating and optimizing queries for PostgreSQL...")
    
    result = validator.generate_with_optimization(
        source_table='customers',
        target_table='dim_customer',
        database_type='postgres',
        query_type='source_minus_target'
    )
    
    print(f"\n✓ AI Available: {result['ai_available']}")
    
    if result['ai_available'] and 'optimization_notes' in result:
        notes = result['optimization_notes'].get('source_minus_target', {})
        
        if notes.get('suggestions'):
            print(f"\n💡 Optimization Suggestions:")
            for suggestion in notes['suggestions']:
                print(f"   • {suggestion}")
        
        if notes.get('improvements'):
            print(f"\n✨ Improvements Made:")
            for improvement in notes['improvements']:
                print(f"   • {improvement}")
        
        if notes.get('performance_notes'):
            print(f"\n⚡ Performance Notes:")
            print(f"   {notes['performance_notes']}")
    else:
        print("\n   (AI optimization not available - using base query)")


def demo_transformation_explanations():
    """Demo: Plain English explanations"""
    print("\n" + "="*80)
    print("DEMO 5: Transformation Explanations")
    print("="*80)
    
    validator = AIEnhancedValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    print("\n📖 Getting plain English explanations...")
    
    explanations = validator.explain_transformations()
    
    if explanations:
        print(f"\n✓ Generated {len(explanations)} explanations:\n")
        for target_col, explanation in list(explanations.items())[:5]:
            print(f"   {target_col}:")
            print(f"      {explanation}\n")
    else:
        print("   (AI explanations not available)")


def demo_syntax_validation():
    """Demo: Transformation syntax validation"""
    print("\n" + "="*80)
    print("DEMO 6: Syntax Validation")
    print("="*80)
    
    validator = AIEnhancedValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    print("\n🔍 Validating transformation syntax for PostgreSQL...")
    
    validations = validator.validate_transformation_syntax(database_type='postgres')
    
    if validations:
        print(f"\n✓ Validated {len(validations)} transformations:\n")
        
        for val in validations[:3]:  # Show first 3
            print(f"   {val.get('target_column', 'Unknown')}:")
            print(f"      Valid: {'✓' if val.get('valid') else '✗'}")
            
            if val.get('issues'):
                print(f"      Issues: {', '.join(val['issues'])}")
            
            if val.get('warnings'):
                print(f"      Warnings: {', '.join(val['warnings'])}")
            
            print()
    else:
        print("   (AI validation not available)")


def demo_comprehensive_analysis():
    """Demo: Complete AI analysis"""
    print("\n" + "="*80)
    print("DEMO 7: Comprehensive Analysis")
    print("="*80)
    
    validator = AIEnhancedValidator('examples/complex_mapping.csv')
    validator.load_mappings()
    
    print("\n🔬 Running comprehensive AI analysis...")
    
    analysis = validator.get_comprehensive_analysis(database_type='postgres')
    
    print(f"\n📊 Analysis Complete!")
    print(f"   AI Available: {analysis.get('ai_available', False)}")
    
    summary = analysis.get('mapping_summary', {})
    print(f"   Total Mappings: {summary.get('total_mappings', 0)}")
    print(f"   Source Columns: {len(summary.get('source_columns', []))}")
    print(f"   Target Columns: {len(summary.get('target_columns', []))}")
    
    if 'quality_analysis' in analysis:
        qa = analysis['quality_analysis']
        print(f"\n   Quality Score: {qa.get('quality_score', 'N/A')}")
        print(f"   Issues Found: {len(qa.get('issues', []))}")
        print(f"   Recommendations: {len(qa.get('recommendations', []))}")
    
    if 'syntax_validation' in analysis:
        sv = analysis['syntax_validation']
        valid_count = sum(1 for v in sv if v.get('valid', True))
        print(f"\n   Syntax Validation: {valid_count}/{len(sv)} valid")


def run_all_demos():
    """Run all AI feature demonstrations"""
    print("\n" + "🤖 AI-ENHANCED ETL PARSER - FEATURE DEMONSTRATIONS")
    print("="*80)
    
    # Check AI availability first
    ai_available = check_ai_availability()
    
    if not ai_available:
        print("\n⚠️  AI features are not configured.")
        print("   Demos will show fallback behavior without AI.")
        print("   To enable AI, configure your OpenAI API key in .env file.\n")
    
    demos = [
        demo_transformation_suggestion,
        demo_nl_to_mapping,
        demo_quality_analysis,
        demo_query_optimization,
        demo_transformation_explanations,
        demo_syntax_validation,
        demo_comprehensive_analysis
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n✗ Demo failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("🎉 All AI demonstrations completed!")
    print("="*80)
    
    if ai_available:
        print("\n💡 Try the web interface with AI features:")
    else:
        print("\n💡 Configure AI to unlock these features:")
        print("   1. Get API key from https://platform.openai.com")
        print("   2. Add to .env file: OPENAI_API_KEY=your-key")
        print("   3. Restart the application")
        print("\n   Then try the web interface:")
    
    print("   python app.py")
    print("   Open: http://localhost:5000")


if __name__ == '__main__':
    run_all_demos()
