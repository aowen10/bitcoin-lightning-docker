import os

from flask_admin import expose, BaseView

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.constants import DEFAULT_NETWORK



class TransactionView(BaseView):
    """
    getrawtransaction
    """

    @expose('/<txid>/')
    def index(self, txid):
        bitcoin = BitcoinClient()

        transaction = bitcoin.get_raw_transaction(txid)

        return self.render('admin/bitcoind/transaction.html',
                           transaction=transaction
                           )

