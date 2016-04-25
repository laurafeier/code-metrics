import sys
from mando import command, main, arg

from code_metrics import pylint_metrics
from code_metrics import radon_metrics
from code_metrics import bug_metrics
from code_metrics import git_utils
from code_metrics import utils
from code_metrics.formatters import as_table


@command
@arg('paths', nargs='+')
def average_complexity(paths, ignore=None):
    '''Shows average complexity score.

    The lower the score is, the lower the quality.
    Uses radon to collect complexity from all functions defined
    in a python file. It generates an average from all files
    complexity score.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    '''

    data = radon_metrics.get_files_complexity_data(paths, ignore) or {}
    sys.stdout.write(str(utils.average(data.values())))


@command
@arg('paths', nargs='+')
def average_line_count(paths, ignore=None):
    '''Shows the average of physical lines count.

    Uses radon to collect lines of code for each file.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    '''
    data = radon_metrics.get_files_lines_of_code(paths, ignore) or {}
    sys.stdout.write(str(utils.average(data.values())))


@command
@arg('paths', nargs='+')
def average_maintainability(paths, ignore=None):
    '''Shows average maintainability score.

    The higher the score is, the better the quality.
    Uses radon to collect maintainability index for each file.
    It generates an average from all files maintainability index.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    '''
    data = radon_metrics.get_files_maintainability_data(paths, ignore) or {}
    sys.stdout.write(str(utils.average(data.values())))


@command
@arg('paths', nargs='+')
def files_complexity(paths, ignore=None, limit=None, fmt=u'csv'):
    '''Shows complexity scores per file.

    The lower the score is, the lower the quality.
    Uses radon to collect complexity from all functions defined
    in a python file. It generates an average from all functions
    in a file which will be the complexity score for that file.
    Files are sorted by their complexity score.
    The default output is in CSV format.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -l, --limit <int>: max no of rows to display
    :param -f, --fmt <str>: set output table format; supported formats:
      plain, simple, grid, fancy_grid, pipe, orgtbl, rst, mediawiki, html,
      latex, latex_booktabs, tsv, csv (default: csv)

    '''

    data = radon_metrics.get_files_complexity_data(paths, ignore) or {}
    rows = data.items()[:limit] if limit else data.items()

    sys.stdout.write(
        as_table(rows, ['File', 'Complexity score'], table_format=fmt)
    )


@command
@arg('paths', nargs='+')
def files_maintainability(paths, ignore=None, limit=None, fmt=u'csv'):
    '''Shows maintainability score per file.

    The higher the score is, the better the quality.
    Uses radon to collect maintainability index for each file.
    Files are sorted by their maintainability score. Lowest scores firsts.
    The output is in CSV format.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -l, --limit <int>: max no of rows to display
    :param -f, --fmt <str>: set output table format; supported formats:
      plain, simple, grid, fancy_grid, pipe, orgtbl, rst, mediawiki, html,
      latex, latex_booktabs, tsv, csv (default: csv)
    '''
    data = radon_metrics.get_files_maintainability_data(paths, ignore) or {}
    rows = data.items()[:limit] if limit else data.items()

    sys.stdout.write(
        as_table(rows, ['File', 'Maintainability score'], table_format=fmt)
    )


@command
@arg('paths', nargs='+')
def files_line_count(paths, ignore=None, limit=None, fmt=u'csv'):
    '''Shows the number of physical lines count per file.

    Uses radon to collect lines of code for each file.
    Files are sorted by their line count score. Highest scores firsts.
    The output is in CSV format.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -l, --limit <int>: max no of rows to display
    :param -f, --fmt <str>: set output table format; supported formats:
      plain, simple, grid, fancy_grid, pipe, orgtbl, rst, mediawiki, html,
      latex, latex_booktabs, tsv, csv (default: csv)
    '''
    data = radon_metrics.get_files_lines_of_code(paths, ignore) or {}
    rows = data.items()[:limit] if limit else data.items()

    sys.stdout.write(
        as_table(rows, ['File', 'Physical lines of code'], table_format=fmt)
    )


@command
@arg('paths', nargs='+')
def pylint_score(paths, rcfile=None):
    '''Shows pylint score.

    :param paths: paths that pylint will check
    :param --rcfile <str>: Path to pylint rc file
    '''
    score = pylint_metrics.get_global_score(paths, rcfile)
    sys.stdout.write(str(score))


@command
def recent_tags(path='.'):
    '''Shows tags ordered as version numbers.

    :param path: The path for the working tree directory of the git repo.
    '''
    tags = git_utils.get_most_recent_tag_names(git_utils.get_repo(path))
    sys.stdout.write(" ".join(tags))


@command
def jira_tickets(from_commit, to_commit, path='.'):
    '''Shows all JIRA tickets between two commits.

    :param path: The path for the working tree directory of the git repo.
    :param from_commit: The start commit point.
    :param to_commit: The end commit point.
    '''
    ticket_commits = bug_metrics.get_ticket_commits(path, from_commit, to_commit) or {}
    tickets = set(ticket_commits.values())
    sys.stdout.write(" ".join(tickets))


@command
def bug_score(from_commit, to_commit, path='.', ignore=None, fmt=u'csv'):
    '''Shows a list of changed files by bug tickets between two commits.

    The output is in csv format. It contains 4 columns:
    'No of tickets', 'Tickets', 'Score', 'File changed'.
    The score column shows the sum of the change score
    that file suffered for each bug(commit) that touched it.

    :param from_commit: The start commit point.
    :param to_commit: The end commit point.
    :param path: The path for the working tree directory of the git repo.
    :param ignore: regex pattern to match the files to exclude from output.
    :param -f, --fmt <str>: set output table format; supported formats:
      plain, simple, grid, fancy_grid, pipe, orgtbl, rst, mediawiki, html,
      latex, latex_booktabs, tsv, csv (default: csv)
    '''
    score_data = bug_metrics.get_bug_score(path, from_commit, to_commit, ignore) or {}

    header = ['No of tickets', 'Tickets', 'Score', 'File changed']
    rows = [
        [len(stats['tickets']), ' '.join(stats['tickets']), stats['changes_score'], _file,]
        for _file, stats in score_data.items()]
    sys.stdout.write(as_table(rows, header, table_format=fmt))


if __name__ == '__main__':
    main()
