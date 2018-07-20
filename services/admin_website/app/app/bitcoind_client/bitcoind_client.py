import platform
from typing import Tuple, List
import os

import bitcoin.rpc
from markupsafe import Markup

from app.constants import DEFAULT_NETWORK, TESTNET_FAUCET


class BitcoinClient(object):
    def __init__(self):
        self.network = os.environ.get('NETWORK', DEFAULT_NETWORK)
        bitcoin.SelectParams(self.network)

    @property
    def proxy(self):

        conf_file = f'bitcoind-{self.network}.conf'

        # Check for the standard spot for configuration files
        if platform.system() == 'Darwin':
            btc_conf_path = os.path.expanduser('~/Library/Application Support/Bitcoin/')
        elif platform.system() == 'Windows':
            btc_conf_path = os.path.join(os.environ['APPDATA'], 'Bitcoin')
        else:
            btc_conf_path = os.path.expanduser('~/.bitcoin')

        if not os.path.exists(os.path.join(btc_conf_path, conf_file)):
            btc_conf_path = os.path.dirname(os.path.abspath(__file__))

        btc_conf_path = os.path.join(btc_conf_path, conf_file)
        return bitcoin.rpc.Proxy(btc_conf_file=btc_conf_path)

    def generate(self, num_blocks_to_mine: int) -> Tuple[str, str]:
        try:
            block_hashes = self.proxy.call('generate', num_blocks_to_mine)
            num_blocks_mined = len(block_hashes)
            message = f'{num_blocks_mined} blocks mined'
            category = 'info'
        except Exception as exc:
            message = str(exc)
            category = 'error'
        return message, category

    def create_transaction(self):
        destinations = self.get_new_addresses()
        amount = self.get_wallet_info()['balance']


    def get_block_count(self) -> int:
        block_count = self.proxy.call('getblockcount')
        return block_count

    def get_block_hash(self, block_height: int) -> str:
        block_hash = self.proxy.call('getblockhash', block_height)
        return block_hash

    def get_block(self, block_hash: str = None, verbosity: int = 1) -> dict:

        if block_hash is None:
            block_hash = self.get_best_block_hash()

        block = self.proxy.call('getblock', block_hash, verbosity)
        return block

    def get_recent_txid(self):
        block = self.get_block()
        transactions = block['tx']
        return transactions[0]

    def get_blocks(self, last_block_hash: str, count: int = 10) -> List[dict]:
        blocks = []
        find_block_hash = None

        while len(blocks) < count:
            block = self.get_block(find_block_hash or last_block_hash, 1)
            blocks.append(block)
            find_block_hash = block.get('previousblockhash')
            if find_block_hash is None:
                break

        return blocks

    def get_best_block_hash(self) -> str:
        best_block_hash = self.proxy.call('getbestblockhash')
        return best_block_hash

    def get_most_recent_blocks(self, count: int = 10) -> List[dict]:
        best_block_hash = self.get_best_block_hash()
        blocks = self.get_blocks(last_block_hash=best_block_hash, count=count)
        return blocks

    def get_network_info(self) -> dict:
        try:
            network_info = self.proxy.call('getnetworkinfo')
        except Exception as exc:
            network_info = {'Error': str(exc)}
        return network_info

    def get_blockchain_info(self) -> dict:
        try:
            blockchain_info = self.proxy.call('getblockchaininfo')
        except Exception as exc:
            blockchain_info = {'Error': str(exc)}
        return blockchain_info

    def get_transaction_stats(self) -> dict:
        try:
            transaction_stats = self.proxy.call('getchaintxstats')
        except Exception as exc:
            transaction_stats = {'Error': str(exc)}
        return transaction_stats

    def get_block_stats(self, block_hash: str = None,
                        block_height: int = None) -> dict:
        too_few_args = block_hash is None and block_height is None
        too_many_args = block_hash is not None and block_height is not None
        if too_few_args or too_many_args:
            raise ValueError('get_block_stats requires either block_hash or block_height')
        try:
            block_stats = self.proxy.call('getblockstats', block_hash or block_height)
        except Exception as exc:
            block_stats = {'Error': str(exc)}
        return block_stats

    def get_mempool_info(self) -> dict:
        try:
            mempool_info = self.proxy.call('getmempoolinfo')
        except Exception as exc:
            mempool_info = {'Error': str(exc)}
        return mempool_info

    def get_raw_mempool(self, verbose: bool = True) -> dict:
        mempool_entries = self.proxy.call('getrawmempool', verbose)
        return mempool_entries

    def get_mempool_entry(self, txid: str) -> dict:
        mempool_entry = self.proxy.call('getmempoolentry', txid)
        return mempool_entry

    def get_raw_transaction(self, txid: str, verbose: bool = True,
                            block_hash: str = None) -> dict:
        tx = self.proxy.call('getrawtransaction', txid, verbose, block_hash)
        return tx

    def get_wallet_info(self) -> dict:
        wallet_info = self.proxy.call('getwalletinfo')
        return wallet_info

    def get_new_addresses(self, chain: str = None) -> dict:
        address_types = ['bech32', 'p2sh-segwit', 'legacy']
        try:
            new_addresses = {t: self.proxy.call('getnewaddress', '', t) for t in
                             address_types}
            if chain == 'test':
                new_addresses['Get testnet coins'] = Markup(
                    f'<a target="_blank" href="{TESTNET_FAUCET}">{TESTNET_FAUCET}</a>')
        except Exception as exc:
            new_addresses = {'Error': str(exc)}

        return new_addresses
