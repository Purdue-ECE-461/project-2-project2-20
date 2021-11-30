from django.urls import path
from packages import views

urlpatterns = [
    path('packages/', views.PackageList.as_view()),
    path('package/<int:pk>/', views.PackageByID.as_view()),
    path('package/', views.CreatePackage.as_view()),
    path('package/<int:pk>/rate', views.rate_package),
    path('package/byName/<str:name>/', views.PackageByName.as_view()),
    path('reset/', views.reset_registry),
    
    # user URLs
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view())
    # end user URLs
]