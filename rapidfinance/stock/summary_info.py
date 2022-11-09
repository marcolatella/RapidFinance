
class Summary(object):
    def __init__(self, info):
        super(Summary, self).__init__()

        for k, v in info.items():
            if isinstance(v, dict):
                v = Summary(v)
            self.__dict__[k] = v

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            raise AttributeError

    def __repr__(self):
        res = ""
        for k, v in self.__dict__.items():
            res += f"{k}: {v}\n"
        return res

    def __missing__(self, key):
        return False

