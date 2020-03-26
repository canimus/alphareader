import io
import codecs
from types import (FunctionType, LambdaType)
from typing import List
from functools import reduce

def _validate(file_handle, chunk_size, delimiter, terminator, encoding, fn_transform):
    '''Prevalidations of the AlphaReader function'''
    # Validations
    codecs.lookup(encoding)
    
    if not isinstance(file_handle, io.BufferedReader):
        raise TypeError('File handle should be a reference to `open(file, r) or open(file, rb) function')

    if fn_transform:
        if isinstance(fn_transform, List):
            if not all(map(lambda f: isinstance(f, FunctionType) or isinstance(f, LambdaType), fn_transform)):
                raise TypeError('Excepted all transformations to be functions')
        elif not isinstance(fn_transform, FunctionType) or not isinstance(fn_transform, LambdaType):
            raise TypeError('Transformation parameter should be a function or lambda i.e. fn = lambda x: x.replace(a,b)')

    try:
        bytes(chr(terminator), encoding=encoding)
    except UnicodeEncodeError:
        raise UnicodeError(f'Line termination character chr({terminator}) not found in {encoding}')

    try:
        bytes(chr(delimiter), encoding=encoding)
    except UnicodeEncodeError:
        raise UnicodeError(f'Column delimiter character chr({delimiter}) not found in {encoding}')

    return True


def AlphaReader(file_handle, chunk_size=512, delimiter=171, terminator=172, encoding='cp1252', fn_transform=None):
    """A pure python file reader with custom delimiters and infinite size.

    Args:
        file_handle (io.BufferedReader): A file handle. Reference to open(file_name).
        chunk_size (int): The size of the buffered reader.
        delimiter (int): Character code to use for column delimiter.
        terminator (int): Character code to use for line terminator.
        encoding (str): Codec of the file.
        fn_transform (list,lambda): A list of functions/lambdas or single function/lambda to apply to each parsed column.

    Returns:
        generator: A generator that contains a List[String] types
    """
    _validate(file_handle, chunk_size, delimiter, terminator, encoding, fn_transform)

    # Reading routine
    chunk = ""
    while True:
        curr = file_handle.read(chunk_size)
        if encoding:
            curr = curr.decode(encoding)
        chunk += curr
        if not curr:
            break
        if chr(terminator) in chunk:
            lines = chunk.split(chr(terminator))
            for line in lines[0:-1]:
                columns = line.split(chr(delimiter))
                if fn_transform: 
                    try:
                        transformations = iter(fn_transform)
                        yield list(map(lambda x: reduce(lambda a,b: b(a), fn_transform, x), columns))
                    except TypeError:
                        yield list(map(fn_transform, columns))
                else: yield columns
            chunk = lines[-1]