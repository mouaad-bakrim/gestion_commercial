from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect


@login_required(login_url='/login/')
def Dashboard(request):

    return render(request, 'dashboard.html')

# Create your views here.
@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')