from RAM_interpreter import execute
from compilation import TORAM_to_ram
from sys import stdin, argv


def get_input():
    while True:
        for x in input('< ').split():
            yield int(x)

if '-h' in argv:
    print('python3 run.py [options] path/to/file.TORAM')
    print('-c -- print RAM code')
else:
    with open(argv[-1], 'r') as f:
        ram_code=TORAM_to_ram(f.read())
        if '-c' in argv:
            print(ram_code)
        else:
            execute(ram_code, get_input())
