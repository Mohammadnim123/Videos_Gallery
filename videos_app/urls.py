from django.urls import path
from .views import CategoryVideosList, CategoryVideoDetail, VideoDetailView

urlpatterns = [
    path('', CategoryVideosList.as_view(), name='category-videos-list'),
    path('category/<int:pk>/', CategoryVideoDetail.as_view(), name='category-detail'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
