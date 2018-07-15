from jinja2.runtime import Context
from markupsafe import Markup

from app.bitcoind_client.models.blocks import Blocks


def format_block_txids(view, context: Context,
                       model: Blocks, name: str):
    print('here')
    return getattr(model, name)[0:3]