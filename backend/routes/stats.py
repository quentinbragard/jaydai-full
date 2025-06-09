from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import dotenv
import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
from utils.supabase_helpers import get_user_from_session_token
from utils.stats.get_enhanced_stats import get_enhanced_user_stats

# Initialize Supabase client
dotenv.load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)

# Energy cost constants (in joules per token)
ENERGY_COST_PER_INPUT_TOKEN = 0.0003
ENERGY_COST_PER_OUTPUT_TOKEN = 0.0006
JOULES_PER_WH = 3600

# Estimate tokens based on message content length
def estimate_tokens(content):
    if not content:
        return 0
    return len(content) // 4

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


@router.get("/user")
async def get_user_stats(user_id: str = Depends(get_user_from_session_token)):
    try:
        current_date = datetime.now()
        last_week_date = current_date - timedelta(days=7)
        current_date_str = current_date.strftime('%Y-%m-%d')
        last_week_date_str = last_week_date.strftime('%Y-%m-%d')

        # Get total and recent chat counts
        chats_response = supabase.table("chats").select("id").eq("user_id", user_id).execute()
        total_chats = len(chats_response.data)

        recent_chats_response = supabase.table("chats") \
            .select("id, created_at") \
            .eq("user_id", user_id) \
            .gte("created_at", last_week_date_str) \
            .execute()
        recent_chats = len(recent_chats_response.data)

        # Get messages
        messages_response = supabase.table("messages").select(
            "id, chat_provider_id, role, content, created_at, parent_message_provider_id, message_provider_id, model"
        ).eq("user_id", user_id).execute()
        messages = messages_response.data
        total_messages = len(messages)

        # Average messages per chat
        conv_msg_counts = {}
        for m in messages:
            cid = m.get("chat_provider_id")
            if cid:
                conv_msg_counts[cid] = conv_msg_counts.get(cid, 0) + 1
        avg_messages_per_chat = round(total_messages / total_chats, 2) if total_chats else 0

        # Token and energy usage
        recent_input, recent_output, all_input, all_output = 0, 0, 0, 0
        recent_messages = [m for m in messages if m.get("created_at", "") >= last_week_date_str]

        for msg in messages:
            tokens = estimate_tokens(msg.get("content", ""))
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

        all_energy_wh = (all_input * ENERGY_COST_PER_INPUT_TOKEN + all_output * ENERGY_COST_PER_OUTPUT_TOKEN) / JOULES_PER_WH
        recent_energy_wh = (recent_input * ENERGY_COST_PER_INPUT_TOKEN + recent_output * ENERGY_COST_PER_OUTPUT_TOKEN) / JOULES_PER_WH

        # Thinking time
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

        # Efficiency score
        messages_score = 100 - min(abs(avg_messages_per_chat - 5) * 10, 100)
        token_score = (all_output / all_input * 100) if all_input else 50
        response_time_score = 100 - min((avg_thinking_time / 3) * 10, 100)
        energy_per_token_mwh = (all_energy_wh * 1000) / all_tokens if all_tokens else 0
        energy_score = 100 - min(energy_per_token_mwh * 10, 100)
        efficiency_score = round((messages_score + token_score + response_time_score + energy_score) / 4)

        # Model usage
        model_usage = {}
        for msg in messages: 
            model = msg.get("model", "unknown")
            if model not in model_usage:
                model_usage[model] = {"count": 0, "input_tokens": 0, "output_tokens": 0}
            model_usage[model]["count"] += 1
            tok = estimate_tokens(msg.get("content", ""))
            if msg.get("role") == "user":
                model_usage[model]["input_tokens"] += tok
            else:
                model_usage[model]["output_tokens"] += tok
        chats_per_day = { (current_date - timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(7) }
        for chat in chats_response.data:
            if chat.get("created_at"):
                date = chat["created_at"].split('T')[0]
                if date in chats_per_day:
                    chats_per_day[date] += 1

        # Convert date strings to datetime objects for sorting
        chats_per_day = {datetime.strptime(date, '%Y-%m-%d'): count for date, count in chats_per_day.items()}
        
        # Sort chats_per_day by date (earliest first, latest last)
        chats_per_day = dict(sorted(chats_per_day.items()))

        # Convert datetime objects back to date strings
        chats_per_day = {date.strftime('%Y-%m-%d'): count for date, count in chats_per_day.items()}

        return {
            "total_chats": total_chats,
            "recent_chats": recent_chats,
            "total_messages": total_messages,
            "avg_messages_per_chat": avg_messages_per_chat,
            "messages_per_day": messages_per_day,
            "chats_per_day": chats_per_day,
            "token_usage": {
                "recent": recent_tokens,
                "recent_input": recent_input,
                "recent_output": recent_output,
                "total": all_tokens,
                "total_input": all_input,
                "total_output": all_output
            },
            "energy_usage": {
                "recent_wh": round(recent_energy_wh, 4),
                "total_wh": round(all_energy_wh, 4),
                "per_message_wh": round(all_energy_wh / total_messages, 6) if total_messages else 0,
                "equivalent": energy_to_equivalent(all_energy_wh)
            },
            "thinking_time": {
                "average": avg_thinking_time,
                "total": total_thinking_time
            },
            "efficiency": efficiency_score,
            "model_usage": model_usage
        }

    except Exception as e:
        print(f"Error getting user stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting user stats: {str(e)}")
    
@router.get("/user/enhanced")
async def get_enhanced_user_stats_endpoint(user_id: str = Depends(get_user_from_session_token)):
    return await get_enhanced_user_stats(user_id)
