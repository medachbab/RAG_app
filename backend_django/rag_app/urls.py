from django.urls import path
from . import views

urlpatterns = [
    path("query/", views.rag_query, name="rag_query"),
    path("upload/", views.UploadAndIndexView.as_view(), name="upload_index"),
    path('index_products/', views.IndexProductsFromPostgresView.as_view(), name='index_products'),
]