import django_tables2 as tables
from .models import Client

class ClientListTable(tables.Table):
    nom = tables.TemplateColumn(
        '<a href="">{{ record.nom }}</a>',
        verbose_name="Nom"
    )

    formatted_phone = tables.Column(
        verbose_name="Téléphone",
        accessor="formatted_phone"
    )



    category = tables.TemplateColumn(
        template_code='''
            {% if record.category.type == "passage" %}
                <span class="badge badge-primary fw-bolder w-60 fs-8">{{ record.category.name }}</span>
            {% elif record.category.type == "compte" %}
                <span class="badge badge-danger fw-bolder w-60 fs-8">{{ record.category.name }}</span>
            {% else %}
                <span class="badge badge-secondary fw-bolder w-60 fs-8">Unknown</span>
            {% endif %}
        ''',
        verbose_name="Catégorie"
    )

    class Meta:
        model = Client
        fields = ("nom", "adresse", "ville", "formatted_phone", "patente", "external_id", "ice", "category", "site")
        attrs = {
            "class": "table table-bordered table-striped table-hover text-gray-600 table-heading table-datatable dataTable g-3 fs-7"
        }
        per_page = 100
        template_name = 'django_tables2/bootstrap.html'
