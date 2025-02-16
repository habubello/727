from django.urls import path

from shop import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category-detail/<int:category_id>/', views.ProductDetailView.as_view(), name='products_of_category'),
    path('order-detail/<int:pk>/save/', views.ProductDetailView.as_view(), name='order_detail'),
    path('create-product/', views.ProductCreateView.as_view(), name='product_create'),
    path('delete-product/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('edit-product/<int:product_id>/', views.ProductUpdateView.as_view(), name='edit_product'),
]