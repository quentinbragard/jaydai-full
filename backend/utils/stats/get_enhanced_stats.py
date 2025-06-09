from fastapi import HTTPException
from datetime import datetime, timedelta
import dotenv
import os
from supabase import create_client, Client
from utils.supabase_helpers import get_user_from_session_token
from utils.stats.estimate_tokens import estimate_tokens
from utils.stats.compute_usage_patterns import compute_usage_patterns
from utils.stats.analyze_response_quality import analyze_response_quality
from utils.stats.calculate_efficiency_score import calculate_efficiency_score
from utils.stats.generate_personalized_insights import generate_personalized_insights

# Energy cost constants (in joules per token)
ENERGY_COST_PER_INPUT_TOKEN = 0.0003
ENERGY_COST_PER_OUTPUT_TOKEN = 0.0006
JOULES_PER_WH = 3600

# Convert energy usage in Wh to user-friendly equivalents
def energy_to_equivalent(wh: float) -> str:
    if wh < 0.05:
        return "équivaut à allumer une LED pendant quelques secondes"
    elif wh < 0.2:
        return "équivaut à allumer une LED pendant une minute"
    elif wh < 1:
        return "équivaut à une minute de vidéo YouTube"
    else:
        return "équivaut à quelques minutes d’ordinateur portable"

