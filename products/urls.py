from django.urls import path

from .views import ProductsListView, CategoryListView, FileListVeiw
from .views import ProductDetailView, CategoryDetailView, FileDetailView

urlpatterns = [
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('category-list/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('list/', ProductsListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/files/', FileListVeiw.as_view(), name='product-files-list'),
    path('<int:product_id>/files/<int:pk>/', FileDetailView.as_view(), name='product-files-detail'),

]