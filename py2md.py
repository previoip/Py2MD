class Py2MD:

    class TOKEN: 
        def __init__(self, name, inline, group=None):
            self.name = name
            self.inline = inline
            self.group = group

        def __repr__(self):
            return f'token::{self.name}'

        def __eq__(self, o):
            if not self.group:
                return self.name == o
            return self.group == o

    T_PARAG = TOKEN('paragraph', True, 'parag')
    T_HEADINGS = TOKEN('heading', False, 'head')
    T_TASKS = TOKEN('task', True)
    T_TABLE = TOKEN('table', True)
    T_CODEBLOCK = TOKEN('codeblock', True, 'parag')
    T_FOOTNOTE = TOKEN('footnote', False, 'parag')
    T_URL = TOKEN('url', True, 'parag')
    T_DEFINITION = TOKEN('definition', False)
    T_SUBSCRIPT = TOKEN('subscript', True, 'parag')
    T_SUPSCRIPT = TOKEN('superscript', True, 'parag')
    T_HRULE = TOKEN('horizontal_rule', False)
    T_BREAK = TOKEN('break', False)

    def __init__(self):
        # defaults
        self.max_characters = 72
        self.num_newlines = 2
        # prog init
        self.__buffer = []
        self.__TOKENS = {
            'p': self.T_PARAG, 
            'h': self.T_HEADINGS,
            'ts': self.T_TASKS,
            'tb': self.T_TABLE,
            'cb': self.T_CODEBLOCK,
            'fn': self.T_FOOTNOTE,
            'url': self.T_URL,
            'def': self.T_DEFINITION,
            'sb': self.T_SUBSCRIPT,
            'ss': self.T_SUPSCRIPT,
            'hr': self.T_HRULE,
            'b': self.T_BREAK,
            }



    def parse(self) -> str:
        string_buffer = []
        prev_token = None
        print(self.__buffer)
        while self.__buffer:
            token = self.__buffer.pop(0)
            param = self.__buffer.pop(0)
            value = self.__buffer.pop(0)
            if token.inline and param[1] and token == prev_token:
                string_buffer[-1] += self.__parse_by_token(value, token, param)
            else:
                string_buffer.append(self.__parse_by_token(value, token, param))
            prev_token = token
        return ('\n'*self.num_newlines + '\n').join(string_buffer).strip()

    def clear(self):
        self.__buffer = []

    def add(self, ttype='p', value='', inline=True):
        # adds item to the buffer stack/deque
        ident = ttype.rstrip('0123456879')
        param = ttype[len(ident):]
        param = int(param) if param else None
        # print('added: ',ident, param, value)
        param = (param, inline)
        token = self.__TOKENS[ident]
        self.__buffer.append(token)
        self.__buffer.append(param)
        self.__buffer.append(value)
        return self


    def __parse_by_token(self, value, token, param) -> str:
        previous_group = token.group
        token.group = None
        print(f'parsing: {token.name}',param,value)
        param = param[0] if param[0] else 1
        if token == self.T_PARAG: 
            value = value.replace('\n', ' ').split(' ')
            value = [v for v in value if v]
            value = ' '.join(value)
        elif token == self.T_HEADINGS:
            value = '#' * param + ' ' + value
        elif token == self.T_TASKS: pass
        elif token == self.T_TABLE: pass
        elif token == self.T_CODEBLOCK: pass
        # elif token == self.T_FOOTNOTE: pass
        elif token == self.T_URL: pass
        elif token == self.T_DEFINITION: 
            value = value[0] + '\n:' + value[1]
        elif token == self.T_SUBSCRIPT:
            value = '~' + value + '~'
        elif token == self.T_SUPSCRIPT:
            value = '^' + value + '^'
        elif token == self.T_HRULE: 
            value = '---'
        elif token == self.T_BREAK: 
            value = ''
        token.group = previous_group
        return value + ' '

if __name__ == '__main__':
    mdparser = Py2MD()
    mdparser.num_newlines = 1
    mdparser.add('h', 'Py2MD')
    mdparser.add('p', 'python internal to markdown parser.')
    mdparser.add('p', 'impractical, but fun.')
    mdparser.add('hr', 'horizontal rules doenst parse value')
    mdparser.add('h1', 'example heading')
    mdparser.add('h2', 'example heading number 2')
    mdparser.add('p', 'example paragraph somehow differs.        ')
    mdparser.add('p', 'example paragraph and newlinw').add('b')
    mdparser.add('p', '123')
    mdparser.add('p', 'foooobar')
    mdparser.add('ss', 'sup')
    mdparser.add('sb', 'sub')
    mdparser.add('def', ('definition', 'this is a definition, though it doesnt work in github markdown format.'))
    mdparser.add('def', ('definition', 'this is a definition'))

    mdparser.add('p', 'example paragraph that doestn go inline', inline=False)
    with open('README.md', 'w') as fp:
        fp.write(mdparser.parse())
