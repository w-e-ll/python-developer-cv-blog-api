from django.urls import path
from .views import ContactView, thankyou

urlpatterns = [
    path('', ContactView.as_view(), name='contacts'),
    path('thankyou/', thankyou, name='thankyou'),
]