async def get_enhanced_user_stats(user_id):
    supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
    """
    Enhanced analytics endpoint that provides comprehensive user stats and insights.
    Includes advanced metrics for AI interaction quality, user behavior patterns,
    personalized insights, and an improved efficiency score.
    """
    try:
        current_date = datetime.now()
        last_week_date = current_date - timedelta(days=7)
        current_date_str = current_date.strftime('%Y-%m-%d')
        last_week_date_str = last_week_date.strftime('%Y-%m-%d')

        # Get chats
        chats_response = supabase.table("chats").select("id, created_at").eq("user_id", user_id).execute()
        chats = chats_response.data
        total_chats = len(chats)
        recent_chats = [c for c in chats if c.get("created_at", "") >= last_week_date_str]
        recent_chats_count = len(recent_chats)

        # Get messages with extended data
        messages_response = supabase.table("messages").select(
            "id, chat_provider_id, role, content, created_at, parent_message_provider_id, message_provider_id, model"
        ).eq("user_id", user_id).execute()
        messages = messages_response.data
        total_messages = len(messages)

        # Calculate basic stats (similar to original function)
        # Average messages per chat
        conv_msg_counts = {}
        for m in messages:
            cid = m.get("chat_provider_id")
            if cid:
                conv_msg_counts[cid] = conv_msg_counts.get(cid, 0) + 1
        avg_messages_per_chat = round(total_messages / total_chats, 2) if total_chats else 0

        # Use enhanced token estimation
        recent_input, recent_output, all_input, all_output = 0, 0, 0, 0
        recent_messages = [m for m in messages if m.get("created_at", "") >= last_week_date_str]

        for msg in messages:
            model = msg.get("model", "default")
            tokens = estimate_tokens(msg.get("content", ""), model)
            if msg.get("role") == "user":
                all_input += tokens
                if msg in recent_messages:
                    recent_input += tokens
            else:
                all_output += tokens
                if msg in recent_messages:
                    recent_output += tokens

        all_tokens = all_input + all_output
        recent_tokens = recent_input + recent_output

        # Calculate energy usage
        all_energy_wh = (all_input * ENERGY_COST_PER_INPUT_TOKEN + all_output * ENERGY_COST_PER_OUTPUT_TOKEN) / JOULES_PER_WH
        recent_energy_wh = (recent_input * ENERGY_COST_PER_INPUT_TOKEN + recent_output * ENERGY_COST_PER_OUTPUT_TOKEN) / JOULES_PER_WH

        # Calculate thinking time (same as original)
        thinking_times = []
        msg_lookup = {m.get("message_provider_id"): m for m in messages if m.get("message_provider_id")}

        for msg in messages:
            if msg.get("role") == "assistant" and msg.get("parent_message_provider_id") and msg.get("created_at"):
                parent_msg = msg_lookup.get(msg["parent_message_provider_id"])
                if parent_msg and parent_msg.get("created_at"):
                    try:
                        t1 = datetime.fromisoformat(msg["created_at"].replace('Z', '+00:00'))
                        t0 = datetime.fromisoformat(parent_msg["created_at"].replace('Z', '+00:00'))
                        diff = (t1 - t0).total_seconds()
                        if 0.1 <= diff <= 60:
                            thinking_times.append(diff)
                    except Exception:
                        pass

        avg_thinking_time = round(sum(thinking_times) / len(thinking_times), 2) if thinking_times else 2.5
        total_thinking_time = round(sum(thinking_times), 2) if thinking_times else round(avg_thinking_time * total_messages, 2)

        # Message count per day (last 7 days)
        messages_per_day = { (current_date - timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(7) }
        for msg in messages:
            if msg.get("created_at"):
                date = msg["created_at"].split('T')[0]
                if date in messages_per_day:
                    messages_per_day[date] += 1

        # Get model usage stats
        model_usage = {}
        for msg in messages:
            model = msg.get("model", "unknown")
            if model not in model_usage:
                model_usage[model] = {"count": 0, "input_tokens": 0, "output_tokens": 0}
            model_usage[model]["count"] += 1
            tok = estimate_tokens(msg.get("content", ""), model)
            if msg.get("role") == "user":
                model_usage[model]["input_tokens"] += tok
            else:
                model_usage[model]["output_tokens"] += tok

        # ======= NEW ENHANCED ANALYTICS =======
        
        # 1. Usage Patterns Analysis
        usage_patterns = compute_usage_patterns(messages)
        
        # 2. Response Quality Analysis
        response_quality = analyze_response_quality(messages)
        
        # 3. New Enhanced Efficiency Score
        token_usage_dict = {
            "recent": recent_tokens,
            "recent_input": recent_input,
            "recent_output": recent_output,
            "total": all_tokens,
            "total_input": all_input,
            "total_output": all_output
        }
        
        energy_usage_dict = {
            "recent_wh": round(recent_energy_wh, 4),
            "total_wh": round(all_energy_wh, 4),
            "per_message_wh": round(all_energy_wh / total_messages, 6) if total_messages else 0,
            "equivalent": energy_to_equivalent(all_energy_wh)
        }
        
        efficiency_score = calculate_efficiency_score(
            messages=messages,
            chats=chats,
            response_quality=response_quality,
            usage_patterns=usage_patterns
        )
        
        # 4. Generate Personalized Insights
        insights = generate_personalized_insights(
            efficiency_score=efficiency_score,
            response_quality=response_quality,
            usage_patterns=usage_patterns,
            token_usage=token_usage_dict,
            energy_usage=energy_usage_dict
        )

        # Return comprehensive stats
        return {
            # Basic stats (compatible with original endpoint)
            "total_chats": total_chats,
            "recent_chats": recent_chats_count,
            "total_messages": total_messages,
            "avg_messages_per_chat": avg_messages_per_chat,
            "messages_per_day": messages_per_day,
            "token_usage": token_usage_dict,
            "energy_usage": energy_usage_dict,
            "thinking_time": {
                "average": avg_thinking_time,
                "total": total_thinking_time
            },
            "model_usage": model_usage,
            "efficiency": efficiency_score["overall_score"],
            
            # Enhanced analytics data
            "enhanced_analytics": {
                "usage_patterns": usage_patterns,
                "response_quality": response_quality,
                "efficiency_details": efficiency_score,
                "personalized_insights": insights
            }
        }

    except Exception as e:
        print(f"Error getting enhanced user stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting enhanced user stats: {str(e)}")