
class Py2MD:

    class __DoubleDeque:
            def __init__(self):
                self.buffer = [None, None]

            def __repr__(self):
                return str(self.buffer)

            def flush(self):
                buffer = self.buffer
                self.buffer = [None, None]
                return buffer

            def put(self, item):
                self.buffer[0] = self.buffer[-1]
                self.buffer[-1] = item

            def peek(self, index):
                return self.buffer[index]

            def peekl(self):
                return self.peek(1)

            def peekr(self):
                return self.peek(-1)

    class __TokenContainer:
        __ids = []
        __tokens = []
        __names = []

        def getById(self, ident):
            index = self.__ids.index(ident)
            return self.__tokens[index]

        def append_to_container(self, ident, token, name=''):
            self.__ids.append(ident)
            self.__tokens.append(token)
            self.__names.append(name)

        def get_token_ids(self):
            return self.__ids.copy()

        def get_token_names(self):
            return self.__names.copy()

    class __Token(__TokenContainer):
        def __init__(self, ident, name, isinline=False):
            self.id = ident
            self.name = name
            self.append_to_container(ident, self, name)
            self.isinline = isinline
            self.params = []

        def __repr__(self):
            return f'<t::{self.name}>'

        def __eq__(self, o):
            return self.id == o

    __T_PARAG      = __Token('p', 'paragraph', True) 
    __T_HEADINGS   = __Token('h', 'heading')
    __T_TASKS      = __Token('l', 'list')
    __T_TASKS      = __Token('ts', 'task')
    __T_TABLE      = __Token('t', 'table')
    __T_CODEBLOCK  = __Token('cb', 'codeblock')
    __T_FOOTNOTE   = __Token('fn', 'footnote', True)
    __T_URL        = __Token('url', 'url', True)
    __T_DEFINITION = __Token('d', 'definition')
    __T_HRULE      = __Token('hr', 'horizontal_rule')
    __T_BREAK      = __Token('b', 'break')
    __T_SUBSCRIPT  = __Token('sub', 'subscript', True)
    __T_SUPSCRIPT  = __Token('sup', 'superscript', True)

    __TOKEN_CONTAINER = __TokenContainer()

    def __init__(self):
        self.ddeque = self.__DoubleDeque()
        self.stream = []
        self.tags = self.__TOKEN_CONTAINER.get_token_ids()
        self.tag_names = self.__TOKEN_CONTAINER.get_token_names()
        self.tags_dict = dict(zip(self.tags, self.tag_names))
        self.getByID = self.__TOKEN_CONTAINER.getById

    def add(self, tag, value):
        tagid = tag.rstrip('0123456879')
        param = tag[len(tagid):]
        param = param if param else None

        if tagid not in self.tags:
            raise ValueError(f'tag \'{tagid}\' is not present for parser.')
        else:
            tag_token = self.getByID(tagid)
            tag_token.params.append(param)
            self.stream.append(tag_token)
            self.stream.append(value)
        return self

    def addlist(self, tag, values):
        for item in values:
            self.add(tag, item)
        return self

    def parse(self) -> str:
        # todo
        string = ''
        pbuff = []
        print(self.stream)
        param = None
        while self.stream:
            value = self.stream.pop(0)
            if isinstance(value, self.__Token):
                param = value.params.pop(0)

            print(param)
            self.ddeque.put(value)
            print(self.ddeque)
        self.ddeque.flush()
        return string

if __name__ == '__main__':
    mdparser = Py2MD()
    print(mdparser.tags)
    mdparser.add('p', 'value')
    mdparser.addlist('p', ['value2', 'value3'])
    mdparser.add('h2', 'heading1')
    mdparser.add('h3', 'heading2')
    mdparser.add('h4', 'heading3')
    mdparser.add('p', 'value')
    mdparser.parse()
    