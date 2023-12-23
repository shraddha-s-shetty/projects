from django.shortcuts import render
from second_app.models import Webpage,Topic,AccessRecord

# Create your views here.

def index(request):
    web_page_list = AccessRecord.objects.order_by('date')
    insert_dict = {"insert_content_1": "Hi I AM A Django APP"}
    return render(request,'second_app/index.html',insert_dict)