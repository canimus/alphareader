# AlphaReader
[![canimus](https://circleci.com/gh/canimus/alphareader.svg?style=svg)](https://circleci.com/gh/canimus/alphareader)
After several attempts to try the `csv` package or `pandas` for reading large files with custome delimiters, I ended up writting a little program that does the job without complaints.

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

> fn = lambda x: x+1
> reader = AlphaReader(open('/raw/tsv/file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=44, fn_transform=fn)
> next(reader)
> [2,3,4]
> next(reader)
> [11,21,31]
```

## Chain Transformations
```python
# !cat file.csv
# 1,2,3
# 10,20,30
# 100,200,300

> fn_1 = lambda x: x+1
> fn_2 = lambda x: x*10
> reader = AlphaReader(open('/raw/tsv/file.tsv', 'rb'), encoding='cp1252', terminator=10, delimiter=44, fn_transform=[fn_1, fn_2])
> next(reader)
> [20,30,40]
> next(reader)
> [110,210,310]
```

## __Caution__ with large files
```python
> reader = AlphaReader(open('large_file.xsv', 'rb'), encoding='cp1252', terminator=172, delimiter=173)
> records = list(reader) # Avoid this as it will load all file in memory
```

> Limitations:
> As described by @eesmith in `Hacker News`. The multi-byte separators are not handled correctly. For this it will be necessary to confirm if the chunks split in the middle of the multi-byte character used to separate columns. This will introduce a performance impact in the library. Suggestions for a solution are welcomed.