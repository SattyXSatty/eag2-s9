# modules/heuristics.py

import re
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of validation check"""
    is_valid: bool
    cleaned_text: str
    reason: Optional[str] = None
    severity: str = "info"  # info, warning, error


class QueryHeuristics:
    """Pre-processing heuristics for user queries before sending to LLM"""
    
    # Banned words and patterns
    BANNED_WORDS = {
        # Profanity (add more as needed)
        "fuck", "shit", "damn", "bitch", "asshole",
        # Sensitive patterns will be caught by regex
    }
    
    # Prompt injection patterns
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|above)\s+instructions?",
        r"disregard\s+(previous|all|above)",
        r"forget\s+(everything|all|previous)",
        r"new\s+instructions?:",
        r"system\s*:\s*you\s+are",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"###\s*instruction",
    ]
    
    # Sensitive data patterns
    SENSITIVE_PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        "api_key": r'\b[A-Za-z0-9]{32,}\b',
    }
    
    MAX_QUERY_LENGTH = 2000  # characters
    MIN_QUERY_LENGTH = 2
    
    @classmethod
    def validate_and_clean(cls, query: str) -> ValidationResult:
        """Run all query heuristics and return cleaned query"""
        
        # 1. Remove banned or sensitive words
        result = cls.remove_sensitive_data(query)
        if not result.is_valid:
            return result
        query = result.cleaned_text
        
        # 2. Stop prompt injection
        result = cls.detect_prompt_injection(query)
        if not result.is_valid:
            return result
        
        # 3. Trim and normalize input
        query = cls.normalize_input(query)
        
        # 4. Limit query length
        result = cls.check_length(query)
        if not result.is_valid:
            return result
        query = result.cleaned_text
        
        # 5. Detect empty or meaningless input
        result = cls.check_meaningful(query)
        if not result.is_valid:
            return result
        
        return ValidationResult(
            is_valid=True,
            cleaned_text=query,
            reason="Query validated successfully"
        )
    
    @classmethod
    def remove_sensitive_data(cls, text: str) -> ValidationResult:
        """Heuristic 1: Remove or mask sensitive information"""
        cleaned = text
        redactions = []
        
        for data_type, pattern in cls.SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                cleaned = re.sub(pattern, f"[REDACTED_{data_type.upper()}]", cleaned)
                redactions.append(data_type)
        
        # Check for banned words
        text_lower = text.lower()
        found_banned = [word for word in cls.BANNED_WORDS if word in text_lower]
        if found_banned:
            for word in found_banned:
                cleaned = re.sub(
                    rf'\b{re.escape(word)}\b',
                    "[REDACTED]",
                    cleaned,
                    flags=re.IGNORECASE
                )
            redactions.append("profanity")
        
        if redactions:
            return ValidationResult(
                is_valid=True,
                cleaned_text=cleaned,
                reason=f"Redacted: {', '.join(redactions)}",
                severity="warning"
            )
        
        return ValidationResult(is_valid=True, cleaned_text=text)
    
    @classmethod
    def detect_prompt_injection(cls, text: str) -> ValidationResult:
        """Heuristic 2: Detect and block prompt injection attempts"""
        text_lower = text.lower()
        
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                return ValidationResult(
                    is_valid=False,
                    cleaned_text="",
                    reason="Potential prompt injection detected. Please rephrase your query.",
                    severity="error"
                )
        
        return ValidationResult(is_valid=True, cleaned_text=text)
    
    @classmethod
    def normalize_input(cls, text: str) -> str:
        """Heuristic 3: Trim and normalize input"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive punctuation
        text = re.sub(r'([!?.]){3,}', r'\1\1', text)
        
        # Remove emojis (optional - keep if needed for sentiment)
        # text = re.sub(r'[^\w\s,.!?-]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @classmethod
    def check_length(cls, text: str) -> ValidationResult:
        """Heuristic 4: Limit query length"""
        length = len(text)
        
        if length > cls.MAX_QUERY_LENGTH:
            truncated = text[:cls.MAX_QUERY_LENGTH] + "..."
            return ValidationResult(
                is_valid=True,
                cleaned_text=truncated,
                reason=f"Query truncated from {length} to {cls.MAX_QUERY_LENGTH} characters",
                severity="warning"
            )
        
        return ValidationResult(is_valid=True, cleaned_text=text)
    
    @classmethod
    def check_meaningful(cls, text: str) -> ValidationResult:
        """Heuristic 5: Detect empty or meaningless input"""
        if len(text) < cls.MIN_QUERY_LENGTH:
            return ValidationResult(
                is_valid=False,
                cleaned_text="",
                reason="Query too short. Please provide more details.",
                severity="error"
            )
        
        # Check for meaningless single words
        meaningless = {"hi", "hello", "ok", "okay", "yes", "no", "?", ".", "!"}
        if text.lower().strip() in meaningless:
            return ValidationResult(
                is_valid=False,
                cleaned_text="",
                reason="Please provide a specific question or task.",
                severity="error"
            )
        
        return ValidationResult(is_valid=True, cleaned_text=text)


