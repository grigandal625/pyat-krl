GRAMMAR = r"""
%import common.WS
%import python (compound_stmt, single_input, file_input, eval_input, test, suite, parameters, _NEWLINE, _INDENT, _DEDENT, COMMENT, NAME)
%extend compound_stmt: rule_stmt

rule_stmt: "ruledef" NAME ":" rule_definition
rule_definition: _NEWLINE _INDENT [suite] rule_body _DEDENT

rule_body: "if" condition_params ":" condition "then" action_params ":" action

condition_params: ["(" parameters ")"]
condition: _NEWLINE _INDENT test _NEWLINE _DEDENT
action_params: ["(" parameters ")"]
action: suite

%ignore /[\t \f]+/          // WS
%ignore /\\[\t \f]*\r?\n/   // LINE_CONT
%ignore COMMENT
%ignore WS
"""
