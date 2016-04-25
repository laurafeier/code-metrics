import os
import re

from jira import JIRA


class JiraClient(object):

    def __init__(self, **credentials):
        self.ticket_pattern = credentials.pop('ticket_pattern')
        self.credentials = credentials
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = JIRA(**self.credentials)
        return self._client

    @classmethod
    def from_environment(cls):
        server = os.environ.get("JIRA_URL")
        user = os.environ.get("JIRA_USER")
        passwd = os.environ.get("JIRA_PASSWORD")
        project_prefix = os.environ.get("JIRA_PROJECT_ID")
        if not server:
            raise RuntimeError("JIRA server URL required. Set env var JIRA_URL")
        if not user:
            raise RuntimeError("JIRA username required. Set env var JIRA_USER")
        if not passwd:
            raise RuntimeError("JIRA password required. Set env var JIRA_PASSWORD")
        if not project_prefix:
            raise RuntimeError("JIRA project ID required. Set env var JIRA_PROJECT_ID")

        ticket_pattern = r"(^\s*{}-\d+)".format(project_prefix)
        return cls(
            server=server,
            basic_auth=(user, passwd),
            ticket_pattern=ticket_pattern
        )

    def get_issue_key(self, message):
        ticket_match = re.match(self.ticket_pattern, message)
        if not ticket_match:
            return None
        return ticket_match.groups()[0]

    def filter_bugs(self, issues_list):
        if not issues_list:
            return []
        bug_types = ["Bug", "Bug Sub Task"]
        jql_bug_types = ",".join(["'{}'".format(_type) for _type in bug_types])
        jql_issues_keys = ','.join(issues_list or [])
        jql = "issuetype in ({}) AND key in ({})".format(
            jql_bug_types, jql_issues_keys
        )
        bugs = self.client.search_issues(jql_str=jql)
        return [bug.key for bug in bugs]
