# ValAuth
A Riot Games / Valorant auth provider for use in shell scripts

# Motivation
So far, I only found [this](https://github.com/HeyM1ke/ValorantClientAPI/blob/master/Docs/RSO_AuthFlow.py) 
authentication wrapper that is capable of generating an `access_token`, `entitlements_token` and `user_id`. However, 
that script broke in the meantime and was still broken after applying
[some adjustments](https://github.com/HeyM1ke/ValorantClientAPI/issues/28#issuecomment-1059647354).

[Other projects](https://github.com/staciax/Valorant-DiscordBot/issues/57) do suffer from this, too.

As a result, I looked into this issue and found [a solution on Stack Overflow](https://stackoverflow.com/a/49088162).
The problem seems to be a (recently introduced) recently added security-measure by Cloudflare on Riots servers:
```
This is due to the fact that the page uses Cloudflare's anti-bot page (or IUAM).
Bypassing this check is quite difficult to solve on your own, since Cloudflare changes their techniques periodically.
Currently, they check if the client supports JavaScript, which can be spoofed.
```
[source](https://stackoverflow.com/a/49088162)

Also:
```
[The cloudscraper] does not require Node.js dependency
```
[source](https://stackoverflow.com/a/60884613)

This projects implements the changes on top of the authentication scheme provided by both 
[ValorantClientAPI](ValorantClientAPI) and [Postman](https://www.postman.com/flight-astronomer-35971560/workspace/riot-auth/documentation/19680348-ebef585d-d9a4-42ad-a33b-e0a3e67e0d08).

# Prerequisites
- You need to have 2fa **disabled** on your Riot Account ([click here](https://account.riotgames.com/#mfa-card) to do so).
- You need either python or docker installed on your system.

# How to run
## Vanilla
```
$ pip3 install -r requirements.txt
$ VAL_USER=username VAL_PASS=password python3 auth.py
```

## Docker
```
docker run \
  --rm \
  -it \
  -e VAL_USER='username' \
  -e VAL_PASS='password' \
  --entrypoint ash \
  -v "$(pwd):/app" \
  python:3-alpine \
  -c 'cd /app && pip3 install -r requirements.txt >/dev/null 2>&1 && python3 auth.py'
```

