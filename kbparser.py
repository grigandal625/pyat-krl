from lark.lark import Lark
from lark.indenter import PythonIndenter

from grammar import GRAMMAR

parser = Lark(GRAMMAR, start=[
              'single_input', 'file_input', 'eval_input'], postlex=PythonIndenter(), maybe_placeholders=False)

if __name__ == '__main__':
    tree = parser.parse(r"""
ruledef TestRule:
    '''
    TEST RULE
    '''
    if(x=None):
        5 == x
    then:
        print(chr)
        print("hello")
""", "file_input")
    print(tree)