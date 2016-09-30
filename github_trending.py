import requests
import json
import datetime


API_GITHUB_URL = 'https://api.github.com/'


DAYS_NUMBER = 7


TOP_SIZE = 20


def get_date_before_today(days_number):
    return datetime.date.today() - datetime.timedelta(days_number)


def get_trending_repositories(top_size):
    date = get_date_before_today(DAYS_NUMBER)
    url = '{}search/repositories?q=created:>{}&sort=stars'.format(
        API_GITHUB_URL, date
    )
    data = json.loads(requests.get(url).text)
    return data['items'][:top_size]


def get_open_issues_amount(repo_owner, repo_name):
    url = '{}repos/{}/{}/issues?state=open'.format(
        API_GITHUB_URL, repo_owner, repo_name
    )
    return json.loads(requests.get(url).text)


if __name__ == '__main__':
    data = get_trending_repositories(TOP_SIZE)
    for repo in data:
        issue_data = get_open_issues_amount(
            repo['owner']['login'], repo['name']
        )
        print('#'*80)
        print('Repository name:', repo['name'])
        print('Repository url:', repo['html_url'])
        print('Number of open issues:', len(issue_data))
