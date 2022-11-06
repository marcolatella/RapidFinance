import os


class Config(dict):
    def __init__(self):
        super(Config, self).__init__()

    def load_data(self, data):
        for key, val in data.items():
            self[key] = val

    # def __setitem__(self, key: str, value):
    #    super(Config, self).__setitem__(key, value)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    def __delattr__(self, item):
        del self[item]

    @property
    def curr_dir(self):
        """System current directory."""
        return os.getcwd()
