import httpx
import json
from webhook import feed2, quotefeed
from datetime import datetime as dt, timezone
from dateutil import parser
import pytz

if len(feed2) > 0:
    for feed_post in feed2:
        post_time = parser.isoparse(feed_post.post.record.created_at)
        est = pytz.timezone('US/Eastern')
        post_time = post_time.astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        response = httpx.post(
            r"webhook_token",
            data={"payload_json": json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": "bsky-icon-url"
                    },
                    "title": "New Bluesky Post!",
                    "url": feed_post.post.uri,
                    "description": feed_post.post.record.text,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png"
                        }
                    }]
                })}
            )
        # raise an exception if the operation failed.
        response.raise_for_status()

if len(quotefeed) > 0:
    for feed_post in quotefeed:
        post_time = parser.isoparse(quotefeed[feed_post].post.record.created_at)
        est = pytz.timezone('US/Eastern')
        post_time = post_time.astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        post_string = f"{quotefeed[feed_post].post.record.text}\n\nQuoting\n> {feed_post}"
        response = httpx.post(
            r"webhook_token",
            data={"payload_json": json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": "bsky-icon-url"
                    },
                    "title": "New Bluesky Post!",
                    "url": str(quotefeed[feed_post].post.uri),
                    "description": post_string,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png"
                        }
                    }]
                })}
            )
        # raise an exception if the operation failed.
        response.raise_for_status()
        
if len(imagefeed) > 0:
    for feed_post in imagefeed:
        post_time = parser.isoparse(feed_post.post.record.created_at)
        est = pytz.timezone('US/Eastern')
        post_time = post_time.astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        json_string = json.dumps({
            "embeds": [{
                "author": {
                    "name": "your-name",
                    "url": "handle",
                    "icon_url": "bsky-icon-url"
                },
                "title": "New Bluesky Post!",
                "url": feed_post.post.uri,
                "description": feed_post.post.record.text,
                "footer": {
                    "text": time_string,
                    "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png"
                    },
                "image": {
                    "url": feed_post.post.embed.images[0].fullsize
                    }
                }]
            })
        image_json = ""
        for i in range(1, len(feed_post.post.embed.images)):
            json_string2 = json.dumps({
                "url": feed_post.post.uri,
                "image": {
                    "url": feed_post.post.embed.images[i].fullsize
                    }
                })
            image_json = image_json + json_string2
        json_merged = json_string[:-2] + "," + image_json + "]}"
        response = httpx.post(
        r"webhook_token",
        data={"payload_json": json_merged})
        response.raise_for_status()
        


