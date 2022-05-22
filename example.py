import test_kb
import kbmodule
kbmodule.add_hook()


print("CHECKING RULE 1", test_kb.TestRule().check(1))
test_kb.TestRule().fire()

r2 = test_kb.TestRule2()
if r2.check():
    r2.fire('hello')
