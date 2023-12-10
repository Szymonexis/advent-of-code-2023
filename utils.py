import os
import inspect
from time import perf_counter
from typing import Literal


def strip(s: str) -> str:
    return s.strip()


def get_day_input_name(py_file_name: str) -> str:
    return f'{py_file_name[:py_file_name.find(".")]}.txt'


def get_lines(filepath: str) -> list[str]:
    return list(map(strip, open(f'./inputs/{get_day_input_name(os.path.basename(filepath))}', 'r').readlines()))


def clear_log():
    print(file=open('log.txt', 'w'), end='')


def log(s: str = ''):
    print(s, file=open('log.txt', 'a'))


def log_table(logs: list[dict], keys: list[str] = None, min_column_width=3, position: Literal['left', 'center', 'right'] = 'center', lpadding=1, rpadding=1):
    def apply_padding(s): return s.ljust(
        max_lengths[i] + lpadding).rjust(max_lengths[i] + lpadding + rpadding)

    if len(logs) == 0:
        return

    keys = list(logs[0].keys()) if keys == None else keys
    value_rows = []
    for l in logs:
        value_row = []
        for k in keys:
            value_row.append(f'{l[k]}')
        value_rows.append(value_row)

    max_lengths = [min_column_width for _ in keys]
    for i in range(len(keys)):
        if len(keys[i]) > max_lengths[i]:
            max_lengths[i] = len(keys[i])

    for v_r in value_rows:
        for i in range(len(v_r)):
            if len(v_r[i]) > max_lengths[i]:
                max_lengths[i] = len(v_r[i])

    h = ''
    for (i, k) in enumerate(keys):
        if i == 0:
            h += '|'

        match position:
            case 'left':
                h += apply_padding(str(k).ljust(max_lengths[i]))

            case 'center':
                h += apply_padding(str(k).center(max_lengths[i]))

            case 'right':
                h += apply_padding(str(k).rjust(max_lengths[i]))

        h += '|'

    log(h)
    log('-'*len(h))

    for v_r in value_rows:
        r = ''
        for (i, v) in enumerate(v_r):
            if i == 0:
                r += '|'

            match position:
                case 'left':
                    r += apply_padding(str(v).ljust(max_lengths[i]))

                case 'center':
                    r += apply_padding(str(v).center(max_lengths[i]))

                case 'right':
                    r += apply_padding(str(v).rjust(max_lengths[i]))

            r += '|'
        log(r)


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        file_name = os.path.basename(caller_frame.f_code.co_filename)
        m = f'Method {file_name}->{method.__qualname__} took: {(perf_counter() - t) * 1000} ms'
        print(m)
        return ret
    return wrapper_method
