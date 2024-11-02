import django_tables2 as tables
from .models import Vente



class VenteCLientListTable(tables.Table):



    client = tables.Column(
        accessor='client',
        verbose_name='Client',
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center"},
            "tf": {"class": "text-end fw-bolder text-nowrap"},

        }
    )
#        '<a href="{% url "user_management:detail_employer" record.id %}">{{ record.get_nom_display}}</a>',

    date_vente = tables.TemplateColumn(
        template_code="""
                <a href="{% url 'venteAchats:vente_client_detail' record.pk %}">
                   {{ record.date_vente|date:"d-m-Y" }}
               </a>
               """,
        verbose_name='Date',
        attrs={
            "th": {"class": "text-center"},
            "td": {"class": "text-center"},
            "tf": {"class": "text-end fw-bolder text-nowrap"},
        },
    )


    class Meta:
        model = Vente
        fields = ('date_vente','client', 'total')
        attrs = {
            "class": "table table-bordered table-striped table-hover text-gray-600 table-heading table-datatable dataTable g-3 fs-7"
        }
        per_page = 100
        template_name = 'django_tables2/bootstrap.html'
