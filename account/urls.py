from django.urls import path

from account.views import RegisterView, LoginView

app_name = 'auth'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
