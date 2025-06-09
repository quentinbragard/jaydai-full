from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from supabase import create_client, Client
from utils import supabase_helpers
import dotenv
import os
import uuid

dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class NotificationMetadata(BaseModel):
    action_type: str
    action_title_key: str
    action_url: str

class NotificationBase(BaseModel):
    type: str
    title: str
    body: str
    metadata: Optional[NotificationMetadata] = None

class NotificationCreate(NotificationBase):
    user_id: str

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    read_at: Optional[datetime] = None

@router.get("/")
async def get_notifications(user_id: str = Depends(supabase_helpers.get_user_from_session_token)) -> List[NotificationResponse]:
    """Get all notifications for a user."""
    print("Getting notifications for user:", user_id)
    try:
        # Properly handle the query to avoid timestamp issues
        response = supabase.table("notifications") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
        
        # Ensure read_at is properly handled as None/null
        for notification in response.data:
            if notification.get('read_at') == "None":
                notification['read_at'] = None
                
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving notifications: {str(e)}")

@router.get("/unread")
async def get_unread_notifications(user_id: str = Depends(supabase_helpers.get_user_from_session_token)) -> List[NotificationResponse]:
    """Get unread notifications for a user."""
    try:
        # Use is_ for checking null values
        response = supabase.table("notifications") \
            .select("*") \
            .eq("user_id", user_id) \
            .is_("read_at", "null") \
            .order("created_at", desc=True) \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unread notifications: {str(e)}")

@router.get("/count")
async def get_notification_count(user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Get notification counts (total and unread)."""
    try:
        # Get total count
        total_response = supabase.table("notifications") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .execute()
        
        # Get unread count - using is_ for null check
        unread_response = supabase.table("notifications") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .is_("read_at", "null") \
            .execute()
        
        # Use the count from Supabase if available, or fallback to length of data array
        total_count = total_response.count if hasattr(total_response, 'count') else len(total_response.data)
        unread_count = unread_response.count if hasattr(unread_response, 'count') else len(unread_response.data)
        
        return {"total": total_count, "unread": unread_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving notification counts: {str(e)}")
@router.post("/create")
async def create_notification(notification: NotificationCreate) -> NotificationResponse:
    """Create a notification (admin endpoint)."""
    try:
        # Create notification with properly formatted timestamp handling
        data = {
            "user_id": notification.user_id,
            "type": notification.type,
            "title": notification.title,
            "body": notification.body,
            # Only include metadata if it's not None
            **({"metadata": notification.metadata} if notification.metadata else {})
        }
        
        response = supabase.table("notifications").insert(data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create notification")
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")

@router.post("/{notification_id}/read")
async def mark_notification_read(notification_id: str, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Mark a notification as read."""
    try:
        # Verify the notification belongs to the user
        verification = supabase.table("notifications") \
            .select("id") \
            .eq("id", notification_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verification.data:
            raise HTTPException(status_code=404, detail="Notification not found or doesn't belong to user")
        
        # Use properly formatted ISO timestamp
        now = datetime.now(timezone.utc).isoformat()
        response = supabase.table("notifications") \
            .update({"read_at": now}) \
            .eq("id", notification_id) \
            .execute()
        
        return {"success": True, "notification_id": notification_id, "read_at": now}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")

@router.post("/read-all")
async def mark_all_notifications_read(user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Mark all notifications as read for a user."""
    try:
        # Use properly formatted ISO timestamp
        now = datetime.now(timezone.utc).isoformat()
        
        # First, get all unread notifications to count them
        unread = supabase.table("notifications") \
            .select("id") \
            .eq("user_id", user_id) \
            .is_("read_at", "null") \
            .execute()
            
        # Then mark them all as read
        if unread.data:
            response = supabase.table("notifications") \
                .update({"read_at": now}) \
                .eq("user_id", user_id) \
                .is_("read_at", "null") \
                .execute()
            
            return {"success": True, "notifications_updated": len(unread.data)}
        
        return {"success": True, "notifications_updated": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking all notifications as read: {str(e)}")


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Delete a notification."""
    try:
        # Verify the notification belongs to the user
        verification = supabase.table("notifications") \
            .select("id") \
            .eq("id", notification_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verification.data:
            raise HTTPException(status_code=404, detail="Notification not found or doesn't belong to user")
        
        # Delete the notification
        response = supabase.table("notifications") \
            .delete() \
            .eq("id", notification_id) \
            .execute()
        
        return {"success": True, "notification_id": notification_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")