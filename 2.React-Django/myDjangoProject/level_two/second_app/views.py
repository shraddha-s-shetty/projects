from django.shortcuts import render
from second_app.models import Webpage,Topic,AccessRecord

# Create your views here.

def index(request):
    insert_dict = {"insert_content_1": "Hi I AM A Django APP"}
    return render(request,'second_app/index.html',insert_dict)