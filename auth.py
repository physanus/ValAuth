#!/usr/bin/env python3

import cloudscraper
import json
import os
import re


def auth(username, password):
    # print(f'Initiating auth for user \'{username}\' pass \'{password}\'')

    scraper = cloudscraper.create_scraper()
    # scraper.debug = True

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Content-Type': 'application/json',
    }

    # Request 1 - Setup cookies
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    result = scraper.post('https://auth.riotgames.com/api/v1/authorization', headers=headers, json=data)
    if result.status_code != 200:
        print('Error in request 1: ' + str(result.status_code))
        scraper.close()
        exit(2)

    # Request 2 - Retrieve the access_token
    data = {
        'type': 'auth',
        'username': username,
        'password': password,
    }
    result = scraper.put('https://auth.riotgames.com/api/v1/authorization', headers=headers, json=data)
    if result.status_code != 200:
        print('Error in request 1: ' + str(result.status_code))
        scraper.close()
        exit(3)

    re_pattern = re.compile(
        'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    try:
        re_data = re_pattern.findall(json.loads(result.text)['response']['parameters']['uri'])[0]
    except KeyError:
        print('Error in request 1: ' + str(result.status_code))
        scraper.close()
        exit(4)


    access_token = re_data[0]
    id_token = re_data[1]
    expires_in = re_data[2]
    print(f'access_token={access_token}')
    headers['Authorization'] = f'Bearer {access_token}'

    # Request 3 - Retrieve the entitlements_token
    result = scraper.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers)
    if result.status_code != 200:
        print('Error in request 1: ' + str(result.status_code))
        scraper.close()
        exit(5)

    entitlements_token = json.loads(result.text)['entitlements_token']
    print(f'entitlements_token={entitlements_token}')
    headers['X-Riot-Entitlements-JWT'] = entitlements_token

    # Request 4 - Retrieve the user_id
    result = scraper.post('https://auth.riotgames.com/userinfo', headers=headers)
    if result.status_code != 200:
        print('Error in request 1: ' + str(result.status_code))
        scraper.close()
        exit(6)

    user_id = json.loads(result.text)['sub']
    print(f'user_id={user_id}')

    scraper.close()


if __name__ == '__main__':
    username = os.getenv('VAL_USER')
    password = os.getenv('VAL_PASS')

    if not username or not password:
        print("Error: You need to specify the env variables 'VAL_USER' and 'VAL_PASS'.")
        exit(1)

    auth(username, password)
