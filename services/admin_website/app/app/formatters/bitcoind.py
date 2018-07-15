from datetime import datetime

from jinja2.runtime import Context

from app.bitcoind_client.models.blocks import Blocks


def format_block_txids(view, context: Context,
                       model: Blocks, name: str):
    return len(getattr(model, name))

def format_timestamp(view, context, model, name):
    timestamp = getattr(model, name)
    return str(datetime.fromtimestamp(timestamp))

def format_hash(view, context, model, name):
    hash = getattr(model, name)
    return hash[-20:]