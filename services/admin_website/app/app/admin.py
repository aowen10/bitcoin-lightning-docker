import os
import random
import string

from flask import Flask, redirect
from flask_admin import Admin

from app.bitcoind_client.admin.blockchain_view import BlockchainView
from app.bitcoind_client.admin.blocks_model_view import BlocksModelView
from app.bitcoind_client.models.blocks import Blocks
from app.lnd_client.admin.channels_model_view import ChannelsModelView
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
    admin = Admin(app=app,
                  name='Bitcoin/LN',
                  template_mode='bootstrap3',
                  )
    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    if secret_key is None:
        secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        os.environ['FLASK_SECRET_KEY'] = secret_key
    app.config['SECRET_KEY'] = secret_key


    @app.route('/')
    def index():
        return redirect('/admin')

    admin.add_view(BlockchainView(name='Blockchain',
                                  endpoint='blockchain',
                                  category='Bitcoin'))

    admin.add_view(BlocksModelView(Blocks,
                                   name='Blocks',
                                   category='Bitcoin'))

    admin.add_view(LightningDashboardView(name='Dashboard',
                                          endpoint='lightning',
                                          category='LND'))

    admin.add_view(TransactionsModelView(Transaction,
                                         name='Transactions',
                                         category='LND'))

    admin.add_view(PeersModelView(Peer,
                                  name='Peers',
                                  category='LND'))

    admin.add_view(ChannelsModelView(Channel,
                                    name='Channels',
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
    app.run(port=5003)
