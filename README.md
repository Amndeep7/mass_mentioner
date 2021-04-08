# Mass Mentioner

Mention reddit users enmass without having to manually create all the comments.

## Usage server side

Fill out the fields in the .env file: the `client_id` and `client_secret` come from Reddit's developed app management page, the `user_agent` is something you make up yourself in order to identify your traffic to Reddit, the `username` and `password` should be the credentials for a Reddit account that doesn't has 2-factor authentication enabled which will be used to actually do the mention posting, and `monitored_user` is the username of the account that will signal the mentioning to happen.

### Running it directly

The script uses `poetry` as the dependency manager so install that, and then run `poetry install` to install the script's dependencies.  Run `poetry run python3 mass_mentioner/mass_mentioner.py` from the base of the repo to start the script.

### Running it via Docker

Instructions coming soon(tm) for both running it directly via docker and via docker-compose.
