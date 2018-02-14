import argparse
import logging
import os

from multiprocessing import Process, Manager
from multiprocessing.dummy import Pool
from operator import methodcaller

from flask import Flask, render_template, send_file
import multiprocessing_logging

from core.scrapers.bet365_scraper import Bet365Scrapper
from core.scrapers.paddy_scraper import PaddyScraper
from core.scrapers.skybet_scraper import SkybetScraper
from core.scrapers.williamhill_scraper import WilliamScrapper
from core.tools import get_attachment, merge_results


app = Flask(__name__)


@app.route('/_refresh')
def refresh():
    """
    Returns table in current state without updating anything
    """
    data = merge_results(dict(app.results))
    return render_template('table.html', data=data)


@app.route('/_save')
def save_file():
    data = merge_results(dict(app.results))
    return send_file(
        filename_or_fp=get_attachment(data),
        mimetype='application/vnd.ms-excel',
    )


@app.route('/')
def render_root():
    return render_template('base.html')


def get_arg_parser():
    path = os.path.dirname(os.path.abspath(__file__))
    arg_parser = argparse.ArgumentParser(
        description='WoldCup Odds Scrapping', add_help=True
    )
    arg_parser.add_argument(
        '--executable-path',
        action='store',
        dest='path',
        default=f'{path}/chromedriver',
        help='chromeDriver executable path.\nDefault path is ./chromedriver'
    )
    arg_parser.add_argument(
        '--delay',
        action='store',
        default=60*5,  # 5minutes
        dest='delay',
        type=int,
        help='Delay between scrapping requests. Default is 5 minutes'
    )
    return arg_parser


if __name__ == '__main__':
    multiprocessing_logging.install_mp_handler()
    args = get_arg_parser().parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s|%(levelname)s|%(message)s|',
    )
    with Manager() as mp_manager:
        shared_dict = mp_manager.dict()

        app.results = shared_dict
        Process(target=methodcaller('run'), args=(app,)).start()
        scrappers = (
            SkybetScraper(
                shared_dict,
                delay=args.delay,
                executable_path=args.path,
                driver_extra_options=(
                    '--proxy-server=http://54.38.79.85:9000',
                    '--headless',
                )
            ),
            Bet365Scrapper(
                shared_dict,
                delay=args.delay,
                executable_path=args.path,
                driver_extra_options=('--headless',)
            ),
            PaddyScraper(
                shared_dict,
                delay=args.delay,
                executable_path=args.path,
                driver_extra_options=('--headless',)
            ),
            WilliamScrapper(
                shared_dict,
                delay=args.delay,
                executable_path=args.path,
                driver_extra_options=('--headless',)
            ),
        )
        pool = Pool(len(scrappers))
        pool.map(methodcaller('pool'), scrappers)
        pool.join()
