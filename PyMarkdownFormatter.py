import re

class MDFormatter:

    ## TODO
        # [x] Headings
        # [x] Styling text
        # [x] Quoting text
        # [x] Quoting code
        # [x] Links
        # [?] Section links
        # [as embed in url] Images
        # [x] List
        # [x] Task list
        # [?] Mentioning people and teams
        # [x] Paragraphs
        # [x] Footnotes
        # [x] Comments
        # [x] Ignoring Markdown formatting
        # [x] diagrams
        # [x] table

    # https://github.com/jincheng9/markdown_supported_languages
    code_syntaxes = ['Cucumber', 'abap', 'ada', 'ahk', 'apacheconf', 'applescript', 
        'as', 'as3', 'asy', 'bash', 'bat', 'befunge', 'blitzmax', 'boo', 'brainfuck', 'c', 
        'cfm', 'cheetah', 'cl', 'clojure', 'cmake', 'coffeescript', 'console', 'control', 
        'cpp', 'csharp', 'css', 'cython', 'd', 'delphi', 'diff', 'dpatch', 'duel', 'dylan', 
        'erb', 'erl', 'erlang', 'evoque', 'factor', 'felix', 'fortran', 'gas', 'genshi', 
        'glsl', 'gnuplot', 'go', 'groff', 'haml', 'haskell', 'html', 'hx', 'hybris', 'ini', 
        'io', 'ioke', 'irc', 'jade', 'java', 'js', 'jsp', 'lhs', 'llvm', 'logtalk', 'lua', 
        'make', 'mako', 'maql', 'mason', 'markdown', 'modelica', 'modula2', 'moocode', 'mupad', 
        'mxml', 'myghty', 'nasm', 'newspeak', 'objdump', 'objectivec', 'objectivej', 'ocaml', 
        'ooc', 'perl', 'php', 'postscript', 'pot', 'pov', 'prolog', 'properties', 'protobuf', 
        'py3tb', 'pytb', 'python', 'r', 'rb', 'rconsole', 'rebol', 'redcode', 'rhtml', 'rst', 
        'sass', 'scala', 'scaml', 'scheme', 'scss', 'smalltalk', 'smarty', 'sourceslist', 'splus', 
        'sql', 'sqlite3', 'squidconf', 'ssp', 'tcl', 'tcsh', 'tex', 'text', 'v', 'vala', 'vbnet', 
        'velocity', 'vim', 'xml', 'xquery', 'xslt', 'yaml'
        ]

    codediagram_syntaxes = ['mermaid', 'geoJSON', 'topoJSON', 'ASCII STL']

    styiling_formats = {
        'i': '*',
        'b': '**',
        'ib': '***',
        'bi': '***',
        'st': '~~',
        'sub': ['<sub>', '</sub>'],
        'sup': ['<sup>', '</sup>'],
        # 'sub': '~',
        # 'sup': '^',
    }

    @staticmethod
    def newline(num=2) -> str:
        return '\n'*(num)

    @staticmethod
    def heading(string:str, level:int=1) -> str:
        # assert type(level) == int, f'{level=} not an integer'
        # assert level > 0 or level < 6, f'{level=}: heading level cannot be less than 0 or more than equal to 6'
        if not level:
            level = 1
        return '#'*level + f' {string}'

    @staticmethod
    def paragraph(string:str) -> str:
        string = string.replace('\n', ' ')
        string = string.split(' ')
        return ' '.join(i for i in string if i) + ' '

    @staticmethod
    def quote(string:str, level:int=1) -> str:
        assert type(level) == int, f'{level=} not an integer'
        assert level > 0, f'{level=}: level cannot be less than 0'
        return '>'*level + f' {md_paragraph(string)}'

    @staticmethod
    def codeblock(string:str, syntax:str='', override=False) -> str:
        if syntax not in MDFormatter.code_syntaxes and not override:
            syntax = ''
        return f'``` {syntax}\n{string}\n```'

    @staticmethod
    def diagrams(string:str, syntax:str='') -> str:
        syntax = syntax if syntax in MDFormatter.codediagram_syntaxes else ''
        return md_codeblock(string, syntax, override=True)

    @staticmethod
    def styiling(string:str, style:str) -> str:
        if style not in MDFormatter.styiling_formats:
            return string
        else:
            style = MDFormatter.styiling_formats[style]
            if type(style) == list:
                return f'{style[0]}{string}{style[1]}'
            else:
                return f'{style}{string}{style}'

    @staticmethod
    def links(url:str, alttext:str='', embed=False) -> str:
        if alttext and embed:
            return f'![{alttext}]({url})'
        elif alttext:
            return f'[{alttext}]({url})'
        else:
            return url

    @staticmethod
    def linkuser(string:str) -> str:
        return f'@{string}'

    @staticmethod
    def comment(string:str) -> str:
        return f'<!-- {string} -->'

    @staticmethod
    def footnote(ref:str, desc:str='') -> str:
        if desc:
            return f'[^{ref}]: {desc}'
        return f'[^{ref}]'

    @staticmethod
    def bulletlist(items, level:int=1, num=False, offset=0) -> str:
        # assert type(level) == int, f'{level=} not an integer'
        # assert level > 0, f'{level=}: heading level cannot be less than 0'
        if not level:
            level = 1
        if not offset:
            offset = 0
        level -= 1
        buffer = []
        for n, item in enumerate(items):
            n += offset 
            if type(item) == list or type(item) == tuple:
                buffer.append(MDFormatter.bulletlist(item, level+2, num))
            else:
                if num:
                    string = '   '*level + f'{n+1}. {item}'
                else:
                    string = '  '*level + f'- {item}'
                buffer.append(string)
        return '\n'.join(buffer) + '\n'

    @staticmethod
    def tasks(items, level:int=1) -> str:
        assert type(level) == int, f'{level=} not an integer'
        assert level > 0, f'{level=}: heading level cannot be less than 0'

        def p(items):
            buffer = []
            for item in items:
                if type(item) == list or type(item) == tuple\
                    and type(item[0]) != bool:
                    buffer.append(p(item))
                else:
                    if type(item) == list or type(item) == tuple:
                        cond = 'x' if item[0] else ' '
                        buffer.append(f'[{cond}] {item[1]}')
                    else:
                        buffer.append(f'[ ] {item}')
            return buffer

        items = p(items)
        return MDFormatter.bulletlist(items, level=level, num=False)

    @staticmethod
    def table_content(items) -> str:
        return '| ' + ' | '.join([str(l) for l in items]) + ' |'

    @staticmethod
    def table_header(items, aligns=None) -> str:
        if type(aligns) == list or type(aligns) == tuple:
            if len(aligns) < len(items):
                aligns += [None]*(len(items) - len(aligns))
        else:
            aligns = [None] * len(items)
        aligns = [a.lower()[0] if type(a) == str else '' for a in aligns]
        offset = 0
        for n, align in enumerate(aligns):
            l = len(items[n])
            if l < 3: 
                l = 3

            if align == 'r':
                aligns[n] = '-'*(l-1) + ':'
            elif align == 'c':
                aligns[n] = ':'+'-'*(l-2) +':'
            elif align == 'l':
                aligns[n] = ':' + '-'*(l-1) 
            else:
                aligns[n] = '-' * l


        heads = md_table_content(items)
        aligns = md_table_content(aligns)
        return f'{heads}\n{aligns}'

    @staticmethod
    def escape_tag_form_html_string(string, tags=['b', 'i', 'sup', 'sub']):
        tags = '|'.join(tags)
        pattern = fr"(<(?P<dl>({tags}))>)(.+)(<\/(?P=dl)>)"
        regexp = re.compile(pattern)
        def e(string):
            matches = regexp.finditer(string)
            for match in matches:
                start = match.start()
                end = match.end()
                tag = match.groups()[0] # full tag string
                tag_len = len(tag)
                string_interp = [
                    (None, string[:start]),
                    (tag[1:-1], string[start + tag_len : end - tag_len - 1]),
                    (None, string[end:])
                ]
                string_interp = [i for i in string_interp if i[1]]
                # recurse if string still contains tag
                string_interp = [(i[0], e(i[1])) if regexp.search(i[1]) else i for i in string_interp] 
                return string_interp
            else:
                return (None, string)
        return e(string)

if __name__ == '__main__':
    # TODO: argparse, helper
    parser = MDFormatter()
    
    string = parser.escape_tag_form_html_string('<b><i>foobar<sup>baz</sup></i></b>')


    def recurse(pairs):
        rettemp = ''
        for i in pairs:
            style = i[0]
            value = i[1]
            # print(f'{f} {d}')
            if type(value) == list or type(value) == tuple:
                temp = recurse(value)
                rettemp += f'{style}_{temp}'
            else:
                rettemp += f'{style}_{value}'
        return rettemp


    res = recurse(string)
    print(res)