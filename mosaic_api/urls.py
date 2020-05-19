from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('api/mosaic/', views.MosaicListCreate.as_view() ),
    path('api/newmosaic/', views.NewMosaicListCreate.as_view() ),
    path('api/images/', views.ImageViewSet.as_view() ),
]