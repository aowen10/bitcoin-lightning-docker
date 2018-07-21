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

        try:
            lnd_info = ln.get_info()
            lnd_info = MessageToDict(lnd_info)
        except Exception as exc:
            lnd_info = {'Error': ' '.join([str(type(exc)), str(exc)])}

        try:
            peers = ln.get_peers()
            peers = MessageToDict(peers)['peers']
            if not peers:
                peers = {'No peers': ' '}
        except Exception as exc:
            peers = {'Error': ' '.join([str(type(exc)), str(exc)])}

        try:
            channels = ln.get_channels()
            channels = MessageToDict(channels)['channels']
            if not channels:
                channels = {'No channels': ' '}
        except Exception as exc:
            channels = {'Error': ' '.join([str(type(exc)), str(exc)])}

        return self.render('admin/lnd/lnd_dashboard.html',
                           lnd_info=lnd_info,
                           peers=peers,
                           channels=channels)
