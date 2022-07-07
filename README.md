# Py2MD

## Tag Reference

| Tag | Desc | Inline | Param |
| --- | ---- | ------ | ----- |
| `p` | Paragraph | True | None |
| `h` | Heading | False | <class 'int'> |
| `q` | Quote | True | <class 'int'> |
| `c` | CodeBlock | False | <class 'str'> |
| `fn` | Footnotes | True | <class 'bool'> |
| `url` | URL | False | <class 'bool'> |
| `li` | BulletList | True | (<class 'int'>, <class 'bool'>, <class 'int'>) |
| `t` | Tabular | True | None |
| `th` | TabularHeader | True | None |
| `b` | Breakline | False | None |
| `end` | Endline | False | <class 'int'> |
| `lit` | Literal | False | None |


| Style | Desc |
| ----- | ---- |
| `i` | Italic |
| `b` | Bold |
| `st` | Strikethrough |
| `sup` | Superscript |
| `sub` | Subscript |


--- 

# Heading lv 1

## Heading lv 2

### Heading lv 3

#### Heading lv 4

##### Heading lv 5

Paragraph. adding another paragraph will concatenated into one line. 

except if breakline is added between addition. 

- list item
- uses iterator
- as value
  - nested list
  - will be parsed
    - as multilevel list


- back to level 1


adding `s` suffix on tag arg will reformat *styling* into markdown format. 

<b><i>Italic Bold</i></b> << although normally html inline formatting wtill works just fine. 

> also multilevel Quote Block 
>> Sandwiches at cheap price !? !?. 
>>> satisfactory. 


| Id | This will | parse as Table |
| --- | --------- | -------------- |
| 0 | Value_0 | Another one 0 |
| 1 | Value_1 | Another one 1 |
| 2 | Value_2 | Another one 2 |
| 3 | Value_3 | Another one 3 |
| 4 | Value_4 | Another one 4 |


