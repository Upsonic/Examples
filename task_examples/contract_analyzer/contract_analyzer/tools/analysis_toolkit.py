import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from upsonic.tools import ToolKit, tool


class PartyInfo(BaseModel):
    """Information about a party in a contract."""
    name: str = Field(description="Name of the party")
    role: str = Field(description="Role in the contract (e.g., 'Provider', 'Client', 'Landlord', 'Tenant')")
    type: str = Field(description="Type of entity (e.g., 'Corporation', 'Individual', 'LLC')")


class DateInfo(BaseModel):
    """Date information extracted from a contract."""
    date_type: str = Field(description="Type of date (e.g., 'Effective Date', 'Termination Date', 'Renewal Date')")
    date_value: str = Field(description="The date value")
    description: Optional[str] = Field(default=None, description="Additional context about the date")


class FinancialTerm(BaseModel):
    """Financial term extracted from a contract."""
    term_type: str = Field(description="Type of financial term (e.g., 'Payment', 'Fee', 'Penalty')")
    amount: str = Field(description="The monetary amount or calculation method")
    frequency: Optional[str] = Field(default=None, description="Payment frequency if applicable")
    conditions: Optional[str] = Field(default=None, description="Conditions attached to this term")


class Obligation(BaseModel):
    """An obligation identified in the contract."""
    party: str = Field(description="The party responsible for this obligation")
    description: str = Field(description="Description of the obligation")
    deadline: Optional[str] = Field(default=None, description="Deadline if specified")
    category: str = Field(description="Category (e.g., 'Delivery', 'Payment', 'Confidentiality')")


class RiskClause(BaseModel):
    """A potentially risky clause identified in the contract."""
    clause_type: str = Field(description="Type of clause (e.g., 'Indemnification', 'Limitation of Liability')")
    risk_level: str = Field(description="Risk level: 'Low', 'Medium', 'High'")
    description: str = Field(description="Description of the risk")
    recommendation: str = Field(description="Recommended action or consideration")
    original_text: Optional[str] = Field(default=None, description="The original clause text if identifiable")


