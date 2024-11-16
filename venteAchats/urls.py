from django.urls import path
from . import views
from .views import get_prices
urlpatterns = [

    # ---------------------- create -------------------#
    path('vente/create', views.vente_create, name='Size_vente'),
    # ---------------------- liste -------------------#
    path('liste/vente/client', views.ListeVenteClient.as_view(), name='List_vente_client'),

    # ---------------------- detail -------------------#
    path('Vente_client/detail/<int:pk>/', views.DetailVenteCLient.as_view(), name='vente_client_detail'),
    # ---------------------- autre -------------------#
    path('get-prices/<int:client_id>/', get_prices, name='get_prices'),


]
