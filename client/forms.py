from client.models import Client
from crispy_forms.helper import FormHelper


class ClientListFormHelper(FormHelper):
    model = Client
    form_tag = False
    form_class = 'd-flex flex-column flex-md-row gap-5'
    field_class = 'flex-row-fluid mae-filter-form'
    help_text_inline = True
    form_show_labels = False