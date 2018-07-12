from flask_admin.model import BaseModelView


#
# mine_blocks_form = MineBlocksForm(request.form)
# if request.method == 'POST' and mine_blocks_form.validate():
#     num_blocks_to_mine = mine_blocks_form.num_blocks.data
#     message, category = bitcoin.generate(num_blocks_to_mine=num_blocks_to_mine)
#     flash(message=message, category=category)
from wtforms import Form

from app.bitcoind_client.bitcoind_client import BitcoinClient


class BlocksModelView(BaseModelView):
    bitcoin = BitcoinClient()

    def get_pk_value(self, model):
        pass

    def scaffold_list_columns(self):
        return []

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
        return self.bitcoin.get_block_count(), self.bitcoin.get_most_recent_blocks()

    def get_one(self, id):
        pass

    def create_model(self, form):
        pass

    def update_model(self, form, model):
        pass

    def delete_model(self, model):
        pass
