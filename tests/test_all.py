from alphareader import AlphaReader
from io import StringIO
import typing
import types
from pathlib import Path
import logging
from functools import reduce
parent = Path(__file__).parent

logger = logging.getLogger()
def test_instance():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert isinstance(next(reader), typing.List)

def test_records():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert len(next(reader)) == 4

def test_content():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert next(reader) == ['1', 'John', 'Doe', '2020']

def test_custom_delimiter():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.xsv', 'rb'), terminator=10, delimiter=124, encoding='UTF-8')
    assert len(next(reader)) == 4

def test_fn_transform():
    fn = lambda x: int()
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8', fn_transform=fn)
    assert all(list(map(lambda x: isinstance(x, int), next(reader))))

def test_fn_chain():
    fn1 = lambda x: x.strip()
    fn2 = lambda x: int(x)    
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8', fn_transform=[fn1, fn2])
    assert sum(next(reader)) == 6

def test_fn_chain():
    fn1 = lambda x: x.strip()
    fn2 = lambda x: int(x)
    fn3 = lambda x: x*10
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8', fn_transform=[fn1, fn2, fn3])
    assert sum(next(reader)) == 60
    assert sum(next(reader)) == 600
    assert sum(next(reader)) == 6000
