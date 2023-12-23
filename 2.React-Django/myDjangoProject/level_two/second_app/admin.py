from django.contrib import admin
from second_app.models import Topic,Webpage,AccessRecord,Users

admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(AccessRecord)
admin.site.register(Users)
# Register your models here.
