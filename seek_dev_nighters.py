from datetime import datetime

import pytz
import requests


DEVMAN_API = "https://devman.org/api/challenges/solution_attempts"
LAST_NIGHT_HOUR = 6


def load_attempts():
    page = 1
    pages = 1
    while page <= pages:
        response = requests.get(DEVMAN_API, params={'page': page}).json()
        page += 1
        pages = int(response['number_of_pages'])
        for attempt in response['records']:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
                }

def get_midnighters(attempts):
    for attempt in attempts:
        local_datetime = get_local_datetime(attempt['timestamp'],
                                            attempt['timezone'])
        if local_datetime and local_datetime.hour in range(LAST_NIGHT_HOUR):
            yield attempt['username'], local_datetime


def get_local_datetime(timestamp, timezone):
    if (timestamp and timezone) is not None:
        return datetime.fromtimestamp(timestamp, pytz.timezone(timezone))


if __name__ == '__main__':
    for user, local_datetime in get_midnighters(load_attempts()):
        print('"{}" sent task on {} at {}'.format(
            user, local_datetime.strftime('%d-%m-%Y'),
            local_datetime.strftime('%H:%M %Z')))

