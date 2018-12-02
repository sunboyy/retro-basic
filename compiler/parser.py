def __is_id(string):
    return len(string) == 1 and string >= 'A' and string <= 'Z'

def __is_const(string):
    return string.isdigit() and (0 <= int(string) <= 100)

def __is_line_num(string):
    return string.isdigit() and (1 <= int(string) <= 1000)

def parse(tokens):
    return __parse(['pgm'], tokens + ['EOF'], False)

def __parse(stack, tokens, flag):
    if len(stack) == 0 and len(tokens) == 0:
        return []
    if len(stack) == 0:
        raise SyntaxError('Stack empty')
    if len(tokens) == 0:
        raise SyntaxError('Out of token')
    top = stack[0]
    token = tokens[0]
    if top == 'pgm':
        if __is_line_num(token):
            return __parse(['line', 'pgm'] + stack[1:], tokens, flag)
        if token == 'EOF':
            return __parse(['EOF'] + stack[1:], tokens, flag)
    if top == 'line':
        if __is_line_num(token):
            return __parse(['line_num', 'stmt'] + stack[1:], tokens, flag)
    if top == 'stmt':
        if __is_id(token):
            return __parse(['asgmt'] + stack[1:], tokens, flag)
        if token == 'IF':
            return __parse(['if'] + stack[1:], tokens, flag)
        if token == 'PRINT':
            return __parse(['print'] + stack[1:], tokens, flag)
        if token == 'GOTO':
            return __parse(['goto'] + stack[1:], tokens, flag)
        if token == 'STOP':
            return __parse(['stop'] + stack[1:], tokens, flag)
    if top == 'asgmt':
        if __is_id(token):
            return __parse(['id', '=', 'exp'] + stack[1:], tokens, flag)
    if top == 'exp':
        if __is_id(token) or __is_const(token):
            return __parse(['term', 'exp\''] + stack[1:], tokens, flag)
    if top == 'exp\'':
        if token == '+':
            return __parse(['+', 'term'] + stack[1:], tokens, flag)
        if token == '-':
            return __parse(['-', 'term'] + stack[1:], tokens, flag)
        if token == 'EOF' or __is_line_num(token):
            return __parse(stack[1:], tokens, flag)
    if top == 'term':
        if __is_id(token):
            return __parse(['id'] + stack[1:], tokens, flag)
        if __is_const(token):
            return __parse(['const'] + stack[1:], tokens, flag)
    if top == 'if':
        if token == 'IF':
            return __parse(['IF', 'cond', 'line_num'] + stack[1:], tokens, flag)
    if top == 'cond':
        if __is_id(token) or __is_const(token):
            return __parse(['term', 'cond\''] + stack[1:], tokens, flag)
    if top == 'cond\'':
        if token == '<':
            return __parse(['<', 'term'] + stack[1:], tokens, flag)
        if token == '=':
            return __parse(['=', 'term'] + stack[1:], tokens, flag)
    if top == 'print':
        if token == 'PRINT':
            return __parse(['PRINT', 'id'] + stack[1:], tokens, flag)
    if top == 'goto':
        if token == 'GOTO':
            return __parse(['GOTO', 'line_num'] + stack[1:], tokens, flag)
    if top == 'stop':
        if token == 'STOP':
            return __parse(['STOP'] + stack[1:], tokens, flag)
    if top == 'IF':
        if token == 'IF':
            return [('#if', 0)] + __parse(stack[1:], tokens[1:], True)
    if top == 'GOTO':
        if token == 'GOTO':
            return __parse(stack[1:], tokens[1:], True)
    if top == 'EOF':
        if token == 'EOF':
            return __parse(stack[1:], tokens[1:], flag)
    if top == 'PRINT':
        if token == 'PRINT':
            return [('#print', 0)] + __parse(stack[1:], tokens[1:], flag)
    if top == 'STOP':
        if token == 'STOP':
            return [('#stop', 0)] + __parse(stack[1:], tokens[1:], flag)
    if top == '+':
        if token == '+':
            return [('#op', 1)] + __parse(stack[1:], tokens[1:], flag)
    if top == '-':
        if token == '-':
            return [('#op', 2)] + __parse(stack[1:], tokens[1:], flag)
    if top == '<':
        if token == '<':
            return [('#op', 3)] + __parse(stack[1:], tokens[1:], flag)
    if top == '=':
        if token == '=':
            return [('#op', 4)] + __parse(stack[1:], tokens[1:], flag)
    if top == 'id':
        if __is_id(token):
            return [('#id', ord(token) - ord('A') + 1)] + __parse(stack[1:], tokens[1:], flag)
    if top == 'const':
        if __is_const(token):
            return [('#const', int(token))] + __parse(stack[1:], tokens[1:], flag)
    if top == 'line_num':
        if __is_line_num(token):
            if flag:
                return [('#goto', int(token))] + __parse(stack[1:], tokens[1:], False)
            else:
                return [('#line', int(token))] + __parse(stack[1:], tokens[1:], False)
    raise SyntaxError('Unmatched token ' + token + ' with nonterminal ' + top)
