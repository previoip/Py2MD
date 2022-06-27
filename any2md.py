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
    # [ ]Footnotes
    # [ ] Comments
    # [ ] Ignoring Markdown formatting
    # [ ] diagrams
    # [ ] table

md_code_syntaxes = ['']
md_codediagram_syntaxes = ['mermaid', 'geoJSON', 'topoJSON', 'ASCII STL']
md_styiling_formats = {
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

def mdescape(string):
    return f'\*{string}\*'

def mdheading(string:str, level:int) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0 or level < 6, f'{level=}: heading level cannot be less than 0 or more than equal to 6'
    return '#'*level + f' {string}'

def mdparagraph(string:str) -> str:
    string = string.replace('\n', ' ')
    string = string.split(' ')
    return ' '.join(i for i in string if i)

def mdquote(string:str, level:int=1) -> str:
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0, f'{level=}: level cannot be less than 0'
    return '>'*level + f' {mdparagraph(string)}'

def mdcodeblock(string:str, syntax:str) -> str:
    md_code_syntaxes += md_codediagram_syntaxes
    syntax = syntax if syntax in md_code_syntaxes else ''
    return f'```{syntax}\n{string}\n```'

def mddiagrams(string:str, syntax:str) -> str:
    syntax = syntax if syntax in md_codediagram_syntaxes else ''
    return mdcodeblock(string, syntax)

def mdstyiling(string:str, style:str) -> str:
    if style not in md_styiling_formats:
        return string
    else:
        style = md_styiling_formats[style]
        if type(style) == list:
            return f'{style[0]}{string}{style[1]}'
        else:
            return f'{style}{string}{style}'

def mdlinks(url:str, alttext:str='', embed=False):
    if alttext and embed:
        return f'![{alttext}]({url})'
    elif alttext:
        return f'[{alttext}]({url})'
    else:
        return url

def mdlinkuser(string:str):
    return f'@{string}'

def mdcomment(string:str):
    return f'<!-- {string} -->'

def mdfootnote(ref:str, desc:str=''):
    if desc:
        return f'[^{ref}]: {desc}'
    return f'[^{ref}]'

def mdlists(lists, level:int=1, num=False, offset=0):
    assert type(level) == int, f'{level=} not an integer'
    assert level > 0, f'{level=}: heading level cannot be less than 0'
    level -= 1
    buffer = []
    for n, item in enumerate(lists):
        n += offset 
        if type(item) == list or type(item) == tuple:
            buffer.append(mdlists(item, level+2, num))
        else:
            if num:
                string = '   '*level + f'{n+1}. {item}'
            else:
                string = '  '*level + f'- {item}'
            buffer.append(string)
    return '\n'.join(buffer)

def mdtasks(lists, level:int=1):
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
    return mdlists(lists, level=level, num=False)

def mdtable_content(lists):
    return '| ' + ' | '.join([str(l) for l in lists]) + ' |'

def mdtable_header(lists, aligns=None):
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


    heads = mdtable_content(lists)
    aligns = mdtable_content(aligns)
    return f'{heads}\n{aligns}'


if __name__ == '__main__':

    l1 = ['list 1','list 2','list 3', ['nested 1', 'nested 2', 'nested 3', ['nestednested 1', 'nestednested 2', 'nestednested 3']],'list 4','list 5','list 6',]
    l2 = [
        'task 1',
        (False, 'task 2'),
        (True, 'task 3'),
            [
            (True, 'task 1'),
            (False, 'task 2'),
            (True, 'task 3'),
        ]
    ]

    l3 = ['Hhhead1', 'id', 'Heeeeead3', 'Headddd4']
    a3 = ['l', 'right', 'Center']
    print(mdtable_header(l3))
    # print(mdtasks(l1))
    # print(mdtasks(l2))
