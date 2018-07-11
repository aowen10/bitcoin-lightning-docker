from typing import List
import os

import bitcoin.rpc

from app.constants import DEFAULT_NETWORK


class BitcoinClient(object):
    def __init__(self):
        network = os.environ.get('NETWORK', DEFAULT_NETWORK)
        bitcoin.SelectParams(network)
        self.proxy = bitcoin.rpc.Proxy(btc_conf_file='bitcoin.conf')

    def generate(self, num_blocks_to_mine: int) -> List[str]:
        block_hashes = self.proxy.call('generate', num_blocks_to_mine)
        return block_hashes

