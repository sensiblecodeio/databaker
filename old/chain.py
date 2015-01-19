import functools

def evaluate_chain(chain):
    if isinstance(chain, functools.partial):
        return chain(__sw_stop=True).evaluate()
    else:
        return chain.evaluate()


class Chain(object):
    def __init__(self, target, chain=None):
        self.target = target
        self.chain = chain or []

    def add_to_chain(self, __sw_name, *args, **kwargs):
        chain = list(self.chain)
        chain.append([__sw_name, args, kwargs])
        return Chain(self.target, chain=chain)

    def __getattr__(self,name):
        return functools.partial(self.add_to_chain, name)

    def __repr__(self):
        return "Chain({}, {!r})".format(self.target.__name__, self.chain)

    def evaluate(self):
        target = self.target
        for [name, args, kwargs] in self.chain:
            if '__sw_stop' in kwargs:
                return getattr(target, name)
            target = getattr(target, name)(*args, **kwargs)
        return target

class SheetObject(object):
    # just a demo object
    def __name__(self):
        return 'foo'

    def __init__(self, *args, **kwargs):
        self.foo = 12

    def a1(self, v):
        assert v=='a2'
        return SheetObject()

    def b1(self, v):
        assert v=='b2'
        return SheetObject()



sheet = Chain(target=SheetObject())
# example constants
down = 1
right = 2

def is_number(n):
    return n == 55

q = Chain(SheetObject()).a1('a2').b1('b2')# .ocelot
print q
print evaluate_chain(q)
z = q.foo
print z, type(z)
print evaluate_chain(z)

