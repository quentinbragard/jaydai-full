from typing import Dict, List, Any
import numpy as np

def calculate_efficiency_score(
    messages: List[Dict[str, Any]],
    chats: List[Dict[str, Any]],
    response_quality: Dict[str, Any],
    usage_patterns: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate a comprehensive AI usage efficiency score based on multiple factors.
    
    Args:
        messages: List of all user and AI messages
        chats: List of chat objects
        response_quality: Response quality metrics from analyze_response_quality
        usage_patterns: Usage pattern metrics from compute_usage_patterns
        
    Returns:
        Dictionary with overall and component scores
    """
    # Start with base metrics
    user_messages = [m for m in messages if m.get("role") == "user"]
    ai_messages = [m for m in messages if m.get("role") == "assistant"]
    
    if not user_messages or not ai_messages or not chats:
        return {
            "overall_score": 50,
            "components": {
                "prompt_efficiency": 50,
                "conversation_flow": 50,
                "resource_usage": 50,
                "completion_quality": 50,
                "interaction_pattern": 50
            },
            "percentile": 50,
            "interpretation": "No data available for scoring"
        }
    
    # 1. Prompt Efficiency - How effectively user prompts elicit good responses
    avg_user_prompt_len = np.mean([len(m.get("content", "")) for m in user_messages])
    avg_ai_response_len = np.mean([len(m.get("content", "")) for m in ai_messages])
    
    # Ideal ratio: not too short prompts, but not excessively long compared to responses
    response_to_prompt_ratio = avg_ai_response_len / max(1, avg_user_prompt_len)
    
    # Score highest when ratio is between 2-5 (good leverage of AI)
    if response_to_prompt_ratio < 1:
        prompt_efficiency = 40  # Very low leverage
    elif response_to_prompt_ratio < 2:
        prompt_efficiency = 60  # Moderate leverage
    elif response_to_prompt_ratio < 5:
        prompt_efficiency = 90  # Optimal range
    elif response_to_prompt_ratio < 10:
        prompt_efficiency = 75  # Good but potentially unfocused
    else:
        prompt_efficiency = 60  # Very high ratio may indicate vague prompts
    
    # Adjust based on prompt length distribution
    p_len_dist = usage_patterns.get("prompt_length_distribution", {})
    
    # Very short prompts (< 10 chars) or very long (> 1000) are penalized
    if p_len_dist:
        if p_len_dist.get("median", 0) < 10:
            prompt_efficiency -= 20
        elif p_len_dist.get("median", 0) > 1000:
            prompt_efficiency -= 10
    
    # 2. Conversation Flow - How well conversations develop
    conv_depth = response_quality.get("conversation_depth", 0)
    
    # Score based on depth (ideal: 3-7 turns shows good development without excessive back-and-forth)
    if conv_depth < 2:
        conversation_flow = 40  # Too shallow
    elif conv_depth < 3:
        conversation_flow = 60
    elif conv_depth < 7:
        conversation_flow = 85  # Optimal range
    elif conv_depth < 10:
        conversation_flow = 70  # Getting excessive
    else:
        conversation_flow = 50  # Too much back-and-forth, may indicate confusion
    
    # Adjust by follow-up rate (AI asking good questions)
    follow_up_rate = response_quality.get("follow_up_rate", 0)
    if 0.1 <= follow_up_rate <= 0.4:
        conversation_flow += 10  # Good amount of follow-ups
    
    # 3. Resource Usage - Energy and computational efficiency
    # Calculate tokens per useful information
    info_density = response_quality.get("information_density", 0)
    
    if info_density > 3:
        resource_score = 90  # Very information-dense
    elif info_density > 1.5:
        resource_score = 80  # Good information density
    elif info_density > 0.5:
        resource_score = 65  # Moderate information
    else:
        resource_score = 50  # Low information density
    
    # 4. Completion Quality
    # Based on information density, code quality, and response length variation
    
    length_stats = response_quality.get("response_length_stats", {})
    length_variation = 0
    if length_stats:
        if "p75" in length_stats and "p25" in length_stats and length_stats["p25"] > 0:
            length_variation = length_stats["p75"] / length_stats["p25"]
    
    # Good completions have reasonable length variation (adapting to different questions)
    if 1.5 <= length_variation <= 5:
        length_score = 80  # Good adaptation
    elif length_variation > 10:
        length_score = 60  # Too much variation
    else:
        length_score = 70  # Too little variation
    
    # Code quality component (based on frequency and lines)
    code_stats = response_quality.get("code_snippet_stats", {})
    code_score = 70  # Default
    
    if code_stats:
        # Adjust based on code presence and quality
        code_freq = code_stats.get("frequency", 0)
        avg_lines = code_stats.get("avg_lines", 0)
        
        if code_freq > 0:
            # Some code is present
            if 5 <= avg_lines <= 30:
                code_score = 85  # Good code length
            elif avg_lines > 50:
                code_score = 70  # Potentially excessive code
    
    completion_quality = (length_score + code_score + resource_score) / 3
    
    # 5. Interaction Pattern - How well the user interacts with AI
    session_stats = usage_patterns.get("session_stats", {})
    
    # Optimal: 4-15 messages per session shows good engagement
    avg_msgs = session_stats.get("avg_messages", 0)
    
    if avg_msgs < 3:
        interaction_score = 50  # Too few messages
    elif avg_msgs < 6:
        interaction_score = 75  # Good but could engage more
    elif avg_msgs < 15:
        interaction_score = 90  # Optimal range
    elif avg_msgs < 25:
        interaction_score = 75  # Getting excessive
    else:
        interaction_score = 60  # Too many messages may indicate inefficiency
    
    # Calculate overall score (weighted average)
    overall_score = round(
        prompt_efficiency * 0.25 +
        conversation_flow * 0.25 +
        resource_score * 0.2 +
        completion_quality * 0.15 +
        interaction_score * 0.15
    )
    
    # Cap at 100
    overall_score = min(100, overall_score)
    
    # Determine percentile (placeholder - would need population stats)
    # In a real implementation, you'd compare to population distribution
    percentile = min(100, overall_score + 10)
    
    # Interpret the score
    if overall_score >= 85:
        interpretation = "Expert AI user - highly efficient prompting and interaction patterns"
    elif overall_score >= 75:
        interpretation = "Advanced AI user - good conversation flow and prompt efficiency"
    elif overall_score >= 65:
        interpretation = "Proficient AI user - effective but with room for optimization"
    elif overall_score >= 50:
        interpretation = "Developing AI user - learning effective interaction patterns"
    else:
        interpretation = "Novice AI user - could benefit from prompt optimization techniques"
    
    return {
        "overall_score": overall_score,
        "components": {
            "prompt_efficiency": round(prompt_efficiency),
            "conversation_flow": round(conversation_flow),
            "resource_usage": round(resource_score),
            "completion_quality": round(completion_quality),
            "interaction_pattern": round(interaction_score)
        },
        "percentile": percentile,
        "interpretation": interpretation
    }