class ContractAnalyzerToolKit(ToolKit):
    """
    A toolkit for comprehensive contract analysis.
    
    Provides specialized tools for extracting structured information from 
    legal contracts including parties, dates, financial terms, obligations,
    and risk assessment.
    """
    
    def __init__(self) -> None:
        """Initialize the Contract Analyzer ToolKit."""
        super().__init__()
    
    @tool
    def extract_parties(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract all parties involved in the contract.
        
        Identifies and categorizes all parties mentioned in the contract,
        including their roles and entity types.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A dictionary containing:
                - parties: List of party information with name, role, and type
                - total_count: Number of parties identified
                - primary_parties: The main parties to the agreement
        """
        party_patterns = [
            r'(?:between|among)\s+([^(]+?)\s*\(["\']?(\w+)["\']?\)',
            r'(?:hereinafter|referred to as)\s*["\'](\w+)["\']',
            r'"([^"]+)"\s*(?:as|hereinafter referred to as)\s*["\']?(\w+)',
        ]
        
        parties: List[Dict[str, str]] = []
        
        for pattern in party_patterns:
            matches = re.findall(pattern, contract_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    name = match[0].strip()
                    role = match[1].strip()
                    
                    entity_type = "Unknown"
                    if any(term in name.upper() for term in ["CORP", "INC", "LLC", "LTD", "COMPANY"]):
                        entity_type = "Corporation"
                    elif any(term in name.upper() for term in ["PARTNER", "LLP"]):
                        entity_type = "Partnership"
                    else:
                        entity_type = "Individual or Other"
                    
                    parties.append({
                        "name": name,
                        "role": role,
                        "type": entity_type
                    })
        
        seen_names: set = set()
        unique_parties: List[Dict[str, str]] = []
        for party in parties:
            if party["name"].lower() not in seen_names:
                seen_names.add(party["name"].lower())
                unique_parties.append(party)
        
        return {
            "parties": unique_parties,
            "total_count": len(unique_parties),
            "primary_parties": unique_parties[:2] if len(unique_parties) >= 2 else unique_parties,
            "analysis_note": "Parties extracted using pattern matching. Please verify for accuracy."
        }
    
    @tool
    def extract_key_dates(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract important dates from the contract.
        
        Identifies effective dates, termination dates, renewal dates,
        and other significant dates mentioned in the contract.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A dictionary containing:
                - dates: List of dates with type, value, and context
                - has_auto_renewal: Whether auto-renewal is mentioned
                - term_info: Basic term/duration information
        """
        dates: List[Dict[str, Any]] = []
        
        date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b'
        
        date_types = {
            "effective": r'(?:effective\s+(?:date|as of)|commencing\s+on|starting)\s*[:\s]*',
            "termination": r'(?:termin\w+\s+date|ends?\s+on|expir\w+\s+(?:date|on))\s*[:\s]*',
            "renewal": r'(?:renew\w+\s+date|renew\w+\s+on)\s*[:\s]*',
            "execution": r'(?:executed\s+(?:on|as of)|signed\s+on)\s*[:\s]*',
            "payment_due": r'(?:payment\s+due|due\s+date)\s*[:\s]*',
        }
        
        for date_type, pattern in date_types.items():
            combined_pattern = pattern + r'(' + date_pattern + r')'
            matches = re.findall(combined_pattern, contract_text, re.IGNORECASE)
            for match in matches:
                dates.append({
                    "date_type": date_type.replace("_", " ").title(),
                    "date_value": match.strip() if isinstance(match, str) else match,
                    "description": f"Found in context of {date_type}"
                })
        
        has_auto_renewal = bool(re.search(r'auto[- ]?renew|automatic\w*\s+renew', contract_text, re.IGNORECASE))
        
        term_match = re.search(r'(?:term|period)\s+of\s+(\d+)\s*(year|month|day)s?', contract_text, re.IGNORECASE)
        term_info = None
        if term_match:
            term_info = f"{term_match.group(1)} {term_match.group(2)}(s)"
        
        return {
            "dates": dates,
            "total_dates_found": len(dates),
            "has_auto_renewal": has_auto_renewal,
            "term_info": term_info,
            "analysis_note": "Date extraction based on common contract patterns."
        }
    
    @tool
    def extract_financial_terms(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract payment terms, amounts, and financial obligations.
        
        Identifies monetary values, payment schedules, fees, penalties,
        and other financial provisions in the contract.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A dictionary containing:
                - financial_terms: List of financial provisions found
                - total_value_estimate: Estimated total contract value if determinable
                - payment_structure: Overview of payment arrangements
        """
        financial_terms: List[Dict[str, Any]] = []
        
        currency_pattern = r'\$[\d,]+(?:\.\d{2})?|\b(?:USD|EUR|GBP)\s*[\d,]+(?:\.\d{2})?'
        
        text_lower = contract_text.lower()
        
        term_patterns = {
            "payment": r'(?:payment|pay)\s+(?:of\s+)?(' + currency_pattern + r')',
            "fee": r'(?:fee|fees)\s+(?:of\s+)?(' + currency_pattern + r')',
            "price": r'(?:price|cost|amount)\s+(?:of\s+)?(' + currency_pattern + r')',
            "penalty": r'(?:penalty|penalt(?:y|ies)|late fee)\s+(?:of\s+)?(' + currency_pattern + r')',
            "deposit": r'(?:deposit)\s+(?:of\s+)?(' + currency_pattern + r')',
        }
        
        for term_type, pattern in term_patterns.items():
            matches = re.findall(pattern, contract_text, re.IGNORECASE)
            for match in matches:
                financial_terms.append({
                    "term_type": term_type.title(),
                    "amount": match,
                    "frequency": self._detect_frequency(contract_text, match),
                    "conditions": None
                })
        
        payment_structure = []
        if re.search(r'\bmonthly\b', text_lower):
            payment_structure.append("Monthly payments mentioned")
        if re.search(r'\bquarterly\b', text_lower):
            payment_structure.append("Quarterly payments mentioned")
        if re.search(r'\bannual(?:ly)?\b', text_lower):
            payment_structure.append("Annual payments mentioned")
        if re.search(r'\bone[- ]time\b', text_lower):
            payment_structure.append("One-time payment mentioned")
        
        return {
            "financial_terms": financial_terms,
            "total_terms_found": len(financial_terms),
            "payment_structure": payment_structure if payment_structure else ["Payment structure not clearly identified"],
            "analysis_note": "Financial terms extracted using pattern matching. Verify amounts and terms."
        }
    
    def _detect_frequency(self, text: str, amount: str) -> Optional[str]:
        """Detect payment frequency near an amount."""
        amount_pos = text.find(amount)
        if amount_pos == -1:
            return None
        
        context = text[max(0, amount_pos - 100):amount_pos + 100].lower()
        
        if "monthly" in context:
            return "Monthly"
        elif "quarterly" in context:
            return "Quarterly"
        elif "annual" in context or "yearly" in context:
            return "Annually"
        elif "one-time" in context or "one time" in context:
            return "One-time"
        
        return None
    
    @tool
    def identify_obligations(self, contract_text: str) -> Dict[str, Any]:
        """
        Identify key obligations for each party in the contract.
        
        Extracts and categorizes the responsibilities and requirements
        each party must fulfill under the agreement.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A dictionary containing:
                - obligations: List of identified obligations
                - by_party: Obligations grouped by party if identifiable
                - critical_obligations: Most important obligations identified
        """
        obligations: List[Dict[str, Any]] = []
        
        obligation_patterns = [
            (r'(?:shall|must|is required to|agrees to|will)\s+([^.;]+[.;])', "Required Action"),
            (r'(?:responsible for|obligation to)\s+([^.;]+[.;])', "Responsibility"),
            (r'(?:warrants?|represents?|guarantees?)\s+(?:that\s+)?([^.;]+[.;])', "Warranty/Representation"),
            (r'(?:deliver|provide|supply)\s+([^.;]+[.;])', "Delivery"),
            (r'(?:maintain|keep|preserve)\s+([^.;]+[.;])', "Maintenance"),
            (r'(?:pay|compensate|reimburse)\s+([^.;]+[.;])', "Payment"),
            (r'(?:not\s+(?:shall|will|may)|prohibited from)\s+([^.;]+[.;])', "Restriction"),
        ]
        
        for pattern, category in obligation_patterns:
            matches = re.findall(pattern, contract_text, re.IGNORECASE)
            for match in matches[:3]:
                party = "Unknown Party"
                if "provider" in match.lower() or "seller" in match.lower():
                    party = "Provider/Seller"
                elif "client" in match.lower() or "buyer" in match.lower():
                    party = "Client/Buyer"
                
                obligations.append({
                    "party": party,
                    "description": match.strip()[:200],
                    "category": category,
                    "deadline": None
                })
        
        by_category: Dict[str, List[str]] = {}
        for ob in obligations:
            cat = ob["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(ob["description"][:100])
        
        return {
            "obligations": obligations[:15],
            "total_found": len(obligations),
            "by_category": by_category,
            "analysis_note": "Obligations identified through keyword analysis. Review contract for complete list."
        }
    
    @tool
    def detect_risk_clauses(self, contract_text: str) -> Dict[str, Any]:
        """
        Identify potentially risky or unfavorable clauses in the contract.
        
        Analyzes the contract for clauses that may pose legal, financial,
        or operational risks and provides risk assessments.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A dictionary containing:
                - risks: List of identified risk clauses with severity
                - high_priority_risks: Risks requiring immediate attention
                - overall_risk_level: General risk assessment
                - recommendations: Suggested actions
        """
        risks: List[Dict[str, Any]] = []
        text_lower = contract_text.lower()
        
        risk_patterns = [
            {
                "pattern": r'unlimited\s+liabil|liability\s+(?:shall\s+)?not\s+(?:be\s+)?limited',
                "clause_type": "Unlimited Liability",
                "risk_level": "High",
                "recommendation": "Negotiate liability cap or limitation clause"
            },
            {
                "pattern": r'indemnif(?:y|ication)\s+(?:and\s+)?hold\s+harmless',
                "clause_type": "Indemnification",
                "risk_level": "Medium",
                "recommendation": "Review scope of indemnification and ensure it's mutual"
            },
            {
                "pattern": r'terminat(?:e|ion)\s+(?:at\s+)?(?:any\s+time|without\s+(?:cause|notice))',
                "clause_type": "Termination at Will",
                "risk_level": "Medium",
                "recommendation": "Consider negotiating notice period requirements"
            },
            {
                "pattern": r'(?:exclusive|sole)\s+(?:remedy|remedies)',
                "clause_type": "Exclusive Remedy Limitation",
                "risk_level": "Medium",
                "recommendation": "Evaluate if exclusive remedies provide adequate protection"
            },
            {
                "pattern": r'waiv(?:e|er)\s+(?:of\s+)?(?:jury\s+trial|right\s+to)',
                "clause_type": "Waiver of Rights",
                "risk_level": "High",
                "recommendation": "Review carefully what rights are being waived"
            },
            {
                "pattern": r'auto[- ]?renew|automatic(?:ally)?\s+renew',
                "clause_type": "Auto-Renewal",
                "risk_level": "Low",
                "recommendation": "Note renewal terms and cancellation deadlines"
            },
            {
                "pattern": r'non[- ]?compet(?:e|ition)',
                "clause_type": "Non-Compete",
                "risk_level": "High",
                "recommendation": "Review scope, duration, and geographic limitations"
            },
            {
                "pattern": r'confidential(?:ity)?.*(?:perpetual|indefinite)',
                "clause_type": "Perpetual Confidentiality",
                "risk_level": "Medium",
                "recommendation": "Consider negotiating time-limited confidentiality"
            },
            {
                "pattern": r'governing\s+law|jurisdiction',
                "clause_type": "Jurisdiction/Governing Law",
                "risk_level": "Low",
                "recommendation": "Ensure favorable or neutral jurisdiction"
            },
            {
                "pattern": r'(?:binding\s+)?arbitration',
                "clause_type": "Mandatory Arbitration",
                "risk_level": "Medium",
                "recommendation": "Evaluate arbitration terms and venue"
            },
        ]
        
        for risk_info in risk_patterns:
            if re.search(risk_info["pattern"], text_lower):
                # Try to extract the actual clause text
                match = re.search(risk_info["pattern"] + r'[^.]*\.', contract_text, re.IGNORECASE)
                original_text = match.group(0)[:300] if match else None
                
                risks.append({
                    "clause_type": risk_info["clause_type"],
                    "risk_level": risk_info["risk_level"],
                    "description": f"Contract contains {risk_info['clause_type'].lower()} provisions",
                    "recommendation": risk_info["recommendation"],
                    "original_text": original_text
                })
        
        high_risks = sum(1 for r in risks if r["risk_level"] == "High")
        medium_risks = sum(1 for r in risks if r["risk_level"] == "Medium")
        
        if high_risks >= 2:
            overall_risk = "High"
        elif high_risks >= 1 or medium_risks >= 3:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"
        
        return {
            "risks": risks,
            "total_risks_found": len(risks),
            "high_priority_risks": [r for r in risks if r["risk_level"] == "High"],
            "overall_risk_level": overall_risk,
            "risk_summary": {
                "high": high_risks,
                "medium": medium_risks,
                "low": len(risks) - high_risks - medium_risks
            },
            "recommendations": [r["recommendation"] for r in risks if r["risk_level"] in ["High", "Medium"]],
            "analysis_note": "Risk assessment based on common clause patterns. Consult legal counsel for thorough review."
        }
    
    @tool
    def summarize_contract(self, contract_text: str) -> str:
        """
        Generate an executive summary of the contract.
        
        Creates a high-level overview of the contract's main provisions,
        parties, terms, and key points suitable for quick review.
        
        Args:
            contract_text: The full text of the contract to analyze.
        
        Returns:
            A formatted executive summary string covering the main aspects
            of the contract.
        """
        parties = self.extract_parties(contract_text)
        dates = self.extract_key_dates(contract_text)
        financial = self.extract_financial_terms(contract_text)
        risks = self.detect_risk_clauses(contract_text)
        
        summary_parts = []
        
        summary_parts.append("=" * 50)
        summary_parts.append("CONTRACT EXECUTIVE SUMMARY")
        summary_parts.append("=" * 50)
        
        summary_parts.append("\n📋 PARTIES:")
        if parties["parties"]:
            for p in parties["parties"][:4]:
                summary_parts.append(f"  • {p['name']} ({p['role']}) - {p['type']}")
        else:
            summary_parts.append("  • No parties clearly identified")
        
        summary_parts.append("\n📅 KEY DATES & TERM:")
        if dates["term_info"]:
            summary_parts.append(f"  • Contract Term: {dates['term_info']}")
        if dates["dates"]:
            for d in dates["dates"][:3]:
                summary_parts.append(f"  • {d['date_type']}: {d['date_value']}")
        if dates["has_auto_renewal"]:
            summary_parts.append("  • ⚠️ Contains auto-renewal provisions")
        
        summary_parts.append("\n💰 FINANCIAL TERMS:")
        if financial["financial_terms"]:
            for f in financial["financial_terms"][:4]:
                freq = f" ({f['frequency']})" if f.get('frequency') else ""
                summary_parts.append(f"  • {f['term_type']}: {f['amount']}{freq}")
        else:
            summary_parts.append("  • No specific financial terms identified")
        
        summary_parts.append("\n⚠️ RISK ASSESSMENT:")
        summary_parts.append(f"  • Overall Risk Level: {risks['overall_risk_level']}")
        summary_parts.append(f"  • High Risks: {risks['risk_summary']['high']}, Medium: {risks['risk_summary']['medium']}, Low: {risks['risk_summary']['low']}")
        
        if risks["high_priority_risks"]:
            summary_parts.append("  • Priority Items:")
            for r in risks["high_priority_risks"][:3]:
                summary_parts.append(f"    - {r['clause_type']}: {r['recommendation']}")
        
        summary_parts.append("\n" + "=" * 50)
        summary_parts.append("This summary is for informational purposes only.")
        summary_parts.append("Consult legal counsel for comprehensive review.")
        summary_parts.append("=" * 50)
        
        return "\n".join(summary_parts)
