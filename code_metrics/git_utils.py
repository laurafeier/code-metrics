import re
from git import Repo, Commit
from code_metrics import utils


def get_repo(path):
    return Repo(path)


def get_revision(from_commit, to_commit):
    revision = "{}..{}".format(from_commit, to_commit)
    return revision


def get_most_recent_tag_names(git_repo=None):
    git_repo = git_repo or Repo()
    tag_with_versions = [
        (tag.name, utils.to_version(tag.name))
        for tag in git_repo.tags
    ]
    # remove unmatched versions
    valid_version_tags = [
        (name, version)
        for name, version in tag_with_versions
        if version
    ]
    sorted_version_tags = sorted(
        valid_version_tags,
        key=lambda x: x[1], # sort by version
        reverse=True # newest first
    )
    return [pair[0] for pair in sorted_version_tags]


def get_commit_files(git_repo, commit_sha):
    return Commit(git_repo, commit_sha).stats.files


def get_changed_files(git_repo, from_commit, to_commit, match_only=None):
    revision = get_revision(from_commit, to_commit)
    files = set()
    for commit in git_repo.iter_commits(revision):
        changed = commit.stats.files.keys()
        if match_only:
            changed = [name for name in changed if re.match(match_only, name)]
        files.update(set(changed))
    return files
