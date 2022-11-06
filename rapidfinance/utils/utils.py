
def to_dict(text):
    text = text.replace("null", "None")
    text = text.replace("false", "False")
    text = text.replace("true", "True")
    return eval(text)