from django.urls import path
from . import views

urlpatterns = [

    # ---------------------- create -------------------#

    # ---------------------- liste -------------------#
    path('client/list', views.ListClient.as_view(), name='list_client'),

    # ---------------------- detail -------------------#

    # ---------------------- autre -------------------#

]
