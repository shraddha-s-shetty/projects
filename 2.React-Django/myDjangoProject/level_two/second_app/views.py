from django.shortcuts import render
from second_app.models import Webpage,Topic,AccessRecord,Users
from . import forms
from second_app.forms import NewForms
# Create your views here.

def index(request):
    web_page_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records': web_page_list}
    #insert_dict = {"insert_content_1": "Hi I AM A Django APP"}
    return render(request,'second_app/index.html',date_dict)

def users(request):
    form = NewForms()

    if request.method == 'POST':
        form = NewForms(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("ERROR FORM INVALID")

    return render(request,'second_app/users.html',{'form':form})
