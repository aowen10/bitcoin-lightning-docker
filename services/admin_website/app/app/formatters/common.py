from datetime import datetime


def format_timestamp(view, context, model, name):
    timestamp = getattr(model, name)
    return str(datetime.fromtimestamp(timestamp))


def format_hash(view, context, model, name):
    hash = getattr(model, name)
    return hash[-20:]


def format_amount(amount):
    if amount:
        currency_string = "{0:,d}".format(amount)
        if currency_string.startswith('-'):
            currency_string = currency_string.replace('-', '(')
            currency_string += ')'
        return currency_string
    else:
        return '-'


def satoshi_formatter(view, context, model, name):
    amount = getattr(model, name)
    return format_amount(amount)
