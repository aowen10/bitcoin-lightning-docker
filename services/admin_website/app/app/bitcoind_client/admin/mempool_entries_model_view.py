from flask import flash
from flask_admin.model import BaseModelView
from wtforms import Form

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.bitcoind_client.models.blocks import Blocks
from app.bitcoind_client.models.mempool_entries import MempoolEntries


class MempoolEntriesModelView(BaseModelView):
    bitcoin = BitcoinClient()
    can_view_details = True
    can_create = False

    def get_pk_value(self, model):
        return model.wtxid

    def scaffold_list_columns(self):
        return ['hash', 'confirmations', 'strippedsize', 'size', 'weight',
                'height', 'version', 'versionHex', 'merkleroot', 'tx', 'time',
                'mediantime', 'nonce', 'bits', 'difficulty', 'chainwork', 'nTx',
                'previousblockhash']

    def scaffold_sortable_columns(self):
        pass

    def scaffold_form(self):
        class NewForm(Form):
            pass
        return NewForm

    def scaffold_list_form(self, widget=None, validators=None):
        pass

    def get_list(self, page, sort_field, sort_desc, search, filters,
                 page_size=None):
        mempool_entries = self.bitcoin.get_raw_mempool()
        mempool_entries = [MempoolEntries(**me) for me in mempool_entries]
        return len(mempool_entries), mempool_entries

    def get_one(self, txid):
        mempool_entry = self.bitcoin.get_mempool_entry(txid=txid)
        return MempoolEntries(**mempool_entry)

    def create_model(self, form):
        num_blocks_to_mine = form.num_blocks.data
        message, category = self.bitcoin.generate(num_blocks_to_mine)
        flash(message=message, category=category)
        return Blocks()

    def update_model(self, form, model):
        pass

    def delete_model(self, model):
        pass
