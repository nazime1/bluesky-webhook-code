from atproto import Client, client_utils
import re
from datetime import datetime as dt, timezone, timedelta
from dateutil import parser

current_time = dt.now(timezone.utc)
client = Client()
profile = client.login('handle', 'password')
profile_feed = client.get_author_feed('handle', filter='posts_no_replies')
feed2 = []
for feed_view in profile_feed.feed:
    post_time = parser.isoparse(feed_view.post.record.created_at)
    if 'your-uri' in feed_view.post.uri and max(post_time, current_time - timedelta(hours=1)) == post_time:
        feed2.append(feed_view)
        
for feed_view in feed2:
    feed_view.post.uri = re.sub(r'at://did:plc:your-uri/app.bsky.feed.post/', r'https://bsky.app/profile/did:plc:your-uri/post/', feed_view.post.uri)
    feed_view.post.uri = re.sub(r'did:plc:cargf4lbxd6cg25d637gt2c3', r'handle.', feed_view.post.uri)
