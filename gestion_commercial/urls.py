from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = ([
    path('admin/', admin.site.urls),
    re_path(r'^', include(('base.urls', 'base'), namespace="base")),
    re_path(r'^', include(('stock.urls', 'stock'), namespace="stock")),
    re_path(r'^', include(('client.urls', 'client'), namespace="client")),
    re_path(r'^', include(('dashboard.urls', 'dashboard'), namespace="dashboard")),
    re_path(r'^', include(('produit.urls', 'produit'), namespace="produit")),
    re_path(r'^', include(('venteAchats.urls', 'venteAchats'), namespace="venteAchats")),
    re_path(r'^', include(('commande.urls', 'commande'), namespace="commandes")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
if settings.DEBUG:  # Assurez-vous que les URL de debug toolbar ne sont chargées qu'en mode développement
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
