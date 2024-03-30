from django.urls import path, include
from . import views
from . import consumers
from oauth2_provider.views.base import TokenView

from django.conf.urls import url

urlpatterns = [
    path('userlogin', views.UserLogin.as_view()),
    path('create', views.create, name="create"),
    path('login', views.login, name='login'),
    # path('log', views.log, name='login'),
    path('screate', views.screate, name='screate'),
    path('sacreate', views.sacreate),
    path('get_data', views.get_data),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('contact/', views.contact, name='index'),
    path('verify_captcha/', views.verify_captcha, name='index'),
    path('encrypt', views.encrypt_message, name='index'),
    path('decrypt', views.decrypt_message, name='index'),
    path('ws/', consumers.MyConsumer.as_asgi()),
    path('api/customer_token/', views.CustomTokenView.as_view(), name='token'),
    path('secure-data/', views.secure_data, name='secure_data'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('get-token/', views.obtain_access_token, name='login'),
    path('csv/', views.some_view, name='csv'),
    path('pdf/', views.some_view2, name='pdf'),

]

