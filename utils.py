import os


def strip(s: str) -> str:
    return s.strip()


def get_day_input_name(py_file_name: str) -> str:
    return f'{py_file_name[:py_file_name.find(".")]}.txt'


def get_lines(filepath: str) -> list[str]:
    return map(strip, open(f'./inputs/{get_day_input_name(os.path.basename(filepath))}', 'r').readlines())


def clear_log():
    print(file=open('log.txt', 'w'), end='')


def log(s: str):
    print(s, file=open('log.txt', 'a'))
