from django.urls import path
from . import views 
from .views import SimilarityCheckView

urlpatterns = [
    path('', views.home, name='home'),  
    path('upload/', views.UploadImageView.as_view(), name='upload_image'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('login', views.login, name='login'), 
    path('register', views.register, name='register'), 
    path('check-similarity/', SimilarityCheckView.as_view(), name='check_similarity'),

    #path('test-logged-in/', views.TestLoggedIn.as_view(), name='login'),
    
]

