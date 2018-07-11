import os

from flask import flash, request
from flask_admin import AdminIndexView, expose

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.bitcoind_client.forms import MineBlocksForm
from app.constants import DEFAULT_NETWORK



class BlockchainView(AdminIndexView):

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        bitcoin = BitcoinClient()

        mine_blocks_form = MineBlocksForm(request.form)
        if request.method == 'POST' and mine_blocks_form.validate():
            num_blocks_to_mine = mine_blocks_form.num_blocks.data
            message, category = bitcoin.generate(num_blocks_to_mine=num_blocks_to_mine)
            flash(message=message, category=category)

        blockchain_info = bitcoin.get_blockchain_info()
        mempool_info = bitcoin.get_mempool_info()
        wallet_info = bitcoin.get_wallet_info()
        new_addresses = bitcoin.get_new_addresses(chain=blockchain_info.get('chain'))

        websocket_port = os.environ.get('WEBSOCKET_PORT', 8765)

        return self.render('admin/bitcoind_home.html',
                           websocket_port=websocket_port,
                           blockchain_info=blockchain_info,
                           mempool_info=mempool_info,
                           wallet_info=wallet_info,
                           new_address=new_addresses,
                           network=os.environ.get('NETWORK', DEFAULT_NETWORK),
                           mine_blocks_form=mine_blocks_form,
                           )

