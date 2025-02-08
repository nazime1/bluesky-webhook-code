import httpx
from webhook import feed2

if len(feed2) > 0:
    for feed_post in feed2:
    response = httpx.post(
        r"https://discord.com/api/webhooks/123/webhook_token",
        json={
            "content": f"New Bluesky post! {most_recent_post}",
            }
        )
        # raise an exception if the operation failed.
        response.raise_for_status()
