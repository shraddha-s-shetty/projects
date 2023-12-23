from django.shortcuts import render
from second_app.models import Webpage,Topic,AccessRecord,Users
from . import forms
# Create your views here.

def index(request):
    web_page_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records': web_page_list}
    #insert_dict = {"insert_content_1": "Hi I AM A Django APP"}
    return render(request,'second_app/index.html',date_dict)

def users(request):
    users_list = Users.objects.order_by('first_name')
    user_list = {'user_input':users_list}
    return render(request,'second_app/users.html',user_list)

def form_name(request):
    form = forms.FormName()
    if request.method == "POST":
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("Validation success!")
            print("Name: ",form.cleaned_data['name'])
            print("Email: ",form.cleaned_data['email'])
            print("Text: ",form.cleaned_data['text'])
    return render(request,'second_app/forms_page.html',{'form':form})
