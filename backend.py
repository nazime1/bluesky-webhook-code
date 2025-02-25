import httpx
import json
import re
from webhook import feed2, quotefeed, imagefeed, imagequotefeed, videofeed, giffeed
from dateutil import parser
from zoneinfo import ZoneInfo
import m3u8_To_MP4

est = ZoneInfo('America/New_York')

if len(feed2) > 0:
    for feed_post in feed2:
        post_time = parser.isoparse(feed_post.post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        response = httpx.post(
            r"webhook_token",
            data={"payload_json": json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": feed_post.post.author.avatar
                    },
                    "title": "New Bluesky Post!",
                    "url": feed_post.post.uri,
                    "description": feed_post.post.record.text,
                    "color": 1147902,
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
        post_time = parser.isoparse(quotefeed[feed_post].post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        quoted_post = '\n'.join('> ' + line for line in feed_post[0].split('\n'))
        post_string = f"{quotefeed[feed_post].post.record.text}\n\nQuoting {feed_post[1]}\n{quoted_post}"
        response = httpx.post(
            r"webhook_token",
            data={"payload_json": json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": feed_post.post.author.avatar
                    },
                    "title": "New Bluesky Post!",
                    "url": str(quotefeed[feed_post].post.uri),
                    "description": post_string,
                    "color": 1147902,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png" 
                        }
                    }]
                })}
            )
        response.raise_for_status()
       
        
if len(imagefeed) > 0:
    for feed_post in imagefeed:
        post_time = parser.isoparse(feed_post.post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        json_string = json.dumps({
            "embeds": [{
                "author": {
                    "name": "your-name",
                    "url": "handle",
                    "icon_url": feed_post.post.author.avatar
                },
                "title": "New Bluesky Post!",
                "url": feed_post.post.uri,
                "description": feed_post.post.record.text,
                "color": 1147902,
                "footer": {
                    "text": time_string,
                    "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png"
                    },
                "image": {
                    "url": feed_post.post.embed.images[0].fullsize
                    }
                }] + 
                [
                    {
                        "url": feed_post.post.uri,
                        "image": {
                            "url": image.fullsize
                            }
                    } for image in feed_post.post.embed.images[1:]
                ]
            })
        response = httpx.post(
            r"webhook_token",
            data={"payload_json": json_string})
        response.raise_for_status()

if len(imagequotefeed) > 0:
    for feed_post in imagequotefeed:
        post_time = parser.isoparse(imagequotefeed[feed_post].post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        quoted_post = '\n'.join('> ' + line for line in feed_post[0].split('\n'))
        post_string = f"{imagequotefeed[feed_post].post.record.text}\n\nQuoting {feed_post[1]}\n{quoted_post}"
        json_string = json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": feed_post.post.author.avatar
                    },
                    "title": "New Bluesky Post!",
                    "url": str(imagequotefeed[feed_post].post.uri),
                    "description": post_string,
                    "color": 1147902,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png" 
                        },
                    "image": {
                        "url": imagequotefeed[feed_post].post.embed.media.images[0].fullsize
                        }
                    }] + [
                        {
                            "url": str(imagequotefeed[feed_post].post.uri),
                            "image": {
                                "url": image.fullsize
                            }
                        } for image in imagequotefeed[feed_post].post.embed.media.images[1:]
                    ]
                })
        response=httpx.post(
            r"webhook_token",
            data={"payload_json": json_string})
        response.raise_for_status()
        
if len(videofeed) > 0:
       for feed_post in videofeed:
        post_time = parser.isoparse(feed_post.post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        video_string = "http://video.cdn.bsky.app/hls/did:plc:cargf4lbxd6cg25d637gt2c3/" + feed_post.post.record.embed.video.ref.link + "/playlist.m3u8"
        m3u8_To_MP4.multithread_download(video_string)
        with open("m3u8_To_MP4.mp4", "rb") as io_object:
            json_string = json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": feed_post.post.author.avatar
                    },
                    "title": "New Bluesky Post!",
                    "color": 1147902,
                    "url": feed_post.post.uri,
                    "description": feed_post.post.record.text,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png"
                        },
                    "video": {
                        "url": "attachment://m3u8_To_MP4.mp4"                    
                        }
                    }]
                })
            response = httpx.post(
                r"https://discord.com/api/webhooks/1337872985926795316/vTCP0xC5rA0-Z8fD9j_yr79Dzs_TN-gagj0do0qLY07vQ_eZZhcYMf9qgw-cc_5WtuoF",
                data={"payload_json": json_string}, files={"filetag": ("m3u8_To_MP4.mp4", io_object, "video/mp4")})
            response.raise_for_status()       

if len(giffeed) > 0:
    for feed_post in giffeed:
        post_time = parser.isoparse(feed_post.post.record.created_at).astimezone(est)
        time_string = "Posted on {:%B %d, %Y} at {:%H:%M}".format(post_time, post_time)
        json_string = json.dumps({
                "embeds": [{
                    "author": {
                        "name": "your-name",
                        "url": "handle",
                        "icon_url": feed_post.post.author.avatar
                    },
                    "title": "New Bluesky Post!",
                    "color": 1147902,
                    "url": feed_post.post.uri,
                    "description": feed_post.post.record.text,
                    "footer": {
                        "text": time_string,
                        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1200px-Bluesky_Logo.svg.png" 
                        },
                    "image": {
                        "url": feed_post.post.embed.external.uri
                        }
                    }]
                })
        response=httpx.post(
            r"https://discord.com/api/webhooks/1337872985926795316/vTCP0xC5rA0-Z8fD9j_yr79Dzs_TN-gagj0do0qLY07vQ_eZZhcYMf9qgw-cc_5WtuoF",
            data={"payload_json": json_string})
        response.raise_for_status()