class ResponseHeuristics:
    """Post-processing heuristics for LLM responses before returning to user"""
    
    # System leakage patterns
    SYSTEM_LEAKAGE_PATTERNS = [
        r"as an ai (language )?model",
        r"i('m| am) (an )?ai",
        r"my (training|knowledge) (data|cutoff)",
        r"api[_\s]?key[:\s]+[A-Za-z0-9]+",
        r"secret[_\s]?key",
        r"password[:\s]+\w+",
        r"system\s+prompt",
        r"internal\s+instructions?",
    ]
    
    # Hallucination indicators
    HALLUCINATION_PATTERNS = {
        "suspicious_url": r'https?://[^\s]+\.(xyz|tk|ml|ga|cf)',
        "fake_citation": r'\[citation needed\]|\[source:\s*unknown\]',
        "uncertain": r'(i think|maybe|possibly|might be|could be)\s+\d+',
    }
    
    @classmethod
    def validate_and_clean(cls, response: str, original_query: str = "") -> ValidationResult:
        """Run all response heuristics and return cleaned response"""
        
        # 6. Banned word & safety check
        result = cls.safety_check(response)
        if not result.is_valid:
            return result
        response = result.cleaned_text
        
        # 7. No system or secret leakage
        result = cls.check_system_leakage(response)
        if not result.is_valid:
            return result
        response = result.cleaned_text
        
        # 8. Relevance check (if original query provided)
        if original_query:
            result = cls.check_relevance(response, original_query)
            if not result.is_valid:
                return result
        
        # 9. Basic hallucination guard
        result = cls.check_hallucination(response)
        if result.severity == "warning":
            # Log warning but continue
            pass
        
        # 10. Formatting & clean output
        response = cls.clean_formatting(response)
        
        return ValidationResult(
            is_valid=True,
            cleaned_text=response,
            reason="Response validated successfully"
        )
    
    @classmethod
    def safety_check(cls, text: str) -> ValidationResult:
        """Heuristic 6: Re-scan for banned words and sensitive info"""
        # Reuse query heuristic
        return QueryHeuristics.remove_sensitive_data(text)
    
    @classmethod
    def check_system_leakage(cls, text: str) -> ValidationResult:
        """Heuristic 7: Block system or secret leakage"""
        text_lower = text.lower()
        
        for pattern in cls.SYSTEM_LEAKAGE_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                # Remove the leaking sentence
                cleaned = re.sub(
                    r'[^.!?]*' + re.escape(match.group(0)) + r'[^.!?]*[.!?]',
                    '',
                    text,
                    flags=re.IGNORECASE
                )
                return ValidationResult(
                    is_valid=True,
                    cleaned_text=cleaned.strip(),
                    reason="Removed system information leakage",
                    severity="warning"
                )
        
        return ValidationResult(is_valid=True, cleaned_text=text)
    
    @classmethod
    def check_relevance(cls, response: str, query: str) -> ValidationResult:
        """Heuristic 8: Basic relevance check using keyword overlap"""
        # Extract keywords from query (simple approach)
        query_words = set(re.findall(r'\b\w{4,}\b', query.lower()))
        response_words = set(re.findall(r'\b\w{4,}\b', response.lower()))
        
        if not query_words:
            return ValidationResult(is_valid=True, cleaned_text=response)
        
        # Calculate overlap
        overlap = len(query_words & response_words) / len(query_words)
        
        if overlap < 0.1:  # Less than 10% keyword overlap
            return ValidationResult(
                is_valid=False,
                cleaned_text="",
                reason="Response appears off-topic. Please try rephrasing your query.",
                severity="error"
            )
        
        return ValidationResult(is_valid=True, cleaned_text=response)
    
    @classmethod
    def check_hallucination(cls, text: str) -> ValidationResult:
        """Heuristic 9: Basic hallucination guard"""
        warnings = []
        
        for indicator, pattern in cls.HALLUCINATION_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                warnings.append(indicator)
        
        if warnings:
            return ValidationResult(
                is_valid=True,
                cleaned_text=text,
                reason=f"Potential hallucination indicators: {', '.join(warnings)}",
                severity="warning"
            )
        
        return ValidationResult(is_valid=True, cleaned_text=text)
    
    @classmethod
    def clean_formatting(cls, text: str) -> str:
        """Heuristic 10: Ensure clean output formatting"""
        # Remove double spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove HTML tags (if any leaked through)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Fix broken markdown (optional)
        # text = re.sub(r'\*\*\s+', '**', text)
        # text = re.sub(r'\s+\*\*', '**', text)
        
        # Remove trailing whitespace from lines
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        # Ensure single newline at end
        text = text.strip() + '\n'
        
        return text


# Convenience functions
def validate_query(query: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate and clean user query.
    Returns: (is_valid, cleaned_query, error_message)
    """
    result = QueryHeuristics.validate_and_clean(query)
    return result.is_valid, result.cleaned_text, result.reason


def validate_response(response: str, original_query: str = "") -> Tuple[bool, str, Optional[str]]:
    """
    Validate and clean LLM response.
    Returns: (is_valid, cleaned_response, warning_message)
    """
    result = ResponseHeuristics.validate_and_clean(response, original_query)
    return result.is_valid, result.cleaned_text, result.reason
