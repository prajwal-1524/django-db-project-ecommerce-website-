from django.contrib import admin
from django.urls import path
from userapp import views  # Import views from userapp to handle requests

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.user_login,name='login'),  # URL 
    path('logout/', views.user_logout,name='logout'),  
]