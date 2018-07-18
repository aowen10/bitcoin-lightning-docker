from flask import flash, request, redirect, url_for
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.model.fields import AjaxSelectField
from wtforms import StringField, Form

from app.formatters.lnd import pub_key_formatter
from app.lnd_client.admin.ajax_model_loaders import \
    PeersDirectoryAjaxModelLoader
from app.lnd_client.admin.lnd_model_view import LNDModelView
from app.lnd_client.grpc_generated.rpc_pb2 import LightningAddress, Peer


class PeersModelView(LNDModelView):
    can_create = True
    can_delete = True
    create_form_class = LightningAddress
    get_query = 'get_peers'
    primary_key = 'pub_key'

    column_default_sort = 'pub_key'
    list_template = 'admin/peers_list.html'
    column_formatters = {
        'pub_key': pub_key_formatter
    }

    def scaffold_form(self) -> Form:
        form_class = super(PeersModelView, self).scaffold_form()
        peer_directory_ajax_loader = PeersDirectoryAjaxModelLoader(
            'node_pubkey_string',
            options=None,
            model=Peer,
            placeholder='Select node pubkey')

        old = form_class.node_pubkey_string
        ajax_field = AjaxSelectField(loader=peer_directory_ajax_loader,
                                     label='node_pubkey_string',
                                     allow_blank=True,
                                     description=old.kwargs['description'])

        form_class.pubkey_at_host = ajax_field
        return form_class

    def create_model(self, form_data):
        if hasattr(form_data, 'data'):
            form_data = form_data.data
        if form_data.get('pubkey_at_host'):
            pubkey = form_data.get('pubkey_at_host').split('@')[0]
            host = form_data.get('pubkey_at_host').split('@')[1]
        else:
            pubkey = form_data.get('pubkey')
            host = form_data.get('host')
        try:
            self.ln.connect_peer(pubkey=pubkey, host=host)
        except Exception as exc:
            flash(gettext(exc._state.details), 'error')
            return
        new_peer = [p for p in self.ln.get_peers() if p.pub_key == pubkey][0]
        return new_peer

    def delete_model(self, model: Peer):
        try:
            response = self.ln.disconnect_peer(pub_key=model.pub_key)
            return True
        except Exception as exc:
            if hasattr(exc, '_state'):
                flash(gettext(exc._state.details), 'error')
            else:
                flash(gettext(str(exc)))
            return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        if request.method == 'POST':
            self.create_model(request.form.copy())
            return redirect(url_for('peer.index_view'))

        FormClass = self.scaffold_form()

        self._template_args['add_peer_form'] = FormClass()
        return super(PeersModelView, self).index_view()
