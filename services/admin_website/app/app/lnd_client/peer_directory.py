from collections import namedtuple, defaultdict

import os

Peer = namedtuple('Peer', ['pub_key', 'address', 'name'])


def build_directory():
    htlc_dot_me_testnet = Peer(
        '03193d512b010997885b232ecd6b300917e5288de8785d6d9f619a8952728c78e8',
        '18.205.112.169:9735',
        'htlc.me')

    yalls_testnet = Peer(
        '02212d3ec887188b284dbb7b2e6eb40629a6e14fb049673f22d2a0aa05f902090e',
        'testnet-lnd.yalls.org',
        "Y'alls"
    )

    satoshis_place_testnet = Peer(
        '02dd4cef0192611bc34cd1c3a0a7eb0f381e7229aa3309ae961a7fc0076b4d2bb6',
        '35.198.136.5:9735',
        "Satoshi's Place"
    )

    testnet_peers = [
        htlc_dot_me_testnet,
        yalls_testnet,
        satoshis_place_testnet
    ]

    def peer_factory():
        return Peer(None, None, '')

    testnet_directory = defaultdict(peer_factory)
    for peer in testnet_peers:
        testnet_directory[peer.pub_key] = peer

    if os.environ.get('NETWORK', 'testnet'):
        return testnet_directory
    else:
        return []


peer_directory = build_directory()
