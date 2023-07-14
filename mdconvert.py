from polydoc.parse.utils import markdown2html

markdown = '''

# heading 1
## heading 2
### heading 3
#### heading 4

foo bar *italics* baz **bold** [link](to nowhere)
- item1
- item2
- item3

1. thing
2. another
3. final
'''

print(markdown)
print('--')
print(markdown2html(markdown))