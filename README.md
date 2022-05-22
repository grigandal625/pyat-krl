# Production rules representation language based on python

## Installation

requires python3.9, could be changed in `Pipfile`

1. `pip3 install pipenv`
2. `pipenv install`
3. Now we can run `pipenv run python example`

## Usage

1. Create a python file (i'l name it `my_kb.py`)
2. Write exactly this comment at the beginning of the file
    ```python
    # $kbmodule
    ```
3. Now you can write some production rules like:

    ```python
    # $kbmodule

    x = 0
    ruledef SimpleRule:
        if:                     # you can provide arguments here to use locally like if(a, b=None): ...
            not x
        then:                   # you can also provide arguments
            print('RULE FIRED')
            # do smth else
    ```

4. To use your knowledge base in other python module, write this:

    ```python
    import kbmodule
    kbmodule.add_hook()

    # and now we can import our rule from my_kb.py

    import my_kb

    rule_instance = my_kb.SimpleRule()
    print(rule_instance.check())        # prints True. if arguments are provided, you have to provide required values to this method
    if rule_instance.check():
        rule_instance.fire()            # prints "RULE FIRED". Also don't forget about your arguments
    ```

## P.S.

Extra thanks to: [ideas](https://github.com/aroberge/ideas) & [lark-parser](https://github.com/lark-parser/lark)
