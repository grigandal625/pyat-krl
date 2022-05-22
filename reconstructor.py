from lark.reconstruct import Reconstructor
from lark import Token, Tree

from kbparser import parser
from tree_transformer import transform


class MyReconstructor(Reconstructor):

    def _reconstruct(self, tree: Tree):
        unreduced_tree = self.match_tree(tree, tree.data)
        res = self.write_tokens.transform(unreduced_tree)
        for item in res:
            if isinstance(item, Tree):
                # TODO use orig_expansion.rulename to support templates
                yield from self._reconstruct(item)
            else:
                yield item


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


reconstructor = MyReconstructor(
    parser, {'_NEWLINE': special, '_DEDENT': special, '_INDENT': special})


if __name__ == '__main__':
    tree = parser.parse(r"""
ruledef HelloRule:
    '''
    Test Rule
    '''
    if(a, x=None):
        ((x == 7) or
        (y in [10, 'yes']))
    then:
        return x + 17
""", start='file_input')
    tree = transform(tree)
    output = reconstructor.reconstruct(tree, postproc)
    print(output)