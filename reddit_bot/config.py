import praw
from dotenv import load_dotenv
import os
import logging

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
username = os.getenv("username")
password = os.getenv("password")
user_agent = os.getenv("user_agent")

def authenticateReddit():
    try:
        reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
        check_for_async=False,  # Disable async checks (sync-only mode)
        ratelimit_seconds=300,  # Add rate limit buffer
        )
        if reddit.user.me() is None:
            raise ValueError("Authentication failed. Please check credentials.")
        logging.info(f"Authenticated as {reddit.user.me()}")
        return reddit
    except Exception as e:
        logging.error(f"Error during Reddit authentication: {e}")
        raise