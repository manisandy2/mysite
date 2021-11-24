from django.urls import path
from .views import *
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
urlpatterns = [
    path('',home_page,name='Home_page'),
    path('reg/', registration,name='registration'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('reg_api/', registration_api,name='registration_api'),
    path('login_api/',login_api,name='login_api'),
    path('logout_api/',logout_api,name='logout_api'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('user_list/',user_list,name='user_list'),

]

