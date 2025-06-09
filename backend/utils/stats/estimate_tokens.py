import re
from typing import Dict, Optional

# Token ratio constants for different models
MODEL_TOKEN_RATIOS: Dict[str, float] = {
    "gpt-3.5-turbo": 4.0,
    "gpt-4": 3.8,
    "claude-3-opus": 3.5,
    "claude-3-haiku": 3.7,
    "claude-3-sonnet": 3.6,
    "default": 4.0  # Fallback ratio
}

# Language modifiers (approximation based on character density)
LANGUAGE_MODIFIERS: Dict[str, float] = {
    "en": 1.0,      # English (baseline)
    "fr": 0.9,      # French (tends to use more characters)
    "de": 0.85,     # German (compound words)
    "ja": 0.5,      # Japanese (higher information density)
    "zh": 0.4,      # Chinese (very high information density)
    "default": 1.0  # Default language factor
}

def detect_language(content: str) -> str:
    """Simple language detection based on character patterns"""
    if not content or len(content) < 10:
        return "default"
    
    # Check for Asian languages
    if re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]', content):
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', content):  # Japanese kana
            return "ja"
        if re.search(r'[\u4e00-\u9fff]', content):  # Chinese characters
            return "zh"
    
    # Check for European languages
    if re.search(r'[àáâäæçèéêëìíîïòóôöùúûüÿ]', content):
        if re.search(r'[ùûüÿàâæçéèêëïî]', content):  # French
            return "fr"
        if re.search(r'[äöüß]', content):  # German
            return "de"
    
    return "en"  # Default to English

def estimate_tokens(content: str, model: str = "default") -> int:
    """
    Estimate token count based on content, model, and detected language.
    
    Args:
        content: The text content to estimate tokens for
        model: AI model name to use for estimation
        
    Returns:
        Estimated token count as integer
    """
    if not content:
        return 0
    
    # Get model-specific char-to-token ratio
    ratio = MODEL_TOKEN_RATIOS.get(model, MODEL_TOKEN_RATIOS["default"])
    
    # Apply language-specific modifier
    lang = detect_language(content)
    modifier = LANGUAGE_MODIFIERS.get(lang, LANGUAGE_MODIFIERS["default"])
    
    # Additional factors
    code_blocks = len(re.findall(r'```[\s\S]*?```', content))
    code_modifier = 1.0 + (code_blocks * 0.05)  # Code is typically more token-efficient
    
    # Calculate final token estimate
    char_count = len(content)
    estimated_tokens = int((char_count / (ratio * modifier)) * code_modifier)
    
    return max(1, estimated_tokens)  # Ensure at least 1 token for non-empty content