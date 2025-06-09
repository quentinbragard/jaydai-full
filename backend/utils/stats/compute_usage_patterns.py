from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from typing import Dict, List, Any, Tuple

def compute_usage_patterns(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze user interaction patterns to provide insights on usage behavior.
    
    Args:
        messages: List of message objects with timestamps, content, etc.
        
    Returns:
        Dictionary of usage pattern metrics
    """
    if not messages:
        return {
            "active_hours": {},
            "session_stats": {"avg_duration": 0, "avg_messages": 0, "count": 0},
            "weekday_activity": {},
            "prompt_length_distribution": {},
            "interaction_cadence": "N/A"
        }
    
    # Sort messages by timestamp
    sorted_msgs = sorted(messages, key=lambda m: m.get("created_at", ""))
    
    # Active hours analysis
    hours_count = defaultdict(int)
    weekday_count = defaultdict(int)
    
    # User prompt length distribution
    user_prompt_lengths = []
    
    # Identify user sessions (gaps > 30 minutes indicate new session)
    session_boundaries = []
    session_start = None
    prev_time = None
    
    for msg in sorted_msgs:
        if not msg.get("created_at"):
            continue
            
        try:
            # Parse timestamp
            timestamp = datetime.fromisoformat(msg["created_at"].replace('Z', '+00:00'))
            
            # Track hour and weekday activity
            hour = timestamp.hour
            weekday = timestamp.strftime('%A')
            hours_count[hour] += 1
            weekday_count[weekday] += 1
            
            # Track prompt lengths for user messages
            if msg.get("role") == "user" and msg.get("content"):
                user_prompt_lengths.append(len(msg["content"]))
            
            # Session analysis
            if not session_start:
                session_start = timestamp
                
            if prev_time and (timestamp - prev_time).total_seconds() > 1800:  # 30 min gap
                # Found session boundary
                session_boundaries.append((session_start, prev_time))
                session_start = timestamp
                
            prev_time = timestamp
            
        except Exception:
            continue
            
    # Add the last session
    if session_start and prev_time:
        session_boundaries.append((session_start, prev_time))
    
    # Analyze sessions
    session_durations = []
    session_msg_counts = []
    
    msg_timestamps = defaultdict(list)
    for msg in sorted_msgs:
        if msg.get("created_at") and msg.get("chat_provider_id"):
            try:
                ts = datetime.fromisoformat(msg["created_at"].replace('Z', '+00:00'))
                msg_timestamps[msg["chat_provider_id"]].append(ts)
            except Exception:
                continue
    
    for session_start, session_end in session_boundaries:
        duration = (session_end - session_start).total_seconds() / 60  # in minutes
        
        # Count messages in this session
        msgs_in_session = sum(
            1 for msg in sorted_msgs 
            if msg.get("created_at") and 
            session_start <= datetime.fromisoformat(msg["created_at"].replace('Z', '+00:00')) <= session_end
        )
        
        session_durations.append(duration)
        session_msg_counts.append(msgs_in_session)
    
    # Calculate prompt length distribution
    if user_prompt_lengths:
        p25 = np.percentile(user_prompt_lengths, 25)
        p50 = np.percentile(user_prompt_lengths, 50)
        p75 = np.percentile(user_prompt_lengths, 75)
        p90 = np.percentile(user_prompt_lengths, 90)
        
        length_distribution = {
            "min": min(user_prompt_lengths),
            "p25": p25,
            "median": p50,
            "p75": p75,
            "p90": p90,
            "max": max(user_prompt_lengths)
        }
    else:
        length_distribution = {"min": 0, "p25": 0, "median": 0, "p75": 0, "p90": 0, "max": 0}
    
    # Determine interaction cadence
    if len(session_boundaries) >= 5:
        counts_by_day = defaultdict(int)
        for start, _ in session_boundaries:
            counts_by_day[start.date()] += 1
            
        active_days = len(counts_by_day)
        total_days = (sorted_msgs[-1]["created_at"] - sorted_msgs[0]["created_at"]).days + 1
        
        if active_days / max(1, total_days) > 0.7:
            cadence = "Daily user"
        elif active_days / max(1, total_days) > 0.3:
            cadence = "Regular user"
        else:
            cadence = "Occasional user"
    else:
        cadence = "New user"
    
    # Normalize hours and weekdays
    total_msgs = len(sorted_msgs)
    hours_pct = {str(h): round(count/total_msgs*100, 1) for h, count in hours_count.items()}
    weekday_pct = {day: round(count/total_msgs*100, 1) for day, count in weekday_count.items()}
    
    return {
        "active_hours": dict(sorted(hours_pct.items(), key=lambda x: int(x[0]))),
        "session_stats": {
            "avg_duration": round(np.mean(session_durations), 2) if session_durations else 0,
            "avg_messages": round(np.mean(session_msg_counts), 2) if session_msg_counts else 0,
            "count": len(session_boundaries)
        },
        "weekday_activity": weekday_pct,
        "prompt_length_distribution": length_distribution,
        "interaction_cadence": cadence
    }