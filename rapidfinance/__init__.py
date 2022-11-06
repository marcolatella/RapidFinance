from .configuration import Config


import yaml
import os

config = Config()
endpoints = Config()

filename = os.path.join(config.curr_dir, "config.yaml")

with open(filename, "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    config.load_data(data)

# config.base_url = 'https://' + config.rapid_api_host + '/'
# config.headers = {
#    "X-RapidAPI-Key": config.rapid_api_key,
#    "X-RapidAPI-Host": config.rapid_api_host
#}


endpoints_file = os.path.join(endpoints.curr_dir, "endpoints.yaml")
with open(endpoints_file, "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    endpoints.load_data(data)


__all__ = ['config',
           'endpoints']


