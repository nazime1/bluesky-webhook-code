from atproto import Client, client_utils
import re
from datetime import datetime as dt, timezone, timedelta
from dateutil import parser

current_time = dt.now(timezone.utc)
client = Client()
profile = client.login('handle', 'password')
profile_feed = client.get_author_feed('handle', filter='posts_no_replies')
feed2 = []
quotefeed = {}
imagefeed = []
imagequotefeed = {}
for feed_view in profile_feed.feed:
    post_url = re.sub(r'at://did:plc:your-uri/app.bsky.feed.post/', r'https://bsky.app/profile/did:plc:your-uri/post/', feed_view.post.uri)
    post_url = re.sub(r'did:plc:your-uri', r'handle', post_url)    
    post_time = parser.isoparse(feed_view.post.record.created_at)
    if 'your-uri' in feed_view.post.uri and max(post_time, current_time - timedelta(hours=1)) == post_time:
        if feed_view.post.record.embed != None:
            if hasattr(feed_view.post.record.embed, 'media'):
                post_fetched = client.get_posts([feed_view.post.record.embed.record.record.uri])
                display_name = post_fetched.posts[0].author.display_name
                quoted_text = post_fetched.posts[0].record.text
                feed_view.post.uri = post_url
                imagequotefeed.update({(quoted_text, display_name) : feed_view})
            elif hasattr(feed_view.post.record.embed, 'images'):
                feed_view.post.uri = post_url
                imagefeed.append(feed_view)            
            elif hasattr(feed_view.post.record.embed, 'record'):
                post_fetched = client.get_posts([feed_view.post.record.embed.record.uri])
                display_name = post_fetched.posts[0].author.display_name 
                quoted_text = post_fetched.posts[0].record.text
                feed_view.post.uri = post_url
                quotefeed.update({(quoted_text, display_name) : feed_view})
        else:
            feed_view.post.record.uri = post_url
            feed2.append(feed_view)
