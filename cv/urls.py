from django.urls import path
from cv.views import *

urlpatterns = [
    path('', Profile_View.as_view(), name="cv_page"),
]
