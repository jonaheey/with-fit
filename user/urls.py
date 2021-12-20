from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.signup),
    # path('signin', views.signin, name='signin'),
    # path('signout', views.signout, name='signout')
    path('signin', views.signin),
    path('signout', views.signout)
]