from django.urls import path
from . import views

urlpatterns = [

    # ---------------------- create -------------------#
path('create_facture/', views.CreateFactureView.as_view(), name='create_facture'),
    # ---------------------- liste -------------------#
    path('liste/bon_livresion', views.ListeBonLivraisonClinet.as_view(), name='bon_livresion'),
    path('direct/facture', views.ListFactureView.as_view(), name='factur'),

    # ---------------------- detail -------------------#
    path('bon_livresion/detail/<int:pk>/', views.DetailBonLivresionCLient.as_view(), name='bon_livresion_detail'),
    # ---------------------- autre -------------------#
    path('invoicebonlivraison/<int:pk>/print/', views.invoice_bonlivraison, name='printInvoivebonlivraison'),
    path('invoice/<int:pk>/print/', views.invoice_pdf_view, name='printInvoive'),
    # ---------------------- update -------------------#


]
