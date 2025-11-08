#!/usr/bin/env python
# coding: utf-8

"""
Example usage of the Enhanced Ontology-Driven Stock Analysis System

This script demonstrates the key features and capabilities of the enhanced system.
"""

import asyncio
import json
from datetime import datetime
from enhanced_ontology_system import (
    EnhancedStockAnalysisEngine, 
    SystemConfig,
    config,
    log_step
)

async def main():
    """Main example function demonstrating system capabilities"""
    
    print("🚀 Enhanced Ontology-Driven Stock Analysis System - Example Usage")
    print("=" * 70)
    
    # Initialize the enhanced analysis engine
    print("\n1. Initializing Enhanced Analysis Engine...")
    engine = EnhancedStockAnalysisEngine(config)
    
    # Example 1: Basic Analysis
    print("\n2. Running Basic Analysis...")
    symbol = "AAPL"
    result = await engine.analyze_symbol(symbol, period="6mo", interval="1d")
    
    if "error" in result:
        print(f"❌ Analysis failed: {result['error']}")
        return
    
    print(f"✅ Analysis complete for {symbol}")
    print(f"   Overall Score: {result['overall_score']:.1%}")
    print(f"   Recommendation: {result['overall_recommendation'].upper()}")
    print(f"   Confidence: {result['confidence']:.1%}")
    
    # Example 2: Display Detailed Results
    print("\n3. Detailed Analysis Results:")
    print("-" * 40)
    
    # Market Context
    market_context = result.get("market_context", {})
    print(f"📊 Market State: {market_context.get('market_state', 'unknown').replace('_', ' ').title()}")
    print(f"📈 Trend Direction: {market_context.get('trend_direction', 'neutral').replace('_', ' ').title()}")
    print(f"📉 Volatility Regime: {market_context.get('volatility_regime', 'medium').replace('_', ' ').title()}")
    print(f"💹 Volume Profile: {market_context.get('volume_profile', 'neutral').replace('_', ' ').title()}")
    
    # Risk Assessment
    risk_assessment = result.get("risk_assessment", {})
    print(f"\n🛡️  Risk Assessment:")
    print(f"   Risk Score: {risk_assessment.get('risk_score', 0):.1%}")
    print(f"   Position Size: ${risk_assessment.get('position_size', 0):,.2f}")
    print(f"   Stop Loss: ${risk_assessment.get('stop_loss', 0):.2f}")
    print(f"   Take Profit: ${risk_assessment.get('take_profit', 0):.2f}")
    
    # ML Analysis
    ml_analysis = result.get("ml_analysis", {})
    print(f"\n🤖 Machine Learning Analysis:")
    print(f"   Prediction: {ml_analysis.get('prediction', 'neutral').title()}")
    print(f"   Confidence: {ml_analysis.get('confidence', 0):.1%}")
    print(f"   Anomaly Score: {ml_analysis.get('anomaly_score', 0):.3f}")
    
    # Pattern Analysis
    pattern_analysis = result.get("pattern_analysis", {})
    print(f"\n🔍 Pattern Detection:")
    print(f"   Patterns Detected: {pattern_analysis.get('patterns_detected', 0)}")
    print(f"   Pattern Recommendation: {pattern_analysis.get('pattern_recommendation', 'none').title()}")
    
    # Example 3: Support and Resistance Levels
    print(f"\n4. Key Trading Levels:")
    print("-" * 40)
    
    support_levels = market_context.get("support_levels", [])
    resistance_levels = market_context.get("resistance_levels", [])
    
    if support_levels:
        print("🟢 Support Levels:")
        for i, level in enumerate(support_levels[:3]):
            if level:
                print(f"   Level {i+1}: ${level:.2f}")
    
    if resistance_levels:
        print("🔴 Resistance Levels:")
        for i, level in enumerate(resistance_levels[:3]):
            if level:
                print(f"   Level {i+1}: ${level:.2f}")
    
    # Example 4: Risk Management Recommendations
    print(f"\n5. Risk Management Recommendations:")
    print("-" * 40)
    
    recommendations = risk_assessment.get("recommendations", [])
    for rec in recommendations[:5]:  # Show first 5 recommendations
        print(f"   • {rec}")
    
    # Example 5: Knowledge Graph Statistics
    print(f"\n6. Knowledge Graph Statistics:")
    print("-" * 40)
    
    knowledge_summary = result.get("knowledge_summary", {})
    print(f"   Total Statements: {knowledge_summary.get('total_statements', 0):,}")
    print(f"   Indicators: {knowledge_summary.get('indicators', 0)}")
    print(f"   ML Predictions: {knowledge_summary.get('ml_predictions', 0)}")
    print(f"   Risk Assessments: {knowledge_summary.get('risk_assessments', 0)}")
    print(f"   Contradictions: {knowledge_summary.get('contradictions', 0)}")
    print(f"   Confirmations: {knowledge_summary.get('confirmations', 0)}")
    
    # Example 6: Save Analysis Results
    print(f"\n7. Saving Analysis Results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_{symbol}_{timestamp}.json"
    
    # Save essential results
    essential_results = {
        "symbol": result["symbol"],
        "timestamp": result["timestamp"],
        "overall_score": result["overall_score"],
        "overall_recommendation": result["overall_recommendation"],
        "confidence": result["confidence"],
        "current_price": result["current_price"],
        "market_context": {
            "market_state": market_context.get("market_state"),
            "trend_direction": market_context.get("trend_direction"),
            "volatility_regime": market_context.get("volatility_regime")
        },
        "risk_assessment": {
            "risk_score": risk_assessment.get("risk_score"),
            "position_size": risk_assessment.get("position_size"),
            "stop_loss": risk_assessment.get("stop_loss"),
            "take_profit": risk_assessment.get("take_profit")
        },
        "ml_analysis": {
            "prediction": ml_analysis.get("prediction"),
            "confidence": ml_analysis.get("confidence")
        },
        "knowledge_summary": knowledge_summary
    }
    
    with open(filename, 'w') as f:
        json.dump(essential_results, f, indent=2)
    
    print(f"   ✅ Results saved to {filename}")
    
    # Example 7: Batch Analysis
    print(f"\n8. Running Batch Analysis...")
    symbols = ["GOOGL", "MSFT", "TSLA", "NVDA"]
    batch_results = {}
    
    for symbol in symbols:
        try:
            print(f"   Analyzing {symbol}...")
            result = await engine.analyze_symbol(symbol, "6mo", "1d")
            
            if "error" not in result:
                batch_results[symbol] = {
                    "overall_score": result["overall_score"],
                    "recommendation": result["overall_recommendation"],
                    "confidence": result["confidence"]
                }
                print(f"   ✅ {symbol}: {result['overall_recommendation'].upper()} ({result['overall_score']:.1%})")
            else:
                print(f"   ❌ {symbol}: {result['error']}")
                
        except Exception as e:
            print(f"   ❌ {symbol}: Error - {str(e)}")
    
    # Display batch results summary
    print(f"\n   Batch Analysis Summary:")
    print(f"   Analyzed: {len(batch_results)}/{len(symbols)} symbols")
    
    if batch_results:
        recommendations = [result["recommendation"] for result in batch_results.values()]
        recommendation_counts = {}
        for rec in recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        print(f"   Recommendations:")
        for rec, count in recommendation_counts.items():
            print(f"     {rec.upper()}: {count}")
    
    # Example 8: Custom Configuration
    print(f"\n9. Custom Configuration Example...")
    
    # Create custom configuration
    custom_config = SystemConfig(
        debug_mode=True,
        ml_enabled=True,
        real_time_enabled=False,
        max_position_size=0.15,  # 15% max position
        stop_loss_percentage=0.03,  # 3% stop loss
        take_profit_percentage=0.20  # 20% take profit
    )
    
    # Create engine with custom config
    custom_engine = EnhancedStockAnalysisEngine(custom_config)
    
    print(f"   ✅ Custom engine created with:")
    print(f"     - Debug mode: {custom_config.debug_mode}")
    print(f"     - ML enabled: {custom_config.ml_enabled}")
    print(f"     - Max position size: {custom_config.max_position_size:.1%}")
    print(f"     - Stop loss: {custom_config.stop_loss_percentage:.1%}")
    print(f"     - Take profit: {custom_config.take_profit_percentage:.1%}")
    
    print(f"\n" + "=" * 70)
    print(f"🎉 Example usage complete!")
    print(f"📊 The enhanced ontology system provides comprehensive analysis")
    print(f"🤖 with ML integration, risk management, and real-time capabilities.")
    print(f"🚀 Ready for production deployment with proper testing and validation.")

# Run the example
if __name__ == "__main__":
    asyncio.run(main())