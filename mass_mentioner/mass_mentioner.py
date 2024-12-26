from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from itertools import islice
from os import getenv
from types import SimpleNamespace
import asyncio

from dotenv import dotenv_values
from yaml import safe_load_all
import asyncpraw

ALLOWED_TIME_DELTA_IN_SECONDS = 300 # 5 min

def chunk(iterable, size):
    it = iter(iterable)
    return iter(lambda: tuple(islice(it, size)), ())

async def main():
    config = SimpleNamespace(**dotenv_values(".env"))

    reddit = asyncpraw.Reddit(
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent,
            username = config.username,
            password = config.password
            )

    me = await reddit.redditor(config.monitored_user)
    async for comment in me.stream.comments(skip_existing=True):
        if "!tags" not in comment.body:
            continue

        if (datetime.now(timezone.utc).timestamp() - comment.created_utc) >= ALLOWED_TIME_DELTA_IN_SECONDS:
            continue

        documents = comment.body.split("!tags\n\n", 1)[1]

        parent = await comment.parent()
        print(parent)

        for doc in safe_load_all(documents):
            for batch in (chunk(doc["mentions"], 3) if isinstance(doc, Mapping) and "mentions" in doc
                    else chunk(doc, 3) if isinstance(doc, Sequence) else []):
                message = f"{doc['message']}\n\n" if isinstance(doc, Mapping) and "message" in doc else ""

                for mention in batch:
                    if isinstance(mention, Mapping):
                        if "name" in mention:
                            message += f"/u/{mention['name']}"
                            if "note" in mention:
                                message += f" - {mention['note']}"
                    else:
                        message += f"/u/{mention}"
                    message += "\n\n"

                message.strip()

                parent = await parent.reply(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
