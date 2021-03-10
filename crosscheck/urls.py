from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from crosscheckapi.views import register_user, login_user
from crosscheckapi.views import Tenants

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tenants', Tenants, 'tenant')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
