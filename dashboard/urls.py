from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

	path('',views.dashboard_setup, name = "dashboard-setup"),
	path('render/<str:slug>/',views.dashboard_render, name = "dashboard-render"),
	path('compute/',views.dashboard_compute_pred, name = "dashboard-compute-pred"),

]