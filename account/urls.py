from django.urls import path

from account.views import RegisterView

app_name = 'auth'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
]