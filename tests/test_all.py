from alphareader import AlphaReader,AlphaWriter
from pathlib import Path
import logging
import pytest
import os

parent = Path(__file__).parent

logger = logging.getLogger()
def test_iterator():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert hasattr(reader, '__iter__')

def test_generator():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert hasattr(reader, '__next__')

def test_instance():
    reader = AlphaReader(open(parent / 'fixtures' / 'file.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8')
    assert isinstance(next(reader), list)

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
    fn3 = lambda x: x*10
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8', fn_transform=[fn1, int, fn3])
    assert sum(next(reader)) == 60
    assert sum(next(reader)) == 600
    assert sum(next(reader)) == 6000

def test_list():
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=44, encoding='UTF-8', fn_transform=[lambda x: x.strip(), int])
    n = list(reader)
    assert len(n) == 3

def test_multibyte():    
    reader = AlphaReader(open(parent / 'fixtures' / 'nums.csv', 'rb'), terminator=10, delimiter=198, encoding='UTF-8', fn_transform=[lambda x: x.strip(), int])
    with pytest.raises(ValueError):
        next(reader)

def test_writer():
    reader = AlphaReader(open(parent / 'fixtures' / 'alpha.dat', "rb"))
    total_size = AlphaWriter(str(parent / 'fixtures' / 'alpha-copy.dat'), reader)
    assert os.path.exists(str(parent / 'fixtures' / 'alpha-copy.dat'))
    assert total_size == os.path.getsize(parent / 'fixtures' / 'alpha.dat')