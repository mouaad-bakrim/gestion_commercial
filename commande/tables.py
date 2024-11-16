import django_tables2 as tables
from .models import BonLivraisonClinet, FactureClient


class BonLivresionClientListTable(tables.Table):


    client = tables.Column(
        accessor='client',
        verbose_name='Client',
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center"},
            "tf": {"class": "text-end fw-bolder text-nowrap"},

        }
    )
    selection = tables.CheckBoxColumn(
        accessor='pk',
        attrs={
            "th__input": {"id": "toggleCB", "class": "form-check-input"},
            'td__input': {'class': 'checkbox_local form-check-input'},
        },
        orderable=False
    )

    date_livraison = tables.TemplateColumn(
        template_code="""
                <a href="{% url 'commande:bon_livresion_detail' record.pk %}">
                   {{ record.date_livraison|date:"d-m-Y" }}
               </a>
               """,
        verbose_name='Date',
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center"},
            "tf": {"class": "text-end fw-bolder text-nowrap"},
        },
    )
    quantite = tables.Column(verbose_name="Quantité", attrs={"td": {"data-field": "quantite"}})
    montant = tables.Column(
        verbose_name="Montant",
        attrs={"td": {"data-field": "montant"}}
    )
    class Meta:
        model = BonLivraisonClinet
        fields = ("selection",'date_livraison','client', 'bon_livraison')
        attrs = {
            "class": "table table-bordered table-striped table-hover text-gray-600 table-heading table-datatable dataTable g-3 fs-7"
        }
        per_page = 100
        template_name = 'django_tables2/bootstrap.html'



class FactureClientListTable(tables.Table):
    advancement = tables.TemplateColumn("""
           <div class="progress">
               <div class="progress-bar bg-primary"
                    role="progressbar" aria-valuenow="{{ record.get_avancement|floatformat:0 }}" 
                    aria-valuemin="0" aria-valuemax="100" 
                    style="width:{{ record.get_avancement|floatformat:0 }}%;">
                   {{ record.get_avancement|floatformat:0 }}%
               </div>
           </div>
       """,
                                        attrs={"td": {"class": "align-middle"}},
                                        orderable=True, verbose_name="Avancement de Paiement")
    numero = tables.TemplateColumn(
        '<a href="">{{ record.numero }}</a>',
        verbose_name="Numéro de Facture"
    )
    date = tables.DateColumn(
        format='d/m/Y',
        verbose_name="Date",
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center "},
            "tf": {"class": "text-end fw-bolder text-nowrap"},
        }
    )
    bons_livraison = tables.Column(
        verbose_name="Nombre de BL",
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center"},
            "tf": {"class": "text-end fw-bolder text-nowrap"},
        }
    )
    Imprimer = tables.TemplateColumn(
        template_code=('{% load static %}'
           '<a href="{% url "commande:printInvoive" record.pk %}">'
            '<img alt="PDF" class="w-30px me-3" src="{% static "assets/media/svg/files/pdf.svg" %}" />'
            '</a>'
        ),
        verbose_name="Imprimer",
        orderable=False,
        attrs={
            "td": {"class": "text-center"}
        }
    )

    class Meta:
        model = FactureClient
        fields = ("numero", "date", "client", "montant_ht","montant_tva","montant_ttc", "total_quantity", "bons_livraison","advancement", "Imprimer")
        attrs = {
            "class": "table table-bordered table-striped table-hover text-gray-600 table-heading table-datatable dataTable g-3 fs-7"
        }
        per_page = 100

    def render_bons_livraison(self, value, record):
        return record.nombre_bons_livraison()

