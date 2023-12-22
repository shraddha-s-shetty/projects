from django.shortcuts import render
from django.http import HttpResponse

def app_homepage(request):
    my_dict = {'insert_me' : 'Hi I am from views.py of the app'}
    return render(request,'groceries_app\index.html',context=my_dict)

def help(request):
    help_dict = {'help_insert': "HELP PAGE"}
    return render(request,'groceries_app\help.html',context=help_dict)
# Create your views here.
