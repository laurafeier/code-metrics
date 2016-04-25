import collections
import re
from code_metrics.jira_utils import JiraClient
from code_metrics.git_utils import (
    get_repo, get_commit_files, get_revision)


def get_ticket_commits(repo_path, from_commit, to_commit):
    revision = get_revision(from_commit, to_commit)
    repo = get_repo(repo_path)
    jira_client = JiraClient.from_environment()
    ticket_commits = {}
    for commit in repo.iter_commits(revision):
        ticket_name = jira_client.get_issue_key(commit.message)
        if not ticket_name:
            continue
        ticket_commits[commit.binsha] = ticket_name
    return ticket_commits


def build_bug_score_data(repo, commits, ignore=None):
    files_changed = collections.defaultdict(dict)

    for commit, ticket_name in commits.items():
        files_stats = get_commit_files(repo, commit)
        for file_path, stats in files_stats.items():
            if ignore and re.match(ignore, file_path):
                continue
            file_data = files_changed[file_path]
            file_data.setdefault('tickets', set())
            file_data['tickets'].add(ticket_name)
            file_data.setdefault('changes_score', 0)
            file_data['changes_score'] += stats.get('lines', 0)


    for file_path, file_data in files_changed.items():
        file_data['ticket_count'] = len(file_data['tickets'])
        file_data['ticket_names'] = ' '.join(file_data['tickets'])

    return files_changed


def get_bug_score(repo_path, from_commit, to_commit, ignore=None):
    ticket_commits = get_ticket_commits(repo_path, from_commit, to_commit)
    tickets_found = ticket_commits.values()

    # interogate JIRA for bug type tickets
    jira_client = JiraClient.from_environment()
    bug_tickets = set(jira_client.filter_bugs(tickets_found))

    bug_commits = {}
    for commit_sha, ticket in ticket_commits.items():
        if ticket in bug_tickets:
            bug_commits[commit_sha] = ticket

    data = build_bug_score_data(get_repo(repo_path), bug_commits, ignore=ignore)

    return data
