from datetime import datetime


def format_timestamp(view, context, model, name):
    timestamp = getattr(model, name)
    return str(datetime.fromtimestamp(timestamp))

def format_hash(view, context, model, name):
    hash = getattr(model, name)
    return hash[-20:]
