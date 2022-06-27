import MDParser

class Py2MD:
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

    __T_PARAGRAPH  = __Token('p', 'paragraph', True)
    __T_HEADINGS   = __Token('h', 'heading')
    __T_LISTS      = __Token('l', 'list', True)
    __T_TASKS      = __Token('ts', 'task', True)
    __T_TABLE      = __Token('t', 'table')
    __T_CODEBLOCK  = __Token('cb', 'codeblock')
    __T_FOOTNOTE   = __Token('fn', 'footnote', True)
    __T_URL        = __Token('url', 'url', True)
    __T_DEFINITION = __Token('d', 'definition')
    __T_HRULE      = __Token('hr', 'horizontal_rule')
    __T_BREAK      = __Token('b', 'break')
    __T_STYLING    = __Token('s', 'inlinestyling', True)
    __T_END        = __Token('end', 'eod', True)

    __TOKEN_CONTAINER = __TokenContainer()

    def __init__(self, newlines=2):
        if newlines <= 1:
            newlines = 2
        else:
            newlines = int(newlines) 
        self.newlines = newlines
        self.stream = []
        self.tags = self.__TOKEN_CONTAINER.get_token_ids()
        self.tag_names = self.__TOKEN_CONTAINER.get_token_names()
        self.tags_dict = dict(zip(self.tags, self.tag_names))
        self.getByID = self.__TOKEN_CONTAINER.getById
        self.parser = MDParser.MDParser()

    def add(self, tag:str, value:str=''):
        tagid = tag.rstrip('0123456879')
        param = tag[len(tagid):]
        param = param if param else None
        value = value if value else None
        if tagid not in self.tags:
            raise ValueError(f'tag \'{tagid}\' is not valid.')
        else:
            tag_token = self.getByID(tagid)
            tag_token.params.append(param)
            self.stream.append(tag_token)
            self.stream.append(value)
        return self

    def addlist(self, tag:str, values:list):
        for item in values:
            self.add(tag, item)
        return self

    def parse(self) -> str:
        self.add('end')
        strbuff = []
        tempbuff = []
        param = None
        past_token = None
        while self.stream:
            value = self.stream.pop(0)
            if isinstance(value, self.__Token):
                param = value.params.pop(0)
                if past_token == value and value.isinline:
                    print(value)
                else:
                    past_token = value
                    if tempbuff:
                        strbuff.append(self.__flush(tempbuff))
                    tempbuff.clear()
                    tempbuff.append((value, param))
            else:
                tempbuff.append(value)
        return ('\n'*self.newlines).join(i for i in strbuff if i)

    def __flush(self, block):
        token, param = block.pop(0)
        values = block
        string = ''
        if not isinstance(token, self.__Token):
            raise RuntimeError('Something went wrong on parsing data block')
        for value in values:
            if token == self.__T_END:
                pass
            
            elif token == self.__T_PARAGRAPH:
                string += self.parser.paragraph(value)
                string += ' '
            
            elif token == self.__T_HEADINGS: 
                param = int(param) if param else 1
                string += self.parser.heading(value, param)
            
            elif token == self.__T_LISTS:
                param = True if param else False
                string += self.parser.bulletlist([value], num=param)
                string += '\n'
            
            elif token == self.__T_TASKS: 
                string += self.parser.tasks([value])
                string += '\n'
            
            elif token == self.__T_TABLE:
                if param:
                    string += self.parser.table_header(value)
                else:
                    string += self.parser.table_content(value)
            
            elif token == self.__T_CODEBLOCK: 
                syntax = None
                if type(value) == list or type(value) == tuple:
                    syntax = value[0]
                    value = value[1]
                else:
                    syntax = None
                string += self.parser.codeblock(value, syntax)
            
            elif token == self.__T_FOOTNOTE: 
                desc = ''
                if type(value) == list or type(value) == tuple:
                    desc = value[1]
                    value = value[0]
                else:
                    desc = ''
                string += self.parser.footnote(value, desc)
            
            elif token == self.__T_URL: 
                desc = ''
                if type(value) == list or type(value) == tuple:
                    desc = value[1]
                    value = value[0]
                else:
                    desc = ''
                string += self.parser.links(value, desc)
            
            elif token == self.__T_DEFINITION: pass
            
            elif token == self.__T_HRULE: 
                string += '---'
            
            elif token == self.__T_BREAK: 
                string += ''
            
            elif token == self.__T_STYLING: 
                style = ''
                if type(value) == list or type(value) == tuple:
                    style = value[0]
                    value = value[1]
                else:
                    style = 'i'
                string += self.parser.styiling(value, style)

        return string.rstrip('\n')

if __name__ == '__main__':
    mdparser = Py2MD()
    mdparser.add('h', 'Py2MD')
    mdparser.add('p', 'Python internal markdown parser.')
    mdparser.add('p', 'impractical, heavy, pointless, but its')
    mdparser.add('s', ('i', 'kinda'))
    mdparser.add('p', 'wokrs.')
    with open('README.md', 'w') as fp:
        fp.write(mdparser.parse())
