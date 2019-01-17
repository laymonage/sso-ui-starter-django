from django.urls import path
import django_cas_ng.views

app_name = 'sso_ui'
urlpatterns = [
    path('login/', django_cas_ng.views.LoginView.as_view(), name='login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='logout'),
]
