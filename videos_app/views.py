from rest_framework import generics
from rest_framework.response import Response
from .models import Category, Video
from .serializers import CategorySerializer, ExtendedVideoSerializer
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from rest_framework.authentication import TokenAuthentication


class CategoryVideosList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        videos_with_row = Video.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                order_by=F('updated_at').desc(),
                partition_by=F('category_id')
            )
        )

        limited_videos = videos_with_row.filter(row_number__lte=5)
        return Category.objects.prefetch_related(
            Prefetch("videos", queryset=limited_videos.prefetch_related("users_watched"))
        )


class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Video
        fields = ['title']


class CustomPagination(PageNumberPagination):
    page_size = 5


class CategoryVideoDetail(generics.ListAPIView):
    serializer_class = ExtendedVideoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VideoFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Video.objects.filter(category_id=category_id).select_related('category').prefetch_related('users_watched')


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.select_related('category')
    serializer_class = ExtendedVideoSerializer

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        user = request.user

        if not user.is_anonymous and not video.watched(user):
            video.users_watched.add(user)
            video.save()

        ip_address = self.get_client_ip(request)
        cache_key = f"video_{video.id}_viewed_by_{ip_address}"

        if not cache.get(cache_key):
            video.views_number += 1
            video.save()
            cache.set(cache_key, 1, 86400)

        serializer = self.get_serializer(video)
        return Response(serializer.data)

    def get_client_ip(self, request):
        #This in case we use AWS
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            #This for localhost
            ip = request.META.get('REMOTE_ADDR')
        return ip