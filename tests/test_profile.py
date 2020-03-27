import cProfile, pstats, io
from pstats import SortKey
from alphareader import AlphaReader
from pathlib import Path
import logging
import csv

parent = Path(__file__).parent
logger = logging.getLogger()

def test_alphareader_with_encoding():
    with open(parent / 'fixtures' / 'large.dat', 'rb') as infile:
        pr = cProfile.Profile()
        pr.enable()
        reader = AlphaReader(infile, delimiter=171, terminator=172, encoding='cp1252')
        list(reader)
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        logger.info(s.getvalue())

def test_native_csv():
    with open(str(parent / 'fixtures' / 'xx-large.dat'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        pr = cProfile.Profile()
        pr.enable()
        list(reader)
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        logger.info(s.getvalue())
