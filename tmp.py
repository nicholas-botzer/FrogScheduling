import argparse, sys, logging


x = 'glob_x'
def outer():
    x = 'outer_x'
    def inner()
        #x = 'iner_x'; print(x)
        nonloca x; print(x)
        global x; print(x)
    inner()
outer()
sys.exit(0)

class cls:
    pass
def method():
    pass

print(f'dir(cls)',dir(cls))
print(f'dir(method)',dir(method))


sys.exit(0)
print(f'dir({__name__})',dir(__name__))

print(f'globals()',globals())