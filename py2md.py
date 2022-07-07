from Token import Token, TokenContainer
from PyMarkdownFormatter import MDFormatter
import re

class Py2MD:

    MDFormatter = MDFormatter()

    __T_TAG = TokenContainer()
    __T_STYLE = TokenContainer()
    __T_FLAGS = TokenContainer()

    __TERMINATOR     = Token(__T_FLAGS, '</>',   'Terminator', True,  None,  False)
    __STYLE     = Token(__T_FLAGS, '<s>',   'ParseStyling', True,  None,  False)

    #           Token(Container, id, name, isinline, fn, accepts_param, param_type, param_len)
    __PARAGRAPH     = Token(__T_TAG, 'p',   'Paragraph',  True,  MDFormatter.paragraph, False, None, 0)
    __HEADING       = Token(__T_TAG, 'h',   'Heading',    False, MDFormatter.heading,   True, int)
    __QUOTE         = Token(__T_TAG, 'q',   'Quote',      True, MDFormatter.quote,     True, int)
    __CODE          = Token(__T_TAG, 'c',   'CodeBlock',  False, MDFormatter.codeblock, True, str)
    __FOOTNOTES     = Token(__T_TAG, 'fn',  'Footnotes',  True,  MDFormatter.footnote,  True, bool)
    __URL           = Token(__T_TAG, 'url', 'URL',        False, MDFormatter.links,     True, bool)
    __BULLETLIST    = Token(__T_TAG, 'li',  'BulletList', True,  MDFormatter.bulletlist,True, (int, bool, int), 3)
    __TABULAR       = Token(__T_TAG, 't',   'Tabular',    True,  MDFormatter.table_content, False, None, 0)
    __TABULARHEAD   = Token(__T_TAG, 'th',  'TabularHeader',True,  MDFormatter.table_header, False, None, 0)
    __BREAKLINE     = Token(__T_TAG, 'b',   'Breakline',  False, lambda: '\n',         False, None, 0)
    __ENDLINE       = Token(__T_TAG, 'end', 'Endline',    False, MDFormatter.newline,   True, int)
    __LITERAL       = Token(__T_TAG, 'lit', 'Literal',    False, lambda x: x,           True, None, 0)
    # __BULLETLIST    = Token(__T_TAG, 'l',   'List Items', True,  lambda : MDFormatter.bulletlist,          False)

    __S_ITALIC      = Token(__T_STYLE, 'i', 'Italic',        True, lambda x: MDFormatter.styiling(x, 'i'), False)
    __S_BOLD        = Token(__T_STYLE, 'b', 'Bold',          True, lambda x: MDFormatter.styiling(x, 'b'), False)
    # __S_ITALICBOLD  = Token(__T_STYLE, 'bi', 'Italic-Bold',  True, lambda x: MDFormatter.styiling(x, 'bi'), False)
    __S_STRIKETH    = Token(__T_STYLE, 'st', 'Strikethrough',True, lambda x: MDFormatter.styiling(x, 'st'), False)
    __S_SUPER       = Token(__T_STYLE, 'sup', 'Superscript', True, lambda x: MDFormatter.styiling(x, 'sup'), False)
    __S_SUB         = Token(__T_STYLE, 'sub', 'Subscript',   True, lambda x: MDFormatter.styiling(x, 'sub'), False)

    # __HEADING.opt_param(True, int)


    def __init__(self, newlines:int=2):
        self.newlines = newlines

        self.tags = self.__T_TAG.getIds()
        self.tag_names = self.__T_TAG.getNames()
        self.tag_dict = dict(zip(self.tags, self.tag_names))

        self.styles = self.__T_STYLE.getIds()
        self.style_names = self.__T_STYLE.getNames()
        self.style_dict = dict(zip(self.styles, self.style_names))

        self.getTagById = self.__T_TAG.getById
        self.getStyleById = self.__T_STYLE.getById
        self.__stream = []
        self.__previous_tag = None

    
    def peekstream(self):
        streamlen = len(self.__stream)
        print(self.__stream)
        print('stream size   : ', self.__stream.__sizeof__())
        print('stream length : ', streamlen, 'items')

    def __add_tostream(self, tagstr, param, value):
        if param and (type(param) != list and type(param) != tuple):
            param = [param]
        # elif param and (type(param) == list or type(param) == tuple):
        #     print(type(param), param)
        else:
            param = [None]

        if tagstr.endswith('s'):
            tagstr = tagstr[:-1]
            param = [self.__STYLE, *param]
        elif tagstr not in self.tags:
            tagstr = 'p'

        tag = self.getTagById(tagstr)

        if self.__previous_tag and self.__previous_tag == tag and self.__previous_tag.isinline and tag.isinline:
            self.__stream.pop()
        else:
            self.__stream.append(tag)
        self.__stream.append(param)
        self.__stream.append(value)
        self.__stream.append(self.__TERMINATOR)
        self.__previous_tag = tag

    # no @overload decorator? :(
    def add(self, *args):
        if not args:
            raise ValueError('???')
        if len(args) == 1:
            self.__add_tostream('p', None, args[0])
        elif len(args) == 2:
            self.__add_tostream(args[0], None, args[1])
        else:
            for arg in args[2:]:
                self.__add_tostream(args[0], args[1], arg)
        return self

    def b(self):
        self.__add_tostream('lit', None, '')
        return self

    def __parse_styling(self, string):
        style_pairs = self.MDFormatter.escape_tag_form_html_string(string)
        def esc(pairs):
            strbuff = ''
            for items in pairs:
                style = items[0]
                value = items[1]
                fn = lambda x: x
                # print(style, items)
                if not value:
                    value = ''
                if type(value) == list or type(value) == tuple:
                    value = esc(value)
                if style in self.styles:
                    fn = self.getStyleById(style).fn
                strbuff += fn(value)
            return strbuff
        return esc(style_pairs)
        # return reccc(style_pairs)
        # return 'AAAA'

    def __parse_byToken(self, token, param, value):
        token_fn_arg_len = token.param_len
        fn = token.fn

        if len(param) < token_fn_arg_len:
            param = param + [None]*(token_fn_arg_len-len(param))
        if token in [self.__BREAKLINE]:
            return ''
        if token_fn_arg_len == 0:
            value = fn(value)
        elif token_fn_arg_len == 1:
            value = fn(value, param[0])
        elif token_fn_arg_len == 2:
            value = fn(value, param[0], param[1])
        elif token_fn_arg_len == 3:
            value = fn(value, param[0], param[1], param[2])
        else:
            raise ValueError()
        return value

    def parse(self):
        strout = ''
        previous_token = None
        while self.__stream:
            token = self.__stream.pop(0)
            if token == self.__TERMINATOR:
                if previous_token != self.__LITERAL and previous_token != self.__TABULARHEAD :
                    strout += self.__ENDLINE.fn(self.newlines)
            else:
                while True:
                    if self.__stream[0] == self.__TERMINATOR:
                        break
                    do_parse_style = False
                    strtemp = ''
                    param = self.__stream.pop(0)
                    value = self.__stream.pop(0)
                    if param[0] == self.__STYLE:
                        do_parse_style = True
                        param.pop(0)
                    # print(f'{token=}, {param=}, {value=}')
                    strtemp = self.__parse_byToken(token, param, value)
                    if do_parse_style:
                        strtemp = self.__parse_styling(strtemp)
                    strout += strtemp
            previous_token = token
        return strout


