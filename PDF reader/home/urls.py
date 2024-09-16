from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("<str:name>", views.index, name = "index"),
    path('create_album/', views.create_album, name='create_album'),
    path('album_list/', views.album_list, name='album_list'),
    path('album_detail/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album_detail/<int:album_id>/<int:page_number>/', views.page, name='page'),
    path('upload_image/<int:album_id>/', views.upload_image, name='upload_image'),
    path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)