import configparser
import random
import string
import logging

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('./bot.log'))

SETTINGS_PATH = './bot_settings.ini'
API_URL = 'http://127.0.0.1:8000'


def generate_string(symbols, length):
    return ''.join([random.choice(symbols) for _ in range(length)])


def generate_user_credentials():
    symbols = f'{string.ascii_letters}{string.digits}{string.punctuation}'
    password = generate_string(symbols, 15)

    name = generate_string(string.ascii_lowercase, 7)
    email = f'{name}@mail.com'
    return {
        'email': email,
        'password': password,
    }


def send_request(request_url, method, **kwargs):
    try:
        request_method = getattr(requests, method)

        logger.debug(f'Request to the API. METHOD:{method}, URL:{request_url}, PAYLOAD:{kwargs}')
        response = request_method(request_url, **kwargs)
        logger.debug(f'Response from the API. STATUS:{response.status_code}, RESPONSE:{response.json()}')

        return response.json()
    except (IOError, TypeError, AttributeError, IndexError, ValueError) as e:
        logger.error(f'{e.__class__.__name__}: {e}')


def print_result(action, response, value, message):
    if response == value:
        print(f'[OK] {action}: {message}')
    else:
        print(f'[ERROR] {action}: {message}')


if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read(SETTINGS_PATH)

    number_of_users = settings.getint('ROOT', 'number_of_users')
    max_posts_per_user = settings.getint('ROOT', 'max_posts_per_user')
    max_likes_per_user = settings.getint('ROOT', 'max_likes_per_user')

    users = []
    for _ in range(number_of_users):
        users.append({
            'credentials': generate_user_credentials(),
            'token': '',
        })

    posts = []

    for user in users:
        credentials = user.get('credentials')
        username = credentials.get('email')
        index = users.index(user) + 1
        debug_data = f'{index} {username}'

        json = send_request(f'{API_URL}/api/v1/user/signup/', 'post', data=credentials)
        print_result('SIGNUP', json.get('status'), 'ok', debug_data)
        user_id = json['message']['id']

        json = send_request(f'{API_URL}/login/', 'post', data=credentials)
        token = json.get('access')

        print_result('LOGIN', bool(token), True, debug_data)
        user['token'] = token

        for _ in range(random.randint(0, max_posts_per_user)):
            content = generate_string(string.ascii_letters, 200)
            json = send_request(
                f'{API_URL}/api/v1/post/', 'post', data={'author': user_id, 'content': content},
                headers={'Authorization': f'Bearer {token}'}
            )

            print_result('CREATE_POST', bool(json.get('id')), True, debug_data)
            posts.append(json.get('id'))

    for user in users:
        credentials = user.get('credentials')
        username = credentials.get("email")
        token = user.get('token')

        index = users.index(user) + 1
        debug_data = f'{index} {username}'

        for _ in range(random.randint(0, max_likes_per_user)):
            json = send_request(
                f'{API_URL}/api/v1/post/{random.choice(posts)}/like/', 'put',
                data={'user': username},
                headers={'Authorization': f'Bearer {token}'}
            )

            print_result('LIKE', json.get('status'), 'ok', debug_data)
