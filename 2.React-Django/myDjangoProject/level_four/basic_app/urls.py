#from django.conf.urls import urls
from basic_app import views
from django.urls import path,re_path,include

#TEMPLATE TAGGING
app_name = 'basic_app'

urlpatterns=[
    re_path(r'^relative/$',views.relative,name='relative'),
    re_path(r'^other/$',views.other,name='other')
]