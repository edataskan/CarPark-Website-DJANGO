from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, activate

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name= "signup"),
    path('signin', views.signin, name= "signin"),
    path('signout', views.signout, name= "signout"),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'authentication/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'authentication/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/', include('django.contrib.auth.urls')),
    path('signin/', auth_views.LoginView.as_view(template_name = 'authentication/signin.html'), name='signin'),
    path('authentication/login/', auth_views.LoginView.as_view(template_name='authentication/signin.html'), name='login'),
    path('signin/', CustomLoginView.as_view(template_name = 'authentication/signin.html'), name='signin'),
    #path('change-password/', auth_views.PasswordChangeView.as_view(template_name='authentication/change_password.html'), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/change_password_done.html'), name='password_change_done'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='authentication/password_change_form.html'), name='password_change'),
    path('send-login-notification/', views.send_login_notification, name='send_login_notification'),
    path('activate/<str:email>/', activate, name='activate'),  # Bu URL, kullanıcının e-posta üzerinden tıkladığında çalışacak

]
