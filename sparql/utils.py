class strictDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError("{} is not a legal key of this strictDict".format(repr(key)))
        dict.__setitem__(self, key, value)