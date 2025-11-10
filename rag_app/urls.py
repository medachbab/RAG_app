from django.urls import path
from . import views

urlpatterns = [
    path("query/", views.rag_query, name="rag_query"),
    path("upload/", views.UploadAndIndexView.as_view(), name="upload_index"),
]