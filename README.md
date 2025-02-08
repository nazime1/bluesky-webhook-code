# Bluesky Webhook intended for Discord
All the bots for Discord run awfully slow or are paid so I coded this in a few hours. I might improve on it someday (like make embeds look nicer) but for now it's functional and that's what matters.
# How to Run
1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. Create a [Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in the server that you want to set the webhook up in and copy the URL. Also customize the webhook (name, profile picture) if you want.
4. Replace 'handle' with your handle, 'password' with your password (highly recommend using the App Password feature for this, it's under Settings -> Privacy and Security), 'your-uri' with your Bluesky URI, and 'webhook_token' with the webhook URL. Your Bluesky URI can be found with a little playing with the API.
5. Run `python3 backend.py`, and it'll work like a charm! If you want it to run on a schedule, I do recommend setting up a Github Action. There's a Python template that you can modify fairly easily. 

If you have any questions, commments or concerns, feel free to [open an issue](https://github.com/nazime1/bluesky-webhook-code/issues/new?template=Blank+issue)!
