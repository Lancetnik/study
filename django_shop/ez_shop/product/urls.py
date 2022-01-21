from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve'})),
    path('create/', views.ProductViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/', views.ProductViewSet.as_view({'put': 'update'})),
    path('del/<int:pk>/', views.ProductViewSet.as_view({'delete': 'destroy'})),

    path('category/', views.ListProductCategory.as_view()),
    path('category/<int:pk>/', views.GetProductCategory.as_view()),
    path('category/create/', views.CreateProductCategory.as_view()),
    path('category/update/<int:pk>/', views.UpdateProductCategory.as_view()),
    path('category/del/<int:pk>/', views.DestroyProductCategory.as_view()),

    path('busket/', views.ListProductInBusket.as_view()),
    path('busket/<int:pk>/', views.GetProductInBusket.as_view()),
    path('busket/create/', views.CreateProductInBusket.as_view()),
    path('busket/update/<int:pk>/', views.UpdateProductInBusket.as_view()),
    path('busket/del/<int:pk>/', views.DestroyProductInBusket.as_view()),
]