####### ---------------------------------------------
if __name__ == '__main__':
    mdparser = Py2MD()
    mdparser.newlines = 2
    mdparser.add('h','Py2MD')

    mdparser.add('h', 2, 'Tag Reference')
    mdparser.add('th', ['Tag', 'Desc', 'Inline', 'Param'])
    for k,v in mdparser.tag_dict.items():
        tag = mdparser.getTagById(k)
        isinline = str(tag.isinline)
        paramtype = str(tag.param_type)
        mdparser.add('t', [f'`{k}`', v, isinline, paramtype])

    mdparser.add('th', ['Style', 'Desc'])
    for k,v in mdparser.style_dict.items():
        mdparser.add('t', [f'`{k}`', v])



    ### ---------------------------------------------
    mdparser.add('---')
    mdparser.add('h','Heading lv 1')
    mdparser.add('h', 2, 'Heading lv 2')
    mdparser.add('h', 3, 'Heading lv 3')
    mdparser.add('h', 4, 'Heading lv 4')
    mdparser.add('h', 5, 'Heading lv 5')

    mdparser.add('Paragraph.')
    mdparser.add('p','adding')
    mdparser.add('p','another')
    mdparser.add('p','paragraph')
    mdparser.add('p','will')
    mdparser.add('p','concatenated')
    mdparser.add('p','into')
    mdparser.add('p','one')
    mdparser.add('p','line.')
    mdparser.b()
    mdparser.add('p','except if breakline is added between addition.')

    mdparser.add('li',['list item', 'uses iterator', 'as value', ['nested list', 'will be parsed', ['as multilevel list']], 'back to level 1'])

    mdparser.add('ps','adding `s` suffix on tag arg will reformat <i>styling</i> into markdown format.')
    mdparser.b()
    mdparser.add('p', '<b><i>Italic Bold</i></b> << although normally html inline formatting wtill works just fine.')
    mdparser.add('q', 'also multilevel Quote Block')
    mdparser.add('q', 2, 'Sandwiches at cheap price !? !?.')
    mdparser.add('q', 3, 'satisfactory.')
    mdparser.add('th', ['Id', 'This will','parse as Table'])
    for i in range(5):
        mdparser.add('t', [i, f'Value_{i}', f'Another one {i}'])
    
    
    # mdparser.peekstream()
    mdstr = mdparser.parse()

    with open('README.md',  'w') as fp:
        fp.write(mdstr)
