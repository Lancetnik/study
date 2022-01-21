from django.shortcuts import render
from rest_framework import generics, viewsets

from . import models, serializers


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()


class CreateProductCategory(generics.CreateAPIView):
    serializer_class = serializers.ProductCategorySerializer


class CreateProductInBusket(generics.CreateAPIView):
    serializer_class = serializers.ProductInBusketSerializer


class ListProductCategory(generics.ListAPIView):
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()


class ListProductInBusket(generics.ListAPIView):
    serializer_class = serializers.ProductInBusketSerializer
    queryset = models.ProductInBusket.objects.all()


class GetProductCategory(generics.RetrieveAPIView):
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()


class GetProductInBusket(generics.ListAPIView):
    serializer_class = serializers.ProductInBusketSerializer
    queryset = models.ProductInBusket.objects.all()

    def get_queryset(self):
        user_id = self.request.parser_context['kwargs']['pk']
        return self.queryset.filter(owner_id=user_id)


class UpdateProductCategory(generics.UpdateAPIView):
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()


class UpdateProductInBusket(generics.UpdateAPIView):
    serializer_class = serializers.ProductInBusketSerializer
    queryset = models.ProductInBusket.objects.all()


class DestroyProductCategory(generics.DestroyAPIView):
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()


class DestroyProductInBusket(generics.DestroyAPIView):
    serializer_class = serializers.ProductInBusketSerializer
    queryset = models.ProductInBusket.objects.all()


def index(request, *args, **kwargs):
    return render(request, 'index.html')



# print([str(i) for i in models.ProductCategory.objects.get(pk=1).products.all()])
# print([str(i) for i in models.ProductCategory.objects.get(pk=2).products.all()])
