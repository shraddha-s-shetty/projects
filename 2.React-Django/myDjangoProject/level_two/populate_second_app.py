import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','level_two.settings')

import django
django.setup()

#####FAKE SCRIPT

import random
from second_app.models import Webpage,Topic,AccessRecord,Users
from faker import Faker

fakegen = Faker()
topics = ["Search","Social","MArketplace","News","Games"]

def add_topic():
    t = Topic.objects.get_or_create(top_name = random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):

    for entry in range(N):

        # top = add_topic()

        # name = fakegen.company()
        # date = fakegen.date()
        # url = fakegen.url()
        # webpg = Webpage.objects.get_or_create(topic=top,name=name,url= url)[0]

        # accessrecord = AccessRecord.objects.get_or_create(name = webpg,date = date)[0]
        firstname = fakegen.first_name()
        lastname = fakegen.last_name()
        email = fakegen.email()

        usr = Users.objects.get_or_create(first_name=firstname,last_name=lastname,email=email)
        
if __name__ == '__main__':
    print("Populating script started!")
    populate(40)
    print("Populating script ended!")