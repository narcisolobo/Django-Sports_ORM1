from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.index, name="index"),
	url(r"^orm2$", views.orm2, name="orm2"),
	url(r"^make_data/", views.make_data, name="make_data"),
]