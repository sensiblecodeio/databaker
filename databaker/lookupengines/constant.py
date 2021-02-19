

class ConstantEngine(object):
    """
    Used for HDimConst dimensions.
    Using the engine pattern to keep the logic clean
    """
    def __init__(self, overrides):
        assert len(overrides) == 1 and None in overrides, "single value type should have cellvalueoverride={None:defaultvalue}"
        self.constant = overrides[None]

    def lookup(self, cell):
        return None, self.constant