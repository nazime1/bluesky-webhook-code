import httpx
from webhook import feed2

most_recent_post = feed2[0].post.uri
response = httpx.post(
    r"https://discord.com/api/webhooks/123/webhook_token",
json={
    "content": f"New Bluesky post! {most_recent_post}",
    }
)
# raise an exception if the operation failed.
response.raise_for_status()
