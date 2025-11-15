"""
Guardrails & Safety Service
Content moderation, policy enforcement, and safety checks
"""

import logging
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Moderation API (if available)
HF_TOKEN = os.getenv("HF_TOKEN")
MODERATION_MODEL = "facebook/roberta-hate-speech-dynabench-r4-target"


class GuardrailsService:
    """
    Content moderation and safety system
    Checks for: hate speech, violence, adult content, PII, brand safety
    """
    
    def __init__(self):
        self.blocked_words = self._load_blocked_words()
        self.sensitive_topics = self._load_sensitive_topics()
        self.pii_patterns = self._compile_pii_patterns()
    
    def _load_blocked_words(self) -> List[str]:
        """Load list of blocked/inappropriate words"""
        # Basic blocked words list (expand as needed)
        return [
            # Add specific blocked words here
            # This is a minimal list for demonstration
            "hate", "violence", "explicit", "offensive"
        ]
    
    def _load_sensitive_topics(self) -> List[str]:
        """Load list of sensitive topics requiring extra scrutiny"""
        return [
            "politics", "religion", "race", "sexuality", "medical", 
            "tragic events", "terrorism", "self-harm", "illegal activities"
        ]
    
    def _compile_pii_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for PII detection"""
        return {
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            "ip_address": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        }
    
    def check_content_safety(
        self, 
        text: str, 
        strict_mode: bool = False
    ) -> Tuple[bool, Dict]:
        """
        Comprehensive content safety check
        
        Args:
            text: Text to check
            strict_mode: Enable stricter checking
            
        Returns:
            Tuple of (is_safe, details_dict)
        """
        issues = []
        warnings = []
        
        # 1. Check for blocked words
        text_lower = text.lower()
        found_blocked = [word for word in self.blocked_words if word in text_lower]
        if found_blocked:
            issues.append(f"Contains blocked words: {', '.join(found_blocked)}")
        
        # 2. Check for PII
        pii_found = self._detect_pii(text)
        if pii_found:
            issues.append(f"Contains PII: {', '.join(pii_found.keys())}")
        
        # 3. Check for sensitive topics
        sensitive_found = [topic for topic in self.sensitive_topics if topic in text_lower]
        if sensitive_found:
            if strict_mode:
                issues.append(f"Contains sensitive topics: {', '.join(sensitive_found)}")
            else:
                warnings.append(f"Mentions sensitive topics: {', '.join(sensitive_found)}")
        
        # 4. Check text length
        if len(text) > 500:
            warnings.append("Text is very long (>500 chars)")
        
        # 5. Check for excessive caps (shouting)
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        if caps_ratio > 0.5:
            warnings.append("Excessive use of capital letters")
        
        # 6. Check for spam patterns
        if self._is_spam_pattern(text):
            issues.append("Detected spam-like patterns")
        
        # Determine if safe
        is_safe = len(issues) == 0
        
        return is_safe, {
            "is_safe": is_safe,
            "issues": issues,
            "warnings": warnings,
            "pii_detected": bool(pii_found),
            "pii_types": list(pii_found.keys()) if pii_found else [],
            "timestamp": datetime.now().isoformat()
        }
    
    def _detect_pii(self, text: str) -> Dict[str, List[str]]:
        """
        Detect personally identifiable information
        
        Args:
            text: Text to check
            
        Returns:
            Dictionary of PII types and matched values
        """
        pii_found = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Redact actual values in output
                pii_found[pii_type] = ["[REDACTED]"] * len(matches)
        
        return pii_found
    
    def _is_spam_pattern(self, text: str) -> bool:
        """Check for spam-like patterns"""
        # Check for repeated characters
        if re.search(r'(.)\1{5,}', text):
            return True
        
        # Check for excessive URLs
        url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        if url_count > 2:
            return True
        
        # Check for excessive emojis
        emoji_count = sum(1 for c in text if ord(c) > 127000)
        if emoji_count > 20:
            return True
        
        return False
    
    def moderate_with_api(self, text: str) -> Dict:
        """
        Use AI model for content moderation (if API available)
        
        Args:
            text: Text to moderate
            
        Returns:
            Moderation results
        """
        try:
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            api_url = f"https://api-inference.huggingface.co/models/{MODERATION_MODEL}"
            
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse results (format varies by model)
                if isinstance(result, list) and len(result) > 0:
                    scores = result[0]
                    
                    # Find highest scoring label
                    max_label = max(scores, key=lambda x: x['score'])
                    
                    return {
                        "model": MODERATION_MODEL,
                        "label": max_label['label'],
                        "score": max_label['score'],
                        "is_safe": max_label['label'] in ['NEUTRAL', 'SAFE', 'OK'],
                        "all_scores": scores
                    }
            
        except Exception as e:
            logger.warning(f"API moderation failed: {e}")
        
        # Fallback to rule-based
        return {
            "model": "rule_based",
            "is_safe": True,
            "message": "API moderation unavailable, using rule-based checks"
        }
    
    def check_brand_safety(
        self, 
        text: str, 
        image_description: str,
        brand_guidelines: Optional[Dict] = None
    ) -> Tuple[bool, Dict]:
        """
        Check if content aligns with brand safety guidelines
        
        Args:
            text: Caption text
            image_description: Description of image
            brand_guidelines: Optional brand-specific guidelines
            
        Returns:
            Tuple of (is_brand_safe, details_dict)
        """
        issues = []
        warnings = []
        
        # Default brand safety rules
        unsafe_contexts = [
            "violence", "weapons", "drugs", "alcohol", "tobacco",
            "gambling", "adult content", "political extremism"
        ]
        
        # Check caption and image description
        combined_text = f"{text} {image_description}".lower()
        
        for context in unsafe_contexts:
            if context in combined_text:
                issues.append(f"Potentially unsafe context: {context}")
        
        # Check brand guidelines if provided
        if brand_guidelines:
            forbidden_words = brand_guidelines.get("forbidden_words", [])
            required_tone = brand_guidelines.get("required_tone", None)
            
            for word in forbidden_words:
                if word.lower() in combined_text:
                    issues.append(f"Contains forbidden word: {word}")
            
            if required_tone:
                # Simple tone check (can be enhanced with sentiment analysis)
                if required_tone == "professional" and any(slang in combined_text for slang in ["lol", "omg", "wtf"]):
                    warnings.append("Tone may not match professional brand guidelines")
        
        is_brand_safe = len(issues) == 0
        
        return is_brand_safe, {
            "is_brand_safe": is_brand_safe,
            "issues": issues,
            "warnings": warnings,
            "timestamp": datetime.now().isoformat()
        }
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by removing PII and problematic content
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        sanitized = text
        
        # Remove PII
        for pii_type, pattern in self.pii_patterns.items():
            sanitized = pattern.sub("[REDACTED]", sanitized)
        
        # Remove blocked words
        for word in self.blocked_words:
            sanitized = re.sub(r'\b' + re.escape(word) + r'\b', '[FILTERED]', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def get_safety_report(self, text: str, image_description: str = "") -> Dict:
        """
        Generate comprehensive safety report
        
        Args:
            text: Caption text
            image_description: Image description
            
        Returns:
            Complete safety report
        """
        # Content safety check
        is_safe, content_check = self.check_content_safety(text, strict_mode=False)
        
        # Brand safety check
        is_brand_safe, brand_check = self.check_brand_safety(text, image_description)
        
        # API moderation (optional)
        api_moderation = self.moderate_with_api(text)
        
        # Overall verdict
        overall_safe = is_safe and is_brand_safe
        
        return {
            "overall_safe": overall_safe,
            "content_safety": content_check,
            "brand_safety": brand_check,
            "ai_moderation": api_moderation,
            "recommendation": "approved" if overall_safe else "needs_review",
            "timestamp": datetime.now().isoformat()
        }


# Singleton instance
_guardrails_service = None

def get_guardrails_service() -> GuardrailsService:
    """Get or create Guardrails Service singleton"""
    global _guardrails_service
    if _guardrails_service is None:
        _guardrails_service = GuardrailsService()
    return _guardrails_service