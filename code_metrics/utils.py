from pkg_resources import parse_version


def to_version(name):
    if not name:
        return None
    try:
        return parse_version(name)
    except (TypeError, ):
        return None


def average(numbers):
    return sum(numbers) / float(len(numbers))
