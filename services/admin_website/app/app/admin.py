from flask import Flask, redirect
from flask_admin import Admin

from app.bitcoind_client.admin.blockchain_view import BlockchainView
from app.bitcoind_client.admin.blocks_model_view import BlocksModelView
from app.bitcoind_client.admin.mempool_entries_model_view import \
    MempoolEntriesModelView
from app.bitcoind_client.admin.transaction_view import TransactionView
from app.bitcoind_client.admin.wallet_view import WalletView
from app.bitcoind_client.models.blocks import Blocks
from app.bitcoind_client.models.mempool_entries import MempoolEntries
from app.constants import FLASK_SECRET_KEY
from app.lnd_client.admin.open_channels_model_view import OpenChannelsModelView
from app.lnd_client.admin.dashboard_view import LightningDashboardView
from app.lnd_client.admin.invoices_model_view import InvoicesModelView
from app.lnd_client.admin.payments_model_view import PaymentsModelView
from app.lnd_client.admin.peers_model_view import PeersModelView
from app.lnd_client.admin.transactions_model_view import TransactionsModelView
from app.lnd_client.grpc_generated.rpc_pb2 import (
    Channel,
    Invoice,
    Payment,
    Peer,
    Transaction
)


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY

    admin = Admin(app=app,
                  name='Bitcoin/LN',
                  template_mode='bootstrap3',
                  )

    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

    @app.route('/')
    def index():
        return redirect('/admin')

    admin.add_view(WalletView(name='Wallet Info',
                              endpoint='bitcoin',
                              category='Bitcoin Wallet'))

    admin.add_view(BlockchainView(name='Blockchain',
                                  endpoint='blockchain',
                                  category='Bitcoin'))

    admin.add_view(BlocksModelView(Blocks,
                                   name='Blocks',
                                   category='Bitcoin'))

    admin.add_view(TransactionView(name='Transaction',
                                   endpoint='bitcoin-transaction',
                                   category='Bitcoin'))

    admin.add_view(MempoolEntriesModelView(MempoolEntries,
                                           name='Mempool Entries',
                                           category='Bitcoin'))

    admin.add_view(LightningDashboardView(name='Dashboard',
                                          endpoint='lightning',
                                          category='LND'))

    admin.add_view(TransactionsModelView(Transaction,
                                         name='LND Transactions',
                                         category='LND'))

    admin.add_view(PeersModelView(Peer,
                                  name='Peers',
                                  category='LND'))

    admin.add_view(OpenChannelsModelView(Channel,
                                     name='Open Channels',
                                     category='LND'))

    admin.add_view(InvoicesModelView(Invoice,
                                     name='Invoices',
                                     category='LND'))

    admin.add_view(PaymentsModelView(Payment,
                                     name='Payments',
                                     category='LND'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5013)
