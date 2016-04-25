import operator
from collections import OrderedDict
import radon.complexity as cc_mod
from radon.cli.harvest import CCHarvester, MIHarvester, RawHarvester
from radon.cli import Config


def get_files_complexity_data(paths, ignore):
    config = Config(
        min="A",
        max="F",
        exclude=ignore,
        ignore=ignore,
        show_complexity=True,
        average=False,
        total_average=False,
        order=getattr(cc_mod, 'SCORE'),
        no_assert=False,
        show_closures=False,
    )

    harvester = CCHarvester(paths, config)
    data = []
    for filename, functions in harvester.results:
        if not functions:
            continue
        scores = [
            function_obj.complexity
            for function_obj in functions
        ]
        average = float(sum(scores)) / len(scores)
        data.append((filename, average,))

    sorted_scores = sorted(data, key=operator.itemgetter(1), reverse=True)
    return OrderedDict(sorted_scores)


def get_files_maintainability_data(paths, ignore):
    config = Config(
        min="A",
        max="C",
        exclude=ignore,
        ignore=ignore,
        multi=True,
        show=True,
    )
    harvester = MIHarvester(paths, config)
    data = []
    for filename, mi_data in harvester.results:
        if not mi_data:
            continue
        data.append((filename, mi_data['mi']))

    sorted_scores = sorted(data, key=operator.itemgetter(1))
    return OrderedDict(sorted_scores)


def get_files_lines_of_code(paths, ignore):
    config = Config(
        exclude=ignore,
        ignore=ignore,
        summary=False,
    )
    harvester = RawHarvester(paths, config)

    data = []
    for filename, raw_data in harvester.results:
        if not raw_data:
            continue
        data.append((filename, raw_data['loc'],))

    sorted_scores = sorted(data, key=operator.itemgetter(1), reverse=True)
    return OrderedDict(sorted_scores)
