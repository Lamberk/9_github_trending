import requests
import datetime


API_GITHUB_URL = 'https://api.github.com'


QUANTITY_OF_DAYS = 7


TOP_SIZE = 20


def get_date_before_today(days_number):
    return datetime.date.today() - datetime.timedelta(days_number)


def get_trending_repositories(top_size):
    date = get_date_before_today(QUANTITY_OF_DAYS)
    params = {
        'q': 'created:>{}'.format(date),
        'sort': 'stars',
    }
    url = '{}/search/repositories'.format(API_GITHUB_URL)
    data = requests.get(url, params=params).json()
    return [
        {
            'login': repo['owner']['login'],
            'name': repo['name'],
            'html_url': repo['html_url']
        } for repo in data['items'][:top_size]
    ]


def add_open_issues_amount(data):
    for repo in data:
        params = {
            'state': 'open',
        }
        url = '{}/repos/{}/{}/issues'.format(
            API_GITHUB_URL, repo['login'], repo['name']
        )
        repo['issues_amount'] = len(requests.get(url, params=params).json())
    return data


def print_repos(repos):
    for repo in repos:
        print('#'*80)
        print('Repository name:', repo['name'])
        print('Repository url:', repo['html_url'])
        print('Number of open issues:', repo['issues_amount'])


if __name__ == '__main__':
    data = get_trending_repositories(TOP_SIZE)
    data = add_open_issues_amount(data)
    print_repos(data)
