# Mass Mentioner

Mention reddit users enmass without having to manually create all the comments.  The mentions will be in chained comments with the first sharing the same parent comment (or post if the comment is top level) of the comment that has the flag.

## Usage server side

Fill out the fields in the .env file: the `client_id` and `client_secret` come from Reddit's developed app management page, the `user_agent` is something you make up yourself in order to identify your traffic to Reddit, the `username` and `password` should be the credentials for a Reddit account that doesn't has 2-factor authentication enabled which will be used to actually do the mention posting, and `monitored_user` is the username of the account that will signal the mentioning to happen.

### Running it directly

The script uses `poetry` as the dependency manager so install that, and then run `poetry install` to install the script's dependencies.  Run `poetry run python3 mass_mentioner/mass_mentioner.py` from the base of the repo to start the script.

### Running it via Docker

It's the usual Docker stuff, yall know what to do.  As a reminder:

```sh
# calling Docker directly
docker build -t mass_mentioner:v0.1.0 .
docker run -d --rm mass_mentioner:v0.1.0
```

```sh
# using docker-compose
docker-compose up -d
```

## Usage user side

Have the monitored user post a comment in the following format:

1. Whatever text they want including newlines and whatnot.
2. `!tags\n\n`, i.e. the text '!tags' followed by two new lines.
3. However many properly formatted yaml documents.

The yaml documents are relatively flexible.

You can:
 * provide just an array of usernames
 * provide a message that ought to be posted with every batch of usernames along with the array of usernames
 * add specific notes on a per user basis
 * with multiple documents, while they will still tag in the same chain, they can have separate messages

### Examples

```yaml
---
- example
- usernames
- that_exceed
- the_limit_of_3
```

```yaml
---
- more_than

---
- one_document
```

```yaml
---
message: example message
mentions:
  - username
  - name: user
    note: personalized
```
