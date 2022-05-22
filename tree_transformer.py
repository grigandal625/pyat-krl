from lark import Tree, Token

DEFAULT_GLOBALS = [f for f in __builtins__]

RULE_INHERITENCE = Tree('python__arguments', [Tree('python__getattr', [
                        Tree('python__var', [Token('NAME', 'rule')]), Token('NAME', 'Rule')])])
PYTHON_STAR_ARGS = Tree("python__starparams", [Tree("python__starparam", [Token("NAME", "args")]), Tree(
    "python__poststarparams", [Tree("python__kwparams", [Token("NAME", "kwargs")],)],), ],)


def transform(tree: Tree):
    return replace_rules_to_classes(tree)


def replace_rules_to_classes(item):
    if isinstance(item, Tree):
        data = item.data
        if isinstance(data, Token) and data.type == 'RULE' and data.value == 'rule_stmt':
            return rule_to_class(item)
        else:
            return Tree(
                item.data,
                [replace_rules_to_classes(child) for child in item.children]
            )
    return item


def rule_to_class(rule_tree: Tree):
    return Tree(
        'python__classdef',
        [
            Token('NAME', get_rule_name(rule_tree)),
            RULE_INHERITENCE,
            get_rule_body(rule_tree)
        ]
    )


def get_rule_name(rule_tree: Tree):
    return rule_tree.children[0].value


def get_rule_body(rule_tree: Tree):
    return Tree(
        Token('RULE', 'suite'), 
        [
            get_rule_check_method(rule_tree), 
            get_rule_fire_method(rule_tree)
        ]
    )


def get_rule_check_method(rule_tree: Tree):
    rule_def_tree = rule_tree.children[1]
    rule_body_tree = [c for c in rule_def_tree.children if isinstance(c, Tree) and c.data == 'rule_body'][0]
    
    condition_param_tree = [c for c in rule_body_tree.children if isinstance(c, Tree) and c.data == 'condition_params'][0] 
    condition_tree = [c for c in rule_body_tree.children if isinstance(c, Tree) and c.data == 'condition'][0]
    
    returning_expression = condition_tree.children[0]
    params = [Token("NAME", 'self')]
    if len(condition_param_tree.children):
        param_list_tree = condition_param_tree.children[0]
        for p in param_list_tree.children:
            params.append(p)

    return Tree(
        "python__funcdef",
        [
            Token("NAME", "check"),
            Tree(
                "parameters",
                params,
            ),
            Tree("python__var", [Token("NAME", "bool")]),
            Tree(
                Token("RULE", "suite"),
                [
                    Tree(
                        "python__return_stmt",
                        [returning_expression]
                    )
                ]
            )
        ])


def get_rule_fire_method(rule_tree: Tree):
    rule_def_tree = rule_tree.children[1]
    rule_def_tree = rule_tree.children[1]
    rule_body_tree = [c for c in rule_def_tree.children if isinstance(c, Tree) and c.data == 'rule_body'][0]
    
    action_param_tree = [c for c in rule_body_tree.children if isinstance(c, Tree) and c.data == 'action_params'][0] 
    action_tree = [c for c in rule_body_tree.children if isinstance(c, Tree) and c.data == 'action'][0]
    
    action_suite = action_tree.children[0]
    params = [Token("NAME", 'self')]
    if len(action_param_tree.children):
        param_list_tree = action_param_tree.children[0]
        for p in param_list_tree.children:
            params.append(p)

    return Tree(
        "python__funcdef",
        [
            Token("NAME", "fire"),
            Tree(
                "parameters",
                params,
            ),
            action_suite
        ])
