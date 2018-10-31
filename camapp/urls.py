from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('me/', views.me, name='me'),
    path('me/<uuid:pk>', views.CameraDetailView.as_view(), name='camera-detail'),
    path('me/create/', views.CameraCreate.as_view(), name='camera_create'),
    path('me/<uuid:pk>/update/', views.CameraUpdate.as_view(), name='camera_update'),
    path('me/<uuid:pk>/delete/', views.CameraDelete.as_view(), name='camera_delete'),
    path('me/<uuid:pk>/frame/', views.frame_view, name='camera_frame'),
    path('me/api/reset/', views.api_key, name='api_reset'),
]