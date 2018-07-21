from wtforms import Form

from app.formatters.common import satoshi_formatter
from app.formatters.lnd import path_formatter
from app.lnd_client.admin.lnd_model_view import LNDModelView
from app.lnd_client.grpc_generated.rpc_pb2 import SendRequest


class PaymentsModelView(LNDModelView):
    can_create = True
    create_form_class = SendRequest
    get_query = 'get_payments'
    primary_key = 'payment_hash'

    column_formatters = {
        'path': path_formatter,
        'value': satoshi_formatter,
        'fee': satoshi_formatter,
    }

    def scaffold_form(self):
        form_class = super(PaymentsModelView, self).scaffold_form()
        return form_class

    def create_model(self, form: Form):
        data = form.data
        data = {k: v for k, v in data.items() if data[k]}

        response = self.ln.send_payment_sync(**data)
        if response is False:
            return False

        decoded_pay_req = self.ln.decode_payment_request(pay_req=data['payment_request'])
        payments = self.ln.get_payments()
        new_payment = [p for p in payments
                       if p.payment_hash == decoded_pay_req.payment_hash ]
        return new_payment[0]
