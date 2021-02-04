

class ConstantEngine(object):
    """
    Used for HDimConst dimensions.
    Using the engine pattern to keep the logic clean
    """
    def __init__(self, overrides):
        self.constant = overrides[None]

    def lookup(self, cell):
        # TODO - rework this? We don't need the cell, we already know it's None 
        return None, self.constant