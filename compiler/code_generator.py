from functools import reduce

def generate(parse_tree):
    mapper = {'#line': 10, '#id': 11, '#const': 12, '#if': 13, '#goto': 14, '#print': 15, '#stop': 16, '#op': 17}
    out = list(map(lambda x: [mapper[x[0]], x[1]], parse_tree))
    return reduce((lambda x, y: x + y), out, []) + [0]
