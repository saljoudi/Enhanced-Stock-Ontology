# Continuing the enhanced ontology system...
            
            # Generate recommendation
            if len(patterns) > 0:
                bullish_patterns = [p for p in patterns if "bullish" in p.get("type", "")]
                bearish_patterns = [p for p in patterns if "bearish" in p.get("type", "")]
                
                if len(bullish_patterns) > len(bearish_patterns):
                    pattern_results["pattern_recommendation"] = "bullish"
                elif len(bearish_patterns) > len(bullish_patterns):
                    pattern_results["pattern_recommendation"] = "bearish"
                else:
                    pattern_results["pattern_recommendation"] = "neutral"
            
            log_step(f"Pattern analysis complete for {symbol}: {len(patterns)} patterns detected")
            
        except Exception as e:
            log_step(f"Pattern analysis failed for {symbol}: {e}", "ERROR")
        
        return pattern_results
    
    def _detect_basic_patterns(self, prices: np.ndarray) -> List[Dict[str, Any]]:
        """Detect basic chart patterns"""
        patterns = []
        
        # Simple moving average crossover detection
        sma_short = pd.Series(prices).rolling(20).mean()
        sma_long = pd.Series(prices).rolling(50).mean()
        
        if len(prices) >= 50:
            # Golden Cross (bullish)
            if sma_short.iloc[-1] > sma_long.iloc[-1] and sma_short.iloc[-2] <= sma_long.iloc[-2]:
                patterns.append({
                    "type": "golden_cross",
                    "direction": "bullish",
                    "confidence": 0.8,
                    "description": "Golden Cross - Short MA crosses above Long MA"
                })
            
            # Death Cross (bearish)
            if sma_short.iloc[-1] < sma_long.iloc[-1] and sma_short.iloc[-2] >= sma_long.iloc[-2]:
                patterns.append({
                    "type": "death_cross",
                    "direction": "bearish", 
                    "confidence": 0.8,
                    "description": "Death Cross - Short MA crosses below Long MA"
                })
        
        return patterns
    
    async def _anomaly_analysis(self, symbol: str, features: np.ndarray) -> Dict[str, Any]:
        """Perform anomaly detection analysis"""
        anomaly_results = {
            "is_anomaly": False,
            "anomaly_score": 0.0,
            "anomaly_type": "none",
            "confidence": 0.0
        }
        
        try:
            if self.config.ml_enabled and self.anomaly_detector.is_fitted:
                anomaly_score = self.anomaly_detector.detect_anomalies(features)
                
                anomaly_results.update({
                    "is_anomaly": anomaly_score[0] == -1,
                    "anomaly_score": abs(anomaly_score[0]),
                    "anomaly_type": "price_anomaly" if anomaly_score[0] == -1 else "normal",
                    "confidence": 0.9 if anomaly_score[0] == -1 else 0.1
                })
            
            log_step(f"Anomaly analysis complete for {symbol}: {'Anomaly detected' if anomaly_results['is_anomaly'] else 'Normal'}")
            
        except Exception as e:
            log_step(f"Anomaly analysis failed for {symbol}: {e}", "ERROR")
        
        return anomaly_results
    
    def _generate_comprehensive_report(self, symbol: str, ontology_results: Dict[str, Any],
                                     ml_results: Dict[str, Any], risk_results: Dict[str, Any],
                                     pattern_results: Dict[str, Any], anomaly_results: Dict[str, Any],
                                     df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        
        report = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_context": ontology_results,
            "ml_analysis": ml_results,
            "risk_assessment": risk_results,
            "pattern_analysis": pattern_results,
            "anomaly_detection": anomaly_results,
            "current_price": df["close"].iloc[-1],
            "price_change_24h": ((df["close"].iloc[-1] / df["close"].iloc[-2]) - 1) * 100 if len(df) > 1 else 0,
            "volume_24h": df["volume"].iloc[-1] if "volume" in df.columns else 0,
            "market_cap": df["close"].iloc[-1] * df["volume"].iloc[-1] if "volume" in df.columns else 0,
            "overall_score": 0.0,
            "overall_recommendation": "hold",
            "confidence": ontology_results.get("confidence_score", 0.5),
            "ontology_graph": self.ontology.serialize(),
            "knowledge_summary": self.ontology.get_knowledge_summary()
        }
        
        # Calculate overall score
        ontology_score = ontology_results.get("confidence_score", 0) * 0.4
        ml_score = ml_results.get("confidence", 0) * 0.3
        risk_score = (1 - risk_results.get("risk_score", 0.5)) * 0.2  # Inverse risk
        pattern_score = pattern_results.get("pattern_confidence", 0) * 0.1
        
        report["overall_score"] = ontology_score + ml_score + risk_score + pattern_score
        
        # Generate overall recommendation
        if report["overall_score"] > 0.7:
            report["overall_recommendation"] = "strong_buy"
        elif report["overall_score"] > 0.5:
            report["overall_recommendation"] = "buy"
        elif report["overall_score"] < 0.3:
            report["overall_recommendation"] = "strong_sell"
        elif report["overall_score"] < 0.5:
            report["overall_recommendation"] = "sell"
        else:
            report["overall_recommendation"] = "hold"
        
        # Add detailed analysis sections
        report["detailed_analysis"] = {
            "technical_summary": self._generate_technical_summary(ontology_results),
            "ml_summary": self._generate_ml_summary(ml_results),
            "risk_summary": self._generate_risk_summary(risk_results),
            "pattern_summary": self._generate_pattern_summary(pattern_results),
            "anomaly_summary": self._generate_anomaly_summary(anomaly_results)
        }
        
        return report
    
    def _generate_technical_summary(self, ontology_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis summary"""
        return {
            "market_state": ontology_results.get("market_state", "unknown"),
            "trend_direction": ontology_results.get("trend_direction", "neutral"),
            "confidence": ontology_results.get("confidence_score", 0),
            "key_levels": {
                "support": ontology_results.get("support_levels", [])[:2],
                "resistance": ontology_results.get("resistance_levels", [])[:2]
            },
            "volatility": ontology_results.get("volatility_regime", "medium"),
            "volume_profile": ontology_results.get("volume_profile", "neutral")
        }
    
    def _generate_ml_summary(self, ml_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ML analysis summary"""
        return {
            "prediction": ml_results.get("prediction", "neutral"),
            "confidence": ml_results.get("confidence", 0),
            "recommendation": ml_results.get("recommendation", "hold"),
            "anomaly_score": ml_results.get("anomaly_score", 0)
        }
    
    def _generate_risk_summary(self, risk_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk analysis summary"""
        return {
            "risk_score": risk_results.get("risk_score", 0.5),
            "risk_factors": risk_results.get("risk_factors", []),
            "position_size": risk_results.get("position_size", 0),
            "stop_loss": risk_results.get("stop_loss", 0),
            "take_profit": risk_results.get("take_profit", 0)
        }
    
    def _generate_pattern_summary(self, pattern_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pattern analysis summary"""
        return {
            "patterns_detected": len(pattern_results.get("patterns_detected", [])),
            "pattern_recommendation": pattern_results.get("pattern_recommendation", "none"),
            "pattern_confidence": pattern_results.get("pattern_confidence", 0)
        }
    
    def _generate_anomaly_summary(self, anomaly_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate anomaly analysis summary"""
        return {
            "is_anomaly": anomaly_results.get("is_anomaly", False),
            "anomaly_score": anomaly_results.get("anomaly_score", 0),
            "anomaly_type": anomaly_results.get("anomaly_type", "none")
        }
    
    def _cache_results(self, symbol: str, report: Dict[str, Any]):
        """Cache analysis results"""
        cache_key = f"analysis_{symbol}"
        self.cache[cache_key] = {
            "report": report,
            "timestamp": datetime.now(),
            "expiry": datetime.now() + timedelta(minutes=15)  # Cache for 15 minutes
        }
    
    def _error_result(self, symbol: str, error: str) -> Dict[str, Any]:
        """Generate error result"""
        return {
            "symbol": symbol,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "overall_recommendation": "error",
            "overall_score": 0.0
        }
    
    # Signal classification helper methods
    def _classify_ma_signal(self, current: float, ma_value: float, threshold: float = 0.02) -> Tuple[str, float]:
        """Classify price vs moving average relationship"""
        deviation = (current - ma_value) / ma_value
        if deviation > threshold:
            return "strong_above", min(deviation * 2, 1.0)
        elif deviation > 0:
            return "above", deviation * 1.5
        elif deviation < -threshold:
            return "strong_below", min(abs(deviation) * 2, 1.0)
        else:
            return "below", abs(deviation) * 1.5
    
    def _classify_adx(self, value: float) -> Tuple[str, float]:
        """Classify ADX strength"""
        if value > 40:
            return "very_strong", 0.95
        elif value > 25:
            return "strong", 0.8
        elif value > 20:
            return "moderate", 0.6
        return "weak", 0.4
    
    def _classify_rsi(self, value: float) -> Tuple[str, float]:
        """Classify RSI signal"""
        if value > 80:
            return "extremely_overbought", 0.95
        elif value > 70:
            return "overbought", 0.8
        elif value < 20:
            return "extremely_oversold", 0.95
        elif value < 30:
            return "oversold", 0.8
        return "neutral", 0.5
    
    def _classify_macd(self, macd: float, signal: float, hist: float) -> Tuple[str, float]:
        """Classify MACD signal"""
        if macd > signal and macd > 0:
            strength = "strong_" if abs(hist) > 0.02 else ""
            return f"{strength}bullish", 0.85 if "strong" in strength else 0.6
        elif macd < signal and macd < 0:
            strength = "strong_" if abs(hist) > 0.02 else ""
            return f"{strength}bearish", 0.85 if "strong" in strength else 0.6
        return "neutral", 0.4
    
    def _classify_stochastic(self, k: float, d: float) -> Tuple[str, float]:
        """Classify Stochastic signal"""
        if k > 80 and d > 80:
            return "overbought", 0.8
        elif k < 20 and d < 20:
            return "oversold", 0.8
        elif k > d and k < 50:
            return "bullish_cross", 0.7
        elif k < d and k > 50:
            return "bearish_cross", 0.7
        return "neutral", 0.5
    
    def _classify_mfi(self, value: float) -> Tuple[str, float]:
        """Classify MFI signal (similar to RSI)"""
        return self._classify_rsi(value)
    
    def _classify_cci(self, value: float) -> Tuple[str, float]:
        """Classify CCI signal"""
        if value > 100:
            return "overbought", 0.7
        elif value < -100:
            return "oversold", 0.7
        return "neutral", 0.5
    
    def _infer_market_state(self, extracts: Dict[str, Any]) -> Tuple[str, float]:
        """Infer market state from weighted evidence"""
        scores = {
            "bull_trend": 0.0,
            "bear_trend": 0.0,
            "sideways_consolidation": 0.0,
            "volatile_breakout": 0.0,
            "range_bound": 0.0
        }
        confidences = {
            "bull_trend": [],
            "bear_trend": [],
            "sideways_consolidation": [],
            "volatile_breakout": [],
            "range_bound": []
        }
        
        # Trend evidence
        t = extracts.get("trend", {})
        if t.get("strength") in ["strong", "very_strong"]:
            if "bullish" in t.get("di_signal", ""):
                scores["bull_trend"] += 0.3
                confidences["bull_trend"].append(t.get("avg_confidence", 0.5))
            else:
                scores["bear_trend"] += 0.3
                confidences["bear_trend"].append(t.get("avg_confidence", 0.5))
        
        # Momentum evidence
        m = extracts.get("momentum", {})
        bullish_mom = sum(1 for s in m.get("signals", []) if "bullish" in s)
        bearish_mom = sum(1 for s in m.get("signals", []) if "bearish" in s)
        
        if bullish_mom >= 2:
            scores["bull_trend"] += 0.25
            confidences["bull_trend"].append(m.get("avg_confidence", 0.5))
        elif bearish_mom >= 2:
            scores["bear_trend"] += 0.25
            confidences["bear_trend"].append(m.get("avg_confidence", 0.5))
        
        # Volume evidence
        v = extracts.get("volume", {})
        if "strong_accumulation" in v.get("profile", ""):
            scores["bull_trend"] += 0.2 * 1.5
            confidences["bull_trend"].append(v.get("confidence", 0.5))
        elif "distribution" in v.get("profile", ""):
            scores["bear_trend"] += 0.2
            confidences["bear_trend"].append(v.get("confidence", 0.5))
        
        # Volatility regime
        vol = extracts.get("volatility", {})
        if vol.get("regime") == "high":
            scores["volatile_breakout"] += 0.15
            confidences["volatile_breakout"].append(vol.get("confidence", 0.5))
        elif vol.get("regime") == "low" and max(scores.values()) < 0.3:
            scores["range_bound"] += 0.15
            confidences["range_bound"].append(vol.get("confidence", 0.5))
        
        # Select winning state
        winning_state = max(scores.items(), key=lambda x: x[1])[0] if scores else "sideways_consolidation"
        avg_conf = sum(confidences.get(winning_state, [0.5])) / max(len(confidences.get(winning_state, [])), 1)
        
        return winning_state, avg_conf
    
    def _infer_trend_direction(self, extracts: Dict[str, Any]) -> Tuple[str, float]:
        """Infer trend direction from multiple factors"""
        bullish_score = 0.0
        total_conf = 0.0
        
        # Trend indicators
        t = extracts.get("trend", {})
        if t.get("strength") == "very_strong":
            bullish_score += 2.0
            total_conf += t.get("avg_confidence", 0.5)
        elif t.get("strength") == "strong":
            bullish_score += 1.5
            total_conf += t.get("avg_confidence", 0.5)
        
        # Momentum
        m = extracts.get("momentum", {})
        bullish_mom = sum(1 for s in m.get("signals", []) if "bullish" in s)
        bullish_score += bullish_mom * 0.8
        total_conf += m.get("avg_confidence", 0.5)
        
        # Ichimoku
        ich = extracts.get("structure", {})
        if len(ich.get("signals", [])) >= 2:
            bullish_ich = sum(1 for s in ich["signals"] if "bullish" in s)
            bullish_score += bullish_ich * 0.6
        
        # Volume confirmation
        v = extracts.get("volume", {})
        if "accumulation" in v.get("profile", ""):
            bullish_score += 0.5
        
        # Determine direction
        if bullish_score >= 3.0:
            direction = "strong_up"
        elif bullish_score >= 1.5:
            direction = "moderate_up"
        elif bullish_score <= -3.0:
            direction = "strong_down"
        elif bullish_score <= -1.5:
            direction = "moderate_down"
        else:
            direction = "neutral"
        
        avg_conf = total_conf / 3 if total_conf > 0 else 0.5
        return direction, avg_conf
    
    def _infer_risk_level(self, extracts: Dict[str, Any]) -> Tuple[str, float]:
        """Infer risk level from multiple dimensions"""
        risk_score = 0.0
        confidences = []
        
        # Volatility risk (primary factor)
        vol = extracts.get("volatility", {})
        if vol.get("regime") == "high":
            risk_score += 4.0
            confidences.append(vol.get("confidence", 0.5))
        elif vol.get("regime") == "medium":
            risk_score += 2.0
            confidences.append(vol.get("confidence", 0.5))
        
        # Trend risk (counter-trend increases risk)
        t = extracts.get("trend", {})
        if t.get("strength") == "weak":
            risk_score += 1.0
            confidences.append(0.6)
        
        # Momentum exhaustion risk
        m = extracts.get("momentum", {})
        signals = m.get("signals", [])
        if any("overbought" in s or "oversold" in s for s in signals):
            risk_score += 1.5
            confidences.append(0.7)
        
        # Map to RiskLevel
        if risk_score >= 4.5:
            level = "very_high"
        elif risk_score >= 3.5:
            level = "high"
        elif risk_score >= 2.5:
            level = "medium"
        elif risk_score >= 1.5:
            level = "low"
        else:
            level = "very_low"
        
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.5
        return level, avg_conf
    
    def _build_reasoning_chain(self, symbol: str, extracts: Dict[str, Any],
                             market_state: str, trend_direction: str,
                             risk_level: str, confidence: float) -> List[str]:
        """Generate dynamic reasoning trace"""
        chain = [
            f"Comprehensive Analysis for {symbol} at {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Overall Confidence: {confidence:.1%}",
            f"Market State: {market_state.replace('_', ' ').title()}",
            f"Trend Direction: {trend_direction.replace('_', ' ').title()}",
            f"Risk Level: {risk_level.replace('_', ' ').title()}"
        ]
        
        # Add top evidence
        top_evidence = []
        for category, data in extracts.items():
            if category != "ml_features" and isinstance(data, dict):
                if data.get("avg_confidence", 0) > 0.7:
                    top_evidence.append(f"- {category.title()}: High confidence signals")
        
        if top_evidence:
            chain.append("Key Evidence:")
            chain.extend(top_evidence)
        
        # Add contradictions
        contradictions = self.ontology.detect_contradictions()
        if contradictions:
            chain.append(f"⚠️ Detected {len(contradictions)} indicator contradictions")
        
        # Add confirmations
        confirmations = self.ontology.find_confirmations()
        if confirmations:
            chain.append(f"✅ Found {len(confirmations)} strong indicator confirmations")
        
        return chain

# Initialize the enhanced analysis engine
enhanced_engine = EnhancedStockAnalysisEngine(config)

# Export the main components for use in other modules
__all__ = [
    'EnhancedStockAnalysisEngine',
    'EnhancedStockOntologyGraph',
    'PatternRecognitionModel',
    'AdvancedRiskManager',
    'RealTimeDataStreamer',
    'SystemConfig',
    'config',
    'enhanced_engine'
]