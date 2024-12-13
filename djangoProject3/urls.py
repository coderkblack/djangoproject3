"""
URL configuration for djangoProject3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from homify import views

urlpatterns = [
    path('', views.home, name='home'),
    path('houses', views.houses, name='houses'),
    path('onsale/houses', views.houses_on_sale, name='houses_onsale'),
    path('sold/houses', views.purchased_houses, name='purchased'),
    path('fines', views.interest_accrued, name='fines'),
    path('purchase/<int:id>', views.purchase_house, name='purchase'),
    path('refund/<int:id>', views.refund, name='refund'),
    path('pay/<int:id>', views.pay_overdue, name='pay_overdue'),
    path('handle/response/transactions', views.callbacks, name='callbacks'),
    path('admin/', admin.site.urls),
]
