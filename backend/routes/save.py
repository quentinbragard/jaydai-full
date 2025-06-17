from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from supabase import create_client, Client
from utils import supabase_helpers
import dotenv
import os
from typing import List, Optional, Dict, Any

dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(prefix="/save", tags=["Save"])

class MessageData(BaseModel):
    message_provider_id: str
    content: str
    role: str
    chat_provider_id: str
    model: str = "unknown"  # Default model to "unknown"
    created_at: Optional[float] = None  # Make created_at optional
    parent_message_provider_id: Optional[str] = None

class ChatData(BaseModel):
    chat_provider_id: str
    title: str
    provider_name: str = "ChatGPT"  # Default provider to ChatGPT

class UserMetadataData(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    pinned_folder_ids: Optional[List[str]] = None
    preferences_metadata: Optional[Dict[str, Any]] = None
    additional_email: Optional[str] = None
    additional_organization: Optional[str] = None
    organization_id: Optional[List[str]] = None
    linkedin_headline: Optional[str] = None
    linkedin_id: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    email: Optional[str] = None
    google_id: Optional[str] = None
    job_type: Optional[str] = None
    job_industry: Optional[str] = None
    job_seniority: Optional[str] = None
    interests: Optional[List[str]] = None
    signup_source: Optional[str] = None

class BatchMessagesRequest(BaseModel):
    messages: List[MessageData]

class BatchChatsRequest(BaseModel):
    chats: List[ChatData]

class CombinedBatchRequest(BaseModel):
    messages: Optional[List[MessageData]] = []
    chats: Optional[List[ChatData]] = []

@router.post("/message")
async def save_message(message: MessageData, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save a chat message with parent message ID support."""
    #try:
    created_at = None
    if message.created_at:
        try:
            # Handle both seconds and milliseconds timestamps
            # If timestamp is very large (milliseconds), convert to seconds
            timestamp_in_seconds = message.created_at / 1000 if message.created_at > 1e10 else message.created_at
            created_at = datetime.fromtimestamp(timestamp_in_seconds, tz=timezone.utc).isoformat()
        except Exception as e:
            print(f"Error converting timestamp {message.created_at}: {str(e)}")
            # Use current time as fallback
            created_at = datetime.now(tz=timezone.utc).isoformat()
    else:
        # If no timestamp provided, use current time
        created_at = datetime.now(tz=timezone.utc).isoformat()
        
    # Prepare data to insert
    message_data = {
        "user_id": user_id,
        "message_provider_id": message.message_provider_id,
        "content": message.content,
        "role": message.role,
        "chat_provider_id": message.chat_provider_id,
        "model": message.model,
        "created_at": created_at
    }
    
    # Add parent_message_provider_id if provided
    if message.parent_message_provider_id:
        message_data["parent_message_provider_id"] = message.parent_message_provider_id
        
    # Insert message with validated data
    response = supabase.table("messages").insert(message_data).execute()
    
    return {"success": True, "data": response.data}
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Message save error: {str(e)}")
@router.post("/chat")
async def save_chat(chat: ChatData, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save a chat session."""
    try:
        # Check if chat already exists
        existing = supabase.table("chats").select("id") \
            .eq("user_id", user_id) \
            .eq("chat_provider_id", chat.chat_provider_id) \
            .execute()
            
        if existing.data:
            # Update existing chat
            response = supabase.table("chats").update({
                "title": chat.title,
                "provider_name": chat.provider_name,
            }).eq("user_id", user_id) \
              .eq("chat_provider_id", chat.chat_provider_id) \
              .execute()
        else:
            # Create new chat
            response = supabase.table("chats").insert({
                "user_id": user_id,
                "chat_provider_id": chat.chat_provider_id,
                "title": chat.title,
                "provider_name": chat.provider_name,
            }).execute()
            
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat save error: {str(e)}")

@router.post("/user_metadata")
async def save_user_metadata(metadata: UserMetadataData, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save user metadata."""
    #try:
        # Check if metadata already exists
    existing = supabase.table("users_metadata").select("id") \
        .eq("user_id", user_id) \
        .execute()
    
    # Prepare data with validation and defaults
    update_data = {
        "additional_email": metadata.email,
    }
    
    # Only include fields that are not None
    for field in metadata.__dict__:
        if metadata.__dict__[field] is not None:
            update_data[field] = metadata.__dict__[field] 

        
    if existing.data:
        # Update existing metadata
        response = supabase.table("users_metadata").update(update_data).eq("user_id", user_id).execute()
    else:
        # Create new metadata
        update_data["user_id"] = user_id
        response = supabase.table("users_metadata").insert(update_data).execute()
        
    return {"success": True, "data": response.data}
    #except Exception as e:
   #     raise HTTPException(status_code=500, detail=f"Metadata save error: {str(e)}")

@router.post("/batch/message")
async def save_batch_messages(batch_data: BatchMessagesRequest, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save multiple messages in a single batch operation with parent message ID support."""
    #try:
    if not batch_data.messages:
        return {"success": True, "message": "No messages to save", "count": 0}
        
    # Check which message IDs already exist
    message_ids = [msg.message_provider_id for msg in batch_data.messages]
    existing_messages = {}
    
    if message_ids:
        existing_query = supabase.table("messages").select("message_provider_id") \
            .eq("user_id", user_id) \
            .in_("message_provider_id", message_ids) \
            .execute()
        
        if existing_query.data:
            for msg in existing_query.data:
                existing_messages[msg['message_provider_id']] = True
    
    # Filter out messages that already exist
    messages_to_insert = []
    skipped_messages = 0
    
    for message in batch_data.messages:
        if message.message_provider_id in existing_messages:
            skipped_messages += 1
            continue
            
        # Handle timestamp conversion
        created_at = None
        if message.created_at:
            try:
                # Convert timestamp to ISO format, handling both seconds and milliseconds
                timestamp_in_seconds = message.created_at / 1000 if message.created_at > 1e10 else message.created_at
                created_at = datetime.fromtimestamp(timestamp_in_seconds, tz=timezone.utc).isoformat()
            except Exception as e:
                # Use current time as fallback
                created_at = datetime.now(tz=timezone.utc).isoformat()
        else:
            # If no timestamp provided, use current time
            created_at = datetime.now(tz=timezone.utc).isoformat()
            
        # Prepare message data
        message_data = {
            "user_id": user_id,
            "message_provider_id": message.message_provider_id,
            "content": message.content,
            "role": message.role,
            "chat_provider_id": message.chat_provider_id,
            "model": message.model,
            "created_at": created_at
        }
        
        # Add parent_message_provider_id if provided
        if hasattr(message, 'parent_message_provider_id') and message.parent_message_provider_id:
            message_data["parent_message_provider_id"] = message.parent_message_provider_id
            
        messages_to_insert.append(message_data)
    
    results = []
    if messages_to_insert:
        response = supabase.table("messages").insert(messages_to_insert).execute()
        results = response.data
    
    return {
        "success": True,
        "message": f"Saved {len(messages_to_insert)} messages, skipped {skipped_messages} existing messages",
        "saved_count": len(messages_to_insert),
        "skipped_count": skipped_messages,
        "total_count": len(batch_data.messages),
        "data": results
    }
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Message batch save error: {str(e)}")

@router.post("/batch/chat")
async def save_batch_chats(batch_data: BatchChatsRequest, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save multiple chats in a single batch operation."""
    try:
        if not batch_data.chats:
            return {"success": True, "message": "No chats to save", "count": 0}
            
        # Extract chat IDs to check for existing ones
        chat_provider_ids = [chat.chat_provider_id for chat in batch_data.chats]
        existing_chats = {}
        
        if chat_provider_ids:
            existing_query = supabase.table("chats").select("chat_provider_id") \
                .eq("user_id", user_id) \
                .in_("chat_provider_id", chat_provider_ids) \
                .execute()
            
            if existing_query.data:
                for chat in existing_query.data:
                    existing_chats[chat['chat_provider_id']] = True
        
        # Process updates and inserts
        chats_to_insert = []
        updated_chats = 0
        
        for chat in batch_data.chats:
            if chat.chat_provider_id in existing_chats:
                # Update existing chat
                supabase.table("chats").update({
                    "title": chat.title,
                    "provider_name": chat.provider_name
                }).eq("user_id", user_id) \
                  .eq("chat_provider_id", chat.chat_provider_id) \
                  .execute()
                updated_chats += 1
            else:
                # Prepare for batch insert
                chats_to_insert.append({
                    "user_id": user_id,
                    "chat_provider_id": chat.chat_provider_id,
                    "title": chat.title,
                    "provider_name": chat.provider_name
                })
        
        results = []
        if chats_to_insert:
            response = supabase.table("chats").insert(chats_to_insert).execute()
            results = response.data
        
        return {
            "success": True,
            "message": f"Saved {len(chats_to_insert)} new chats, updated {updated_chats} existing chats",
            "inserted_count": len(chats_to_insert),
            "updated_count": updated_chats,
            "total_count": len(batch_data.chats),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat batch save error: {str(e)}")

@router.post("/batch")
async def save_batch(batch_data: CombinedBatchRequest, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Save both chats and messages in a single batch operation."""
    try:
        results = {
            "messages": {"saved_count": 0, "skipped_count": 0, "total_count": 0},
            "chats": {"inserted_count": 0, "updated_count": 0, "total_count": 0}
        }
        
        # Process messages batch if present
        if batch_data.messages:
            messages_request = BatchMessagesRequest(messages=batch_data.messages)
            messages_result = await save_batch_messages(messages_request, user_id)
            results["messages"] = {
                "saved_count": messages_result.get("saved_count", 0),
                "skipped_count": messages_result.get("skipped_count", 0),
                "total_count": messages_result.get("total_count", 0)
            }
        
        # Process chats batch if present
        if batch_data.chats:
            chats_request = BatchChatsRequest(chats=batch_data.chats)
            chats_result = await save_batch_chats(chats_request, user_id)
            results["chats"] = {
                "inserted_count": chats_result.get("inserted_count", 0),
                "updated_count": chats_result.get("updated_count", 0),
                "total_count": chats_result.get("total_count", 0)
            }
        
        return {
            "success": True,
            "message": f"Processed {len(batch_data.messages or [])} messages and {len(batch_data.chats or [])} chats",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Combined batch save error: {str(e)}")