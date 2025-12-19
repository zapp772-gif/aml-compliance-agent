"""
AI Analysis module using Venice AI API with automatic regulation category detection
"""

import os
import requests
from dotenv import load_dotenv
import re

load_dotenv()

class ComplianceAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('VENICE_API_KEY')
        self.api_url = "https://api.venice.ai/api/v1/chat/completions"
        
        # Category detection keywords
        self.category_keywords = {
            "BSA": ["bank secrecy act", "bsa", "31 cfr", "title 31"],
            "PATRIOT": ["patriot act", "usa patriot", "title iii"],
            "CDD": ["customer due diligence", "cdd", "beneficial ownership"],
            "CIP": ["customer identification", "cip", "customer verification", "identity verification"],
            "SAR": ["suspicious activity report", "sar", "suspicious transaction"],
            "CTR": ["currency transaction report", "ctr", "cash transaction", "$10,000"],
            "RECORDKEEPING": ["recordkeeping", "record retention", "record keeping"],
            "SANCTIONS": ["sanctions", "ofac", "sdn", "specially designated", "blocked property"],
            "DIGITAL_ASSETS": ["cryptocurrency", "crypto", "digital asset", "virtual currency", "bitcoin", "blockchain"]
        }
        
        self.system_prompt = """You are an expert AML/BSA Compliance Officer with 20+ years of experience advising large financial institutions like Morgan Stanley, JP Morgan Chase, and Bank of America.

Your analysis must be FACTUAL ONLY - no speculation, opinions, or assumptions. Base all analysis strictly on the regulatory text provided.

Core Focus Areas:
- Bank Secrecy Act (BSA) of 1970
- USA PATRIOT Act (Title III)
- Title 31 CFR Chapter X (Treasury regulations implementing BSA/AML)

Key Requirements & Reporting:
- Customer Due Diligence (CDD) & Know Your Customer (KYC)
- Customer Identification Program (CIP)
- Suspicious Activity Reports (SARs) - filing thresholds, timeframes (30-60 days)
- Currency Transaction Reports (CTRs) - $10,000+ cash transactions
- Recordkeeping requirements
- OFAC Sanctions Compliance - SDN list screening, blocked property reporting
- Digital Asset/Cryptocurrency regulations

Analysis Framework:
1. REGULATORY SUMMARY: Factual description of what changed (2-3 sentences)
2. COMPLIANCE IMPACTS: Specific, measurable impacts on large financial institutions' AML/BSA programs
3. ACTIONABLE RECOMMENDATIONS: Concrete steps institutions must take to comply

Rules:
- State only verifiable facts from the regulatory update
- Do not speculate on potential future impacts
- Do not provide general opinions
- Reference specific regulations, sections, or requirements when applicable
- Recommendations must be specific and actionable, not general guidance"""
    
    def detect_categories(self, text):
        """Detect relevant regulation categories from text"""
        detected = []
        text_lower = text.lower()
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if category not in detected:
                        detected.append(category)
                    break
        
        return detected if detected else ["GENERAL"]
    
    def analyze_update(self, update_text, regulator_name, regulation_type):
        """Analyze a regulatory update using AI"""
        
        # Detect categories from title and summary
        full_text = f"{update_text.get('title', '')} {update_text.get('summary', '')}"
        detected_categories = self.detect_categories(full_text)
        
        user_prompt = f"""Analyze this regulatory update from {regulator_name}:

TITLE: {update_text.get('title', 'N/A')}
TYPE: {regulation_type}
DETECTED CATEGORIES: {', '.join(detected_categories)}
CONTENT: {update_text.get('summary', 'N/A')}
SOURCE: {update_text.get('link', 'N/A')}

Provide analysis in this exact format:

REGULATORY SUMMARY:
[2-3 sentences describing exactly what this regulatory update changes or announces. Be factual and specific. Cite regulation numbers/sections if mentioned.]

APPLICABLE COMPLIANCE AREAS:
[List which of these areas are directly affected: BSA, PATRIOT Act, CDD/KYC, CIP, SAR Filing, CTR Reporting, Recordkeeping, OFAC Sanctions, Digital Assets]

COMPLIANCE IMPACTS FOR LARGE FINANCIAL INSTITUTIONS:
[List 3-5 specific, measurable impacts. Each must state:
 - What specific compliance requirement is affected
 - How it affects Morgan Stanley/JP Morgan/Bank of America type institutions
 - Which BSA/AML program areas are impacted]

Example format:
- CIP Requirements: [specific change] affecting customer onboarding processes
- SAR Filing: [specific change] impacting reporting thresholds or timeframes
- OFAC Screening: [specific change] to sanctions screening protocols

ACTIONABLE RECOMMENDATIONS:
[List 3-5 concrete steps large institutions should take. Each must be:
 - Specific and implementable
 - Tied directly to the regulatory change
 - Relevant to enterprise-scale AML/BSA programs]

Example format:
- Update CIP procedures to incorporate [specific requirement] by [deadline if stated]
- Revise SAR filing workflows to ensure [specific compliance action]
- Implement enhanced OFAC screening for [specific transaction types]

Remember: Facts only. No speculation. Reference specific BSA/AML requirements."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 1500
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            return {
                'update': update_text,
                'analysis': analysis,
                'regulator': regulator_name,
                'regulation_type': regulation_type,
                'categories': detected_categories
            }
            
        except Exception as e:
            print(f"Error analyzing update from {regulator_name}: {str(e)}")
            return {
                'update': update_text,
                'analysis': f"Analysis unavailable: {str(e)}",
                'regulator': regulator_name,
                'regulation_type': regulation_type,
                'categories': detected_categories
            }
    
    def batch_analyze(self, updates_by_regulator):
        """Analyze multiple updates from multiple regulators"""
        analyzed_results = []
        
        for regulator, data in updates_by_regulator.items():
            updates = data['updates']
            reg_type = data['type']
            
            print(f"  Analyzing {len(updates[:3])} updates from {regulator}...")
            
            for update in updates[:3]:
                analysis = self.analyze_update(update, regulator, reg_type)
                analyzed_results.append(analysis)
        
        return analyzed_results
