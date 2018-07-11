import os

from flask import flash, request
from flask_admin import AdminIndexView, expose
from markupsafe import Markup

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.bitcoind_client.forms import MineBlocksForm
from app.constants import DEFAULT_NETWORK



class BlockchainView(AdminIndexView):

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        bitcoin = BitcoinClient()

        mine_blocks_form = MineBlocksForm(request.form)
        if request.method == 'POST' and mine_blocks_form.validate():
            try:
                num_blocks_to_mine = mine_blocks_form.num_blocks.data

                num_blocks_mined = len(block_hashes)
                flash(f'{num_blocks_mined} blocks mined')
            except Exception as exc:
                err = {'Error': str(exc)}
                flash(err)

        try:
            blockchain_info = proxy.call('getblockchaininfo')
        except Exception as exc:
            blockchain_info = {'Error': str(exc)}

        try:
            mempool_info = proxy.call('getmempoolinfo')
        except Exception as exc:
            mempool_info = {'Error': str(exc)}

        try:
            wallet_info = proxy.call('getwalletinfo')
        except Exception as exc:
            wallet_info = {'Error': str(exc)}

        try:
            new_address = {
                'bech32': proxy.call('getnewaddress', '', 'bech32'),
                'p2sh-segwit': proxy.call('getnewaddress', '', 'p2sh-segwit'),
                'legacy': proxy.call('getnewaddress', '', 'legacy'),
            }
            if blockchain_info['chain'] == 'test':
                testnet_faucet = 'https://testnet.coinfaucet.eu/'
                new_address['Get testnet coins'] = Markup(
                    f'<a target="_blank" href="{testnet_faucet}">{testnet_faucet}</a>')
        except Exception as exc:
            new_address = {'Error': str(exc)}

        websocket_port = os.environ.get('WEBSOCKET_PORT', 8765)
        return self.render('admin/bitcoind_home.html',
                           websocket_port=websocket_port,
                           blockchain_info=blockchain_info,
                           mempool_info=mempool_info,
                           wallet_info=wallet_info,
                           new_address=new_address,
                           network=os.environ.get('NETWORK', DEFAULT_NETWORK),
                           mine_blocks_form=mine_blocks_form,
                           )

