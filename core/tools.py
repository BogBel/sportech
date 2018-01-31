import io
import time
import logging

from collections import defaultdict
from itertools import chain

import xlwt


def merge_results(collected_data):
    """
    :param collected_data: {
        'company_name1': {
            'country1': 'odd1.1',
            'country2': 'odd1.2',
            ...
        },
        'company_name2': {
            'country1': 'odd2.1',
            'country2': 'odd2.2',
            ...
        }
    ...
    }
    :return:{
        'keys': ['company_name1', 'company_name2'],  # sorted
        'data': [
            ('country1', (odd1.1, odd2.1)),
            ('country2', (odd1.2, odd2.2)),
        ]
    }
    """
    result = dict()
    result['keys'] = sorted(k for k, v in collected_data.items() if v)
    result['data'] = defaultdict(list)
    for country, odd in chain.from_iterable(
        collected_data[key].items() for key in result['keys']
    ):
        result['data'][country].append(odd)

    result['data'] = sorted(result['data'].items())
    return result


def get_attachment(data):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('World Cup 2018')
    tmp_style = (
        'font: name Times New Roman, bold {bold}; '
        'align: wrap on, vert centre, horiz center; '
        'border: left thin, right thin, top thin, bottom thin'
    )
    bold_style = xlwt.easyxf(tmp_style.format(bold='true'))
    single_style = xlwt.easyxf(tmp_style.format(bold='false'))
    for col, site in enumerate(('#', *data['keys'])):
        ws.write(0, col, site, bold_style)
    for raw, team_data in enumerate(data['data'], start=1):
        team_name, odds = team_data
        ws.write(raw, 0, team_name, bold_style)
        for col_ind, odd in enumerate(odds, start=1):
            ws.write(raw, col_ind, odd, single_style)
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream


def timeit(func):
    """
    Logs time of execution for class methods
    """
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start_time
        company = args[0].COMPANY_NAME
        logging.info(
            f"Method \"{func.__name__}\" of {company} took {exec_time}sec"
        )
        return result
    return wrap
