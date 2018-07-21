import os

from flask_admin import BaseView, expose
from google.protobuf.json_format import MessageToDict

from app.lnd_client.lightning_client import LightningClient


class LightningDashboardView(BaseView):
    @expose('/')
    def index(self):
        rpc_uri = os.environ.get('LND_RPC_URI', '127.0.0.1:10009')
        peer_uri = os.environ.get('LND_PEER_URI', '127.0.0.1:9735')
        ln = LightningClient(rpc_uri=rpc_uri, peer_uri=peer_uri)

        lnd_info = ln.get_info()
        if lnd_info is False:
            lnd_info = {}
        else:
            lnd_info = MessageToDict(lnd_info)


        peers = ln.get_peers()
        if not peers:
            peers = {'No peers': ' '}
        else:
            peers = MessageToDict(peers)['peers']

        channels = ln.get_channels()
        if not channels:
            channels = {'No channels': ' '}
        else:
            channels = MessageToDict(channels)['channels']

        return self.render('admin/lnd/lnd_dashboard.html',
                           lnd_info=lnd_info,
                           peers=peers,
                           channels=channels)
