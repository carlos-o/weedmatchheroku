"""weedmatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from accounts import views as accounts_views
from payment import  views as payment_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'payment/card', payment_views.CreditCardViewSet)
router.register(r'profile', accounts_views.ProfileViewSet)
router.register(r'public-image', accounts_views.PublicProfileImagesViewSet)

urlpatterns = [
    re_path(r'^jet/', include('jet.urls', 'jet')),
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('countrys/', accounts_views.CountryView.as_view()),
    path('terms-conditions/', accounts_views.TermsConditionsView.as_view()),
    path('register/', accounts_views.RegisterView.as_view()),
    path('forgot-password/', accounts_views.RequestRecoverPassword.as_view()),
    path('recover-password/', accounts_views.RecoverPassword.as_view()),
    path('login/', accounts_views.LoginView.as_view()),
    path('login-facebook/', accounts_views.LoginFacebookView.as_view()),
    path('login-instagram/', accounts_views.LoginInstagramView.as_view()),
    path('logout/', accounts_views.LogoutView.as_view()),
    path('public-profile/<int:pk>/', accounts_views.PublicProfileView.as_view()),
    path('public-feed/', accounts_views.PublicFeedView.as_view()),
    path('', include(router.urls)),
]
from django.conf.urls.static import static, serve
from weedmatch import settings

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
