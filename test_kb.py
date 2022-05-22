# $kbmodule
global_var = 5


def do_someth_external():
    print("doing external")


ruledef TestRule:
    """
    THIS IS SIMPLE TEST RULE
    """
    if(local_if_var):
        (
            global_var == local_if_var * 5 and
            local_if_var > 0
        )
    then:
        print(self)
        do_someth_external()


ruledef TestRule2:
    """
    THIS IS SIMPLE TEST RULE 2
    """
    if:
        bool(global_var)
    then(local_then_var):
        print(local_then_var)
        do_someth_external()
