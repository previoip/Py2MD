## todo
    # [ ] Headings
    # [ ] Styling text
    # [ ] Quoting text
    # [ ] Quoting code
    # [ ] Links
    # [?] Section links
    # [as embed in url] Images
    # [ ] Lists
    # [ ] Task lists
    # [?] Mentioning people and teams
    # [ ] Paragraphs
    # [ ] Footnotes
    # [ ] Comments
    # [ ] Ignoring Markdown formatting
    # [ ] diagrams
    # [ ] table

# https://github.com/jincheng9/markdown_supported_languages#for-markdown-texts-we-need-to-specify-the-languages-for-corresponding-syntax-highlighting
md_const_code_syntaxes = ['Cucumber', 'abap', 'ada', 'ahk', 'apacheconf', 'applescript', 
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

md_const_codediagram_syntaxes = ['mermaid', 'geoJSON', 'topoJSON', 'ASCII STL']

md_const_styiling_formats = {
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

def md_newline(num=2) -> str:
    return '\n'*(num + 1)

def md_heading(string:str, level:int) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0 or level < 6, f'{level=}: heading level cannot be less than 0 or more than equal to 6'
    return '#'*level + f' {string}'

def md_paragraph(string:str) -> str:
    string = string.replace('\n', ' ')
    string = string.split(' ')
    return ' '.join(i for i in string if i)

def md_quote(string:str, level:int=1) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0, f'{level=}: level cannot be less than 0'
    return '>'*level + f' {md_paragraph(string)}'

def md_codeblock(string:str, syntax:str, override=False) -> str:
    if syntax not in md_const_code_syntaxes and not override:
        syntax = ''
    return f'``` {syntax}\n{string}\n```'

def md_diagrams(string:str, syntax:str) -> str:
    syntax = syntax if syntax in md_const_codediagram_syntaxes else ''
    return md_codeblock(string, syntax, override=True)

def md_styiling(string:str, style:str) -> str:
    if style not in md_const_styiling_formats:
        return string
    else:
        style = md_const_styiling_formats[style]
        if type(style) == list:
            return f'{style[0]}{string}{style[1]}'
        else:
            return f'{style}{string}{style}'

def md_links(url:str, alttext:str='', embed=False) -> str:
    if alttext and embed:
        return f'![{alttext}]({url})'
    elif alttext:
        return f'[{alttext}]({url})'
    else:
        return url

def md_linkuser(string:str) -> str:
    return f'@{string}'

def md_comment(string:str) -> str:
    return f'<!-- {string} -->'

def md_footnote(ref:str, desc:str='') -> str:
    if desc:
        return f'[^{ref}]: {desc}'
    return f'[^{ref}]'

def md_lists(lists, level:int=1, num=False, offset=0) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0, f'{level=}: heading level cannot be less than 0'
    level -= 1
    buffer = []
    for n, item in enumerate(lists):
        n += offset 
        if type(item) == list or type(item) == tuple:
            buffer.append(md_lists(item, level+2, num))
        else:
            if num:
                string = '   '*level + f'{n+1}. {item}'
            else:
                string = '  '*level + f'- {item}'
            buffer.append(string)
    return '\n'.join(buffer)

def md_tasks(lists, level:int=1) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0, f'{level=}: heading level cannot be less than 0'

    def p(lists):
        buffer = []
        for item in lists:
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

    lists = p(lists)
    return md_lists(lists, level=level, num=False)

def md_table_content(lists) -> str:
    return '| ' + ' | '.join([str(l) for l in lists]) + ' |'

def md_table_header(lists, aligns=None) -> str:
    if type(aligns) == list or type(aligns) == tuple:
        if len(aligns) < len(lists):
            aligns += [None]*(len(lists) - len(aligns))
    else:
        aligns = [None] * len(lists)
    aligns = [a.lower()[0] if type(a) == str else '' for a in aligns]
    offset = 0
    for n, align in enumerate(aligns):
        l = len(lists[n])
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


    heads = md_table_content(lists)
    aligns = md_table_content(aligns)
    return f'{heads}\n{aligns}'


if __name__ == '__main__':
    # todo: argparse, helper
    pass