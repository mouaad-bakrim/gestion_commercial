from base.utils import PagedFilteredTableView
from client.filters import ClientListFilter
from client.forms import ClientListFormHelper
from .models import Client
from .tables import ClientListTable


class ListClient(PagedFilteredTableView):
    permission_required = 'client.view_client'
    model = Client
    table_class = ClientListTable
    formhelper_class = ClientListFormHelper
    filter_class = ClientListFilter
    template_name = 'client/liste_client.html'
    active_item = 'client_list'
    active_menu = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if user.is_superuser:
            return queryset

        # Filtrer les clients en fonction des sites de l'utilisateur
        if hasattr(user, 'profile') and user.profile.sites.exists():
            # Utiliser un filtre avec __in pour filtrer les sites associés
            sites = user.profile.sites.all()  # Obtenir tous les sites associés
            queryset = queryset.filter(site__in=sites)  # Filtrer par les sites associés
        else:
            queryset = queryset.none()

        # Optimiser le queryset avec only
        queryset = queryset.only('nom', 'ville', 'patente', 'phone', 'adresse',
                                 'external_id', 'email', 'site', 'category', 'ice')

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Récupérer le site de l'utilisateur à partir de son profil
        # Récupérer les sites associés à l'utilisateur
        if hasattr(user, 'profile') and user.profile.sites.exists():
            user_sites = user.profile.sites.all()  # Obtenir tous les sites associés
        else:
            user_sites = None

        context.update({
            'user_sites': user_sites,
            'active_item': 'client_list',
            'active_menu': 'clients',
        })

        table = self.get_table()
        table.exclude = ['selection', ]
        context['table'] = table

        return context
