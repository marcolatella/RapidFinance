
class Summary(dict):
    def __init__(self, info):
        super(Summary, self).__init__()

        for k, v in info.items():
            self[k] = v

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    def __repr__(self):
        res = ""
        for k, v in self.items():
            res += f"{k}: {v}\n"
        return res
