"""
URL configuration for ChengHuei_Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from googlemap_reviews.views import views_web,views_api

urlpatterns = [
    path('admin/', admin.site.urls),
    # web
    path('googlemap_reviews/',views_web.googlemap_reviews),
    # Api
    path('api/get_shop_keywords',views_api.get_shop_keywords),
    path('api/reviews_data',views_api.reviews_data),
    path('api/get_storelist',views_api.get_storelist),
    path('api/statistic_card',views_api.statistic_card),
    path('api/statistic_footer',views_api.statistic_footer),
]
