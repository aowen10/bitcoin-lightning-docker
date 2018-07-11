import os

from flask_admin import AdminIndexView, expose

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.constants import DEFAULT_NETWORK



class BlockchainView(AdminIndexView):
    """
    getblockchaininfo
    getchaintxstats
    getblockstats
    """

    @expose('/')
    def index(self):
        bitcoin = BitcoinClient()

        blockchain_info = bitcoin.get_blockchain_info()

        websocket_port = os.environ.get('WEBSOCKET_PORT', 8765)

        return self.render('admin/bitcoind/blockchain.html',
                           websocket_port=websocket_port,
                           blockchain_info=blockchain_info,
                           network=os.environ.get('NETWORK', DEFAULT_NETWORK),
                           )

