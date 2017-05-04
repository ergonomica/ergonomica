from tokenizer import tokenize

# Test it out
data = '''
function f {ls}
'''

print('\n'.join(map(str, tokenize(data))))
