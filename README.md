# Py2MD

## Tag Reference

| Tag | Desc |
| --- | ---- |
| `p` | Paragraph |
| `h` | Heading |
| `q` | Quote |
| `c` | CodeBlock |
| `fn` | Footnotes |
| `url` | URL |
| `li` | BulletList |
| `t` | Tabular |
| `th` | TabularHeader |
| `b` | Breakline |
| `end` | Endline |
| `lit` | Literal |


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

> <b><i>Italic Bold</i></b> << although normally html inline formatting wtill works just fine. 
>> also multilevel Quote Block 
>>>>>>>>>> Sandwiches at cheap price !? !?. 
>>>>>>>>>>> satisfactory. 


| Index | This will | parse as Table |
| ----- | --------- | -------------- |
| 0 | Value_0 | Another one 0 |
| 1 | Value_1 | Another one 1 |
| 2 | Value_2 | Another one 2 |
| 3 | Value_3 | Another one 3 |
| 4 | Value_4 | Another one 4 |


