class Chain(object):
    def invoke(self, *args, **kwargs):
        print "args", args, kwargs
        chain = list(self.chain)
        chain.append([args, kwargs])
        return Chain(self.target, chain=chain) # TODO

    def missing(self, name):
        # chain.append(name)
        return self.invoke

    def __init__(self, target, chain=None):
        self.target = target
        self.chain = chain or []

    def __getattr__(self,name):
        print "name", name
        return self.missing(name)

    def __repr__(self):
        return "Chain({!r}, {!r})".format(self.target, self.chain)


sheet = Chain(target='sheet_object')
down = 1
right = 2

def is_number(n):
    return n == 55
q = Chain('a').b1('b2').c1('c2')# .ocelot
print q
exit()

