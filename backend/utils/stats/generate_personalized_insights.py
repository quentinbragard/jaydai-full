from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

def generate_personalized_insights(
    efficiency_score: Dict[str, Any],
    response_quality: Dict[str, Any],
    usage_patterns: Dict[str, Any],
    token_usage: Dict[str, Any],
    energy_usage: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generate personalized, actionable insights for the user based on their AI usage patterns.
    
    Args:
        efficiency_score: Efficiency scoring metrics
        response_quality: Response quality metrics
        usage_patterns: Usage pattern metrics
        token_usage: Token usage statistics
        energy_usage: Energy consumption metrics
        
    Returns:
        List of insight objects with title, description, and type
    """
    insights = []
    
    # 1. Prompt Optimization Insights
    prompt_efficiency = efficiency_score.get("components", {}).get("prompt_efficiency", 0)
    prompt_lengths = usage_patterns.get("prompt_length_distribution", {})
    
    if prompt_efficiency < 65:
        if prompt_lengths.get("median", 0) < 20:
            insights.append({
                "type": "prompt_optimization",
                "title": "Try More Specific Prompts",
                "description": "Your prompts tend to be very brief. Adding more specific instructions and context could help you get more detailed and accurate responses.",
                "action": "prompt_example"
            })
        elif prompt_lengths.get("median", 0) > 500:
            insights.append({
                "type": "prompt_optimization",
                "title": "Consider More Focused Prompts",
                "description": "Your prompts are quite lengthy. Try breaking complex questions into separate, focused prompts for more precise answers.",
                "action": "show_focus_technique"
            })
    
    # 2. Conversation Flow Insights
    conversation_flow = efficiency_score.get("components", {}).get("conversation_flow", 0)
    follow_up_rate = response_quality.get("follow_up_rate", 0)
    
    if conversation_flow < 70:
        if response_quality.get("conversation_depth", 0) < 3:
            insights.append({
                "type": "conversation_flow",
                "title": "Engage in Deeper Conversations",
                "description": "Your conversations tend to be brief. Follow-up questions can help you get more comprehensive information and explore topics more thoroughly.",
                "action": "conversation_example"
            })
        elif response_quality.get("max_conversation_depth", 0) > 10:
            insights.append({
                "type": "conversation_flow",
                "title": "Streamline Your Conversations",
                "description": "Some of your conversations involve extensive back-and-forth. Try to provide more context upfront to reach solutions more efficiently.",
                "action": "show_streamlining"
            })
    
    # 3. Time-of-Day Optimization
    active_hours = usage_patterns.get("active_hours", {})
    if active_hours:
        # Find peak usage hours
        peak_hours = sorted(active_hours.items(), key=lambda x: float(x[1]), reverse=True)[:2]
        peak_hour_values = [int(h) for h, _ in peak_hours]
        
        # Group into time periods
        morning = list(range(5, 12))
        afternoon = list(range(12, 18))
        evening = list(range(18, 23))
        night = list(range(23, 24)) + list(range(0, 5))
        
        periods = []
        for h in peak_hour_values:
            if h in morning:
                periods.append("morning")
            elif h in afternoon:
                periods.append("afternoon")
            elif h in evening:
                periods.append("evening")
            else:
                periods.append("night")
        
        primary_period = max(set(periods), key=periods.count)
        
        insights.append({
            "type": "usage_pattern",
            "title": f"Peak Productivity: {primary_period.title()} AI User",
            "description": f"You tend to use AI most during the {primary_period}. This pattern might reflect when you're most productive or when you need AI assistance the most.",
            "action": None
        })
    
    # 4. Energy Usage Insights
    per_message_wh = energy_usage.get("per_message_wh", 0)
    if per_message_wh > 0.001:
        insights.append({
            "type": "sustainability",
            "title": "Optimize for Sustainability",
            "description": f"Your AI interactions use {energy_usage.get('total_wh', 0):.4f} Wh of energy. Using more targeted prompts can reduce your carbon footprint while getting better results.",
            "action": "sustainability_tips"
        })
    
    # 5. AI Model Selection Insight
    prompt_effectiveness = efficiency_score.get("components", {}).get("prompt_efficiency", 0)
    resource_usage = efficiency_score.get("components", {}).get("resource_usage", 0)
    
    if resource_usage < 70:
        insights.append({
            "type": "model_selection",
            "title": "Model Selection Optimization",
            "description": "Consider using smaller, more efficient models for simple tasks, saving more powerful models for complex reasoning and creative work.",
            "action": "model_comparison"
        })
    
    # 6. Code Usage Insights
    code_stats = response_quality.get("code_snippet_stats", {})
    if code_stats and code_stats.get("frequency", 0) > 0.1:
        if code_stats.get("avg_lines", 0) < 5:
            insights.append({
                "type": "coding_pattern",
                "title": "Expand Your Code Requests",
                "description": "You're getting code snippets, but they tend to be brief. For more complete solutions, try asking for full implementations with error handling and comments.",
                "action": "code_prompt_example"
            })
        elif code_stats.get("total_snippets", 0) > 20:
            insights.append({
                "type": "coding_pattern",
                "title": "Code Power User",
                "description": "You've generated substantial code with AI assistance. Consider creating a personal code library to reuse these solutions.",
                "action": "code_library_tips"
            })
    
    # 7. Session Pattern Insights
    session_stats = usage_patterns.get("session_stats", {})
    if session_stats:
        avg_duration = session_stats.get("avg_duration", 0)
        if avg_duration > 30:  # More than 30 minutes average
            insights.append({
                "type": "session_pattern",
                "title": "Deep Focus Sessions",
                "description": "Your AI sessions average over 30 minutes. These deep dives suggest you're tackling complex problems or learning new topics.",
                "action": None
            })
        elif avg_duration < 5 and session_stats.get("count", 0) > 10:  # Short, frequent sessions
            insights.append({
                "type": "session_pattern",
                "title": "Quick Reference Pattern",
                "description": "You tend to have many brief AI interactions. This 'quick reference' pattern is efficient for fact-checking and short questions.",
                "action": None
            })
    
    # 8. Token Efficiency Insights
    if token_usage and token_usage.get("total_input", 0) > 0:
        io_ratio = token_usage.get("total_output", 0) / token_usage.get("total_input", 0)
        
        if io_ratio < 2:
            insights.append({
                "type": "token_efficiency",
                "title": "Improve Your Input/Output Ratio",
                "description": "You're getting less AI output relative to your input. More focused prompts could improve this ratio and give you more value.",
                "action": "ratio_tips"
            })
        elif io_ratio > 10:
            insights.append({
                "type": "token_efficiency",
                "title": "Excellent Input Leverage",
                "description": "You're getting a lot of output from minimal input - great efficiency! Your prompt style is working well.",
                "action": None
            })
    
    # 9. User Cadence Insights
    cadence = usage_patterns.get("interaction_cadence", "")
    if cadence in ["Daily user", "Regular user"]:
        insights.append({
            "type": "usage_pattern",
            "title": f"{cadence} Pattern Detected",
            "description": "Your consistent AI usage suggests it's becoming an integral tool in your workflow. Consider exploring advanced features to get even more value.",
            "action": "advanced_features"
        })
    
    # 10. Weekly Activity Pattern
    weekday_activity = usage_patterns.get("weekday_activity", {})
    if weekday_activity:
        # Determine workday vs weekend patterns
        workdays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
        weekend = {"Saturday", "Sunday"}
        
        workday_pct = sum(float(weekday_activity.get(day, 0)) for day in workdays)
        weekend_pct = sum(float(weekday_activity.get(day, 0)) for day in weekend)
        
        if weekend_pct > workday_pct / 2.5:  # Significant weekend usage
            insights.append({
                "type": "usage_pattern",
                "title": "Weekend Explorer",
                "description": "You use AI significantly on weekends, possibly for personal projects or learning. Consider setting specific weekend goals to maximize this time.",
                "action": None
            })
        elif workday_pct > 80:  # Heavy workday concentration
            insights.append({
                "type": "usage_pattern",
                "title": "Professional AI User",
                "description": "Your AI usage is heavily concentrated during workdays, suggesting it's integrated into your professional workflow.",
                "action": None
            })
    
    # Limit to top 3-5 most relevant insights
    # Sort by potential impact (this would be more sophisticated in practice)
    scored_insights = []
    for insight in insights:
        # Score each insight type by importance
        type_scores = {
            "prompt_optimization": 5,
            "conversation_flow": 4,
            "token_efficiency": 4,
            "model_selection": 3,
            "coding_pattern": 3,
            "sustainability": 2,
            "usage_pattern": 2,
            "session_pattern": 1
        }
        base_score = type_scores.get(insight["type"], 1)
        
        # Randomly vary slightly to avoid always showing same insights
        variation = random.uniform(0.8, 1.2)
        
        scored_insights.append((insight, base_score * variation))
    
    # Sort by score and take top insights
    top_insights = [insight for insight, _ in sorted(scored_insights, key=lambda x: x[1], reverse=True)]
    
    # Return top 3-5 insights, depending on how many we have
    return top_insights[:min(5, len(top_insights))]