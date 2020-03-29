# AlphaReader

[![canimus](https://circleci.com/gh/canimus/alphareader.svg?style=svg)](https://circleci.com/gh/canimus/alphareader)

After several attempts to try the `csv` package or `pandas` for reading large files with custom delimiters, I ended up writting a little program that does the job without complaints.

__AlphaReader__ is a high performant, pure python, 15-line of code library, that reads chunks of bytes from your files, and retrieve line by line, the content of it.

The inspiration of this library came by having to extract data from a MS-SQL Server database, and having to deal with the `CP1252` encoding. By default AlphaReader takes this encoding as it was useful in our use case.

It works also with `HDFS` through the `pyarrow` library. But is not a depedency.

## CSVs
```python
# !cat file.csv
# 1,John,Doe,2010
# 2,Mary,Smith,2011
# 3,Peter,Jones,2012

> reader = AlphaReader(open('file.csv', 'rb'), encoding='cp1252', terminator=10, delimiter=44)
> next(reader)
> ['1','John','Doe','2010']
```

## TSVs
```python
# !cat file.tsv
# 1    John    Doe    2010
# 2    Mary    Smith  2011
# 3    Peter   Jones  2012

> reader = AlphaReader(open('file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=9)
> next(reader)
> ['1','John','Doe','2010']
```

## XSVs
```python
# !cat file.tsv
# 1¦John¦Doe¦2010
# 2¦Mary¦Smith¦2011
# 3¦Peter¦Jones¦2012

> ord('¦')
> 166
> chr(166)
> '¦'
> reader = AlphaReader(open('file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=166)
> next(reader)
> ['1','John','Doe','2010']
```

## HDFS
```python
# !hdfs dfs -cat /raw/tsv/file.tsv
# 1    John    Doe    2010
# 2    Mary    Smith  2011
# 3    Peter   Jones  2012

> import pyarrow as pa
> fs = pa.hdfs.connect()
> reader = AlphaReader(fs.open('/raw/tsv/file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=9)
> next(reader)
> ['1','John','Doe','2010']
```

## Transformations
```python
# !cat file.csv
# 1,2,3
# 10,20,30
# 100,200,300

> fn = lambda x: int(x)
> reader = AlphaReader(open('/raw/tsv/file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=44, fn_transform=fn)
> next(reader)
> [1,2,3]
> next(reader)
> [10,20,30]
```

## Chain Transformations
```python
# !cat file.csv
# 1,2,3
# 10,20,30
# 100,200,300

> fn_1 = lambda x: x+1
> fn_2 = lambda x: x*10
> reader = AlphaReader(open('/raw/tsv/file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=44, fn_transform=[int, fn_1, fn_2])
> next(reader)
> [20,30,40]
> next(reader)
> [110,210,310]
```

## Caution
```python
> reader = AlphaReader(open('large_file.xsv', 'rb'), encoding='cp1252', terminator=172, delimiter=173)
> records = list(reader) # Avoid this as it will load all file in memory
```

## Limitations
- No support for `multi-byte` delimiters
- Relatively slower performance than `csv` library. Use `csv` and dialects when your files have `\r\n` terminators
- Transformations are per row, perhaps vectorization could aid performance

## Performance
- 24MB file loaded with `list(AlphaReader(file_handle))`
```bash
tests/test_profile.py::test_alphareader_with_encoding
--------------------------------------------------------------------------------- live log call 
INFO     root:test_profile.py:22          252343 function calls in 0.386 seconds

    Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   119605    0.039    0.000    0.386    0.000 .\alphareader\__init__.py:39(AlphaReader)
   122228    0.266    0.000    0.266    0.000 {method 'split' of 'str' objects}
     2625    0.005    0.000    0.054    0.000 {method 'decode' of 'bytes' objects}
     2624    0.001    0.000    0.049    0.000 .\Python-3.7.4\lib\encodings\cp1252.py:14(decode)
     2624    0.048    0.000    0.048    0.000 {built-in method _codecs.charmap_decode}
     2625    0.027    0.000    0.027    0.000 {method 'read' of '_io.BufferedReader' objects}
        1    0.000    0.000    0.000    0.000 .\__init__.py:5(_validate)
        1    0.000    0.000    0.000    0.000 {built-in method _codecs.lookup}

```