from supabase import create_client, Client
import dotenv
import os
from datetime import datetime, timezone
import uuid

dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

class NotificationService:
    """Service for creating and managing system notifications."""
    
    @staticmethod
    async def create_welcome_notification(user_id: str, username: str = ""):
        """
        Create a welcome notification for new users with LinkedIn follow button.
        Should be called when a user first signs up.
        """
        try:
            # Check if user already has this notification
            existing_notification = supabase.table("notifications") \
                .select("id") \
                .eq("user_id", user_id) \
                .eq("type", "welcome_new_user") \
                .execute()
            
            # If no existing welcome notification
            if len(existing_notification.data) == 0:
                # Create the notification
                notification = {
                    "user_id": user_id,
                    "type": "welcome_new_user",
                    "title": "welcome_notification_title", # Use localization key
                    "body": "welcome_notification_body", # Use localization key with personalization
                    "metadata": {
                        "action_type": "openLinkedIn",
                        "action_title_key": "followOnLinkedIn",
                        "action_url": "https://www.linkedin.com/company/104914264/admin/dashboard/"
                    }
                }
                
                print("notification", notification)
                # Insert notification
                supabase.table("notifications").insert(notification).execute()
                return True
                
            return False
        except Exception as e:
            print(f"Error creating welcome notification: {str(e)}")
            return False

    
    @staticmethod
    async def create_notification(user_id: str, notification_type: str, title: str, body: str, metadata: str = None):
        """Create a notification for a user."""
        try:
            notification = {
                "user_id": user_id,
                "type": notification_type,
                "title": title,
                "body": body,
                "metadata": metadata
            }
            
            response = supabase.table("notifications").insert(notification).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating notification: {str(e)}")
            return None
    