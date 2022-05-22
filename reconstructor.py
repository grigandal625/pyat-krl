from lark.reconstruct import Reconstructor
from lark import Token, Tree

from kbparser import parser
from tree_transformer import transform


def special(sym):
    return Token('SPECIAL', sym.name)


def postproc(items):
    indent_level = 0
    actions = []
    for item in items:
        if isinstance(item, Token):
            if item.type == 'SPECIAL':
                if item.value == '_NEWLINE':
                    actions.append('_NEWLINE')
                    yield '\n'
                elif item.value == '_INDENT':
                    actions.append('_INDENT')
                    indent_level += 1
                elif item.value == '_DEDENT':
                    actions.append('_DEDENT')
                    indent_level -= 1
                else:
                    if actions and actions[0] == '_NEWLINE':
                        actions.clear()
                        yield ' ' * 4 * indent_level
                    yield item
            else:
                if actions and actions[0] == '_NEWLINE':
                    actions.clear()
                    yield ' ' * 4 * indent_level
                yield item
        else:
            if actions and actions[0] == '_NEWLINE':
                actions.clear()
                yield ' ' * 4 * indent_level
            yield item


def compile_kb(source):
    reconstructor = Reconstructor(
        parser, {'_NEWLINE': special, '_DEDENT': special, '_INDENT': special})
    tree = parser.parse(source, "file_input")
    tree = transform(tree)
    return reconstructor.reconstruct(tree, postproc)
    

if __name__ == '__main__':
    compiled = compile_kb(r"""
ruledef HelloRule:
    '''
    Test Rule
    '''
    if(a, x=None):
        ((x == 7) or
        (y in [10, 'yes']))
    then:
        return x + 17
""")
    print(compiled)
