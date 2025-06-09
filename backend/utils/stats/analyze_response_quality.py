from typing import List, Dict, Any, Optional
import re
from collections import defaultdict
import numpy as np

def analyze_response_quality(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze AI responses to evaluate quality metrics.
    
    Args:
        messages: List of message objects with role, content, etc.
        
    Returns:
        Dictionary of response quality metrics
    """
    if not messages:
        return {
            "response_length_stats": {},
            "follow_up_rate": 0,
            "conversation_depth": 0,
            "information_density": 0,
            "code_snippet_stats": {}
        }
    
    # Prepare conversation threads
    conversations = defaultdict(list)
    for msg in messages:
        if msg.get("chat_provider_id"):
            conversations[msg["chat_provider_id"]].append(msg)
    
    # Sort each conversation by timestamp
    for chat_id in conversations:
        conversations[chat_id] = sorted(
            conversations[chat_id], 
            key=lambda m: m.get("created_at", "")
        )
    
    # Track AI response metrics
    ai_response_lengths = []
    follow_up_questions = 0
    total_ai_messages = 0
    code_snippets = 0
    total_code_lines = 0
    
    # Informational metrics
    links_shared = 0
    citations_count = 0
    definitions_count = 0
    
    # Iterate through conversations to analyze patterns
    max_conversation_depth = 0
    avg_conversation_depths = []
    
    for chat_id, chat_messages in conversations.items():
        # Calculate conversation depth (turns of back-and-forth)
        current_depth = 0
        for i, msg in enumerate(chat_messages):
            if msg.get("role") == "assistant":
                total_ai_messages += 1
                
                # Get content
                content = msg.get("content", "")
                
                # Response length
                if content:
                    ai_response_lengths.append(len(content))
                
                # Detect follow-up questions in AI responses
                if re.search(r'\?(\s|$)', content):
                    question_matches = re.findall(r'[.!?]\s+[A-Z].*?\?', content)
                    follow_up_questions += len(question_matches)
                
                # Code snippets
                code_blocks = re.findall(r'```[\s\S]*?```', content)
                code_snippets += len(code_blocks)
                
                # Count code lines
                for block in code_blocks:
                    total_code_lines += len(block.split('\n'))
                
                # Count links and citations
                links_shared += len(re.findall(r'https?://\S+', content))
                citations_count += len(re.findall(r'\[\d+\]|\[\w+, \d{4}\]', content))
                
                # Count definitions (explanatory patterns)
                definitions_count += len(re.findall(r':\s+\S+.*?[.!?]', content))
                
                # Conversation depth
                current_depth += 1
                max_conversation_depth = max(max_conversation_depth, current_depth)
        
        avg_conversation_depths.append(current_depth)
    
    # Compute response length distribution
    length_stats = {}
    if ai_response_lengths:
        length_stats = {
            "min": min(ai_response_lengths),
            "p25": np.percentile(ai_response_lengths, 25),
            "median": np.percentile(ai_response_lengths, 50),
            "p75": np.percentile(ai_response_lengths, 75),
            "max": max(ai_response_lengths),
            "avg": round(np.mean(ai_response_lengths), 2)
        }
    
    # Information density metric (higher is more informative)
    info_density = 0
    if total_ai_messages > 0:
        # Weighted combination of informative elements
        info_elements = (
            links_shared * 2 + 
            citations_count * 3 + 
            definitions_count * 1.5 + 
            code_snippets * 4
        )
        info_density = round(info_elements / total_ai_messages, 2)
    
    # Code snippet stats
    code_stats = {
        "frequency": round(code_snippets / max(1, total_ai_messages), 3),
        "total_snippets": code_snippets,
        "avg_lines": round(total_code_lines / max(1, code_snippets), 1) if code_snippets else 0
    }
    
    return {
        "response_length_stats": length_stats,
        "follow_up_rate": round(follow_up_questions / max(1, total_ai_messages), 2),
        "conversation_depth": round(np.mean(avg_conversation_depths), 1) if avg_conversation_depths else 0,
        "max_conversation_depth": max_conversation_depth,
        "information_density": info_density,
        "code_snippet_stats": code_stats
    }