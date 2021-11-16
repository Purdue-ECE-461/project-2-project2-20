from django.urls import path
from packages import views

urlpatterns = [
    path('packages/', views.package_list),
    path('package/<int:pk>/', views.package_by_id),
    path('reset/', views.reset_registry),
]