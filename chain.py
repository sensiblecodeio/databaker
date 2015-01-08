import functools

class Chain(object):
    def invoke(self, __sw_name, *args, **kwargs):
        print "args", args, kwargs
        chain = list(self.chain)
        chain.append([__sw_name, args, kwargs])
        return Chain(self.target, chain=chain) # TODO

    def missing(self, name):
        # chain.append(name)
        return functools.partial(self.invoke, name)

    def __init__(self, target, chain=None):
        self.target = target
        self.chain = chain or []

    def __getattr__(self,name):
        print "name", name
        return self.missing(name)

    def __repr__(self):
        return "Chain({}, {!r})".format(self.target.__name__, self.chain)



def sheet_object(*args, **kwargs):
    print args, kwargs

sheet = Chain(target=sheet_object)
down = 1
right = 2

def is_number(n):
    return n == 55
q = Chain(sheet_object).a1('a2').b1('b2')# .ocelot
print q, type(q)

z = q.foo
print z, type(z)
exit()

