from typing import Tuple
import os

import bitcoin.rpc
from markupsafe import Markup

from app.constants import DEFAULT_NETWORK, TESTNET_FAUCET


class BitcoinClient(object):
    def __init__(self):
        network = os.environ.get('NETWORK', DEFAULT_NETWORK)
        bitcoin.SelectParams(network)
        self.proxy = bitcoin.rpc.Proxy(btc_conf_file='bitcoin.conf')

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

    def get_wallet_info(self) -> dict:
        try:
            wallet_info = self.proxy.call('getwalletinfo')
        except Exception as exc:
            wallet_info = {'Error': str(exc)}
        return wallet_info

    def get_new_addresses(self, chain: str) -> dict:
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
