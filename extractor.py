import csv
from datetime import date, timedelta
import os
from typing import Iterable, TextIO

import click
from dateutil.relativedelta import relativedelta
from git import Repo

DEFAULT_BRANCH = os.environ.get('DEFAULT_BRANCH', 'master')

GITHUB_SSL_PREFIX = 'git@github.com:'
GITHUB_HTTP_PREFIX = 'https://github.com/'
GIT_URL_SUFFIX = '.git'

DATE = os.environ.get('DATE_LABEL', 'Data')
ID = os.environ.get('ID_LABEL', 'Identyfikator')
SUMMARY = os.environ.get('SUMMARY_LABEL', 'Opis')
LINK = os.environ.get('LINK_LABEL', 'Odnośnik')

FIELDNAMES = (DATE, ID, SUMMARY, LINK)


def parse_commits(
        repos: Iterable[str],
        since: str,
        until: str,
) -> Iterable[dict]:
    for repo_path in repos:
        try:
            repo_path, branch = repo_path.split(':')
        except ValueError:
            branch = DEFAULT_BRANCH

        repo = Repo(repo_path)
        author = repo.config_reader().get_value('user', 'email')
        origin_url = next(repo.remote().urls)
        base_url = origin_url.replace(GITHUB_SSL_PREFIX, GITHUB_HTTP_PREFIX)[:-len(GIT_URL_SUFFIX)]

        for commit in repo.iter_commits(
                branch,
                author=author,
                since=since,
                until=until,
                no_merges=True
        ):
            commit_id = commit.hexsha[:7]  # Seven chars is enough
            yield {
                DATE: date.fromtimestamp(commit.committed_date),
                ID: commit_id,
                SUMMARY: commit.summary,
                LINK: f'{base_url}/commit/{commit_id}'
            }


def write_commits(commits: Iterable[dict], output: TextIO) -> None:
    writer = csv.DictWriter(output, dialect=csv.unix_dialect, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(commits)


@click.command()
@click.argument('repos', nargs=-1)
@click.argument('output', required=True, type=click.File('w', encoding='utf-8'))
@click.option('--since', default=None, type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--until', default=None, type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--month', default=None, type=click.DateTime(formats=["%Y-%m"]))
def main(repos, output, since, until, month):
    if month is not None:
        since = month
        until = month + relativedelta(months=1) - timedelta(days=1)
    write_commits(
        commits=sorted(
            parse_commits(repos, since, until),
            key=lambda x: x[DATE]
        ),
        output=output
    )


if __name__ == '__main__':
    main()
