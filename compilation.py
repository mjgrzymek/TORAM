from sys import stdin, argv
from itertools import chain, zip_longest
from copy import deepcopy
from string import digits, whitespace
from collections import namedtuple

def tree(i):
    word = []
    ret = []
    for c in i:
        if c == ')' or c in whitespace:
            if word:
                ret.append(''.join(word))
                word = []
            if c == ')':
                return ret
        elif c == '(':
            ret.append(tree(i))
        else:
            word.append(c)


unique_nr = 0


def get_unique():
    global unique_nr
    unique_nr += 1
    return str(unique_nr)


codegen_return_type = namedtuple('codegen_return_type', 'code ret')


def join(x, *args):
    return list(chain.from_iterable(codegen(son, *args).code for son in x))


class Args:
    def __init__(self, last_free, vard, fund):
        self.last_free = last_free
        self.vard = vard
        self.fund = fund

    def __iter__(self):
        yield self.last_free
        yield self.vard
        yield self.fund

    def __str__(self):
        return 'Args' + str((*self,))

    def str_no_fund(self):
        return 'Args' + str((self.last_free, self.vard, ...))


def codegen(x, last_free=1, vard={'acc': 0}, fund={}):
    vard = deepcopy(vard)
    args = Args(last_free, vard, fund)
    del last_free
    code = []
    ret = None
    
    if isinstance(x, str):
        if x[0] in digits + '-':
            ret = '=' + x
        elif x[0] in '&*':
            ret = ('=' if x[0] == '&' else '^') + vard[x[1:]]
        else:
            ret = vard[x]
    
    elif x[0] == '//':
        pass
    elif x[0][0] == '@':  # inline RAM
        inside = codegen(x[1], *args)
        code = inside.code + [x[0][1:] + ' ' + inside.ret]

    elif x[0] == '_':
        code = join(x[1:], *args)

    elif x[0] == 'def':
        fund[x[1]] = deepcopy(x)

    elif x[0] in ('while', 'if', 'ifngtz'):
        name, condition, statement = x
        label_name = name + get_unique()
        compiled_condition = codegen(condition, *args)

        if name == 'while':
            code =\
                [label_name + ':'] +\
                compiled_condition.code +\
                ['load ' + compiled_condition.ret] +\
                ['jzero END' + label_name] +\
                codegen(statement, *args).code +\
                ['jump ' + label_name] +\
                ['END' + label_name + ':']
        else:
            code =\
                compiled_condition.code +\
                ['load ' + compiled_condition.ret] +\
                [('jzero ' if name == 'if' else 'jgtz ') + label_name] +\
                codegen(statement, *args).code+\
                [label_name + ':']

    else:  # function (name arg1 arg2) (def name (arg1 ... var1 ...) (_ ...))
        func = deepcopy(fund[x[0]])
        _, _, argvars, func_code = func
        sent_vard = deepcopy(vard)  # need a copy to not override current names

        for argname, passed_arg in zip_longest(argvars, x[1:]):
            if passed_arg:
                compiled_passed_arg = codegen(passed_arg, *args)
                code.extend(compiled_passed_arg.code)
                code.append('load ' + compiled_passed_arg.ret)
                code.append('store ' + str(args.last_free))
                sent_vard[argname] = str(args.last_free)
                args.last_free += 1
            else:
                if isinstance(argname, str):
                    sent_vard[argname] = str(args.last_free)
                    args.last_free += 1
                else: # a table
                    sent_vard[argname[0]] = str(args.last_free)
                    args.last_free += int(argname[1])

        sent_vard['return'], ret = (str(args.last_free),) * 2
        args.vard = sent_vard
        args.last_free += 1
        code.extend(codegen(func_code, *args).code)
    return codegen_return_type(code, ret)


def TORAM_to_ram(txt):
    return '\n'.join(join(tree(iter(txt + ')'))))
