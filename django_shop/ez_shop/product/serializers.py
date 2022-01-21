from rest_framework import serializers

from . import models


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = '__all__'


class ProductImgSerailizer(serializers.ModelSerializer):
    file = serializers.ImageField()

    class Meta:
        model = models.ProductImg
        fields = ['file']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImgSerailizer(read_only=True, many=True)

    def create(self, validated_data):
        product = super().create(validated_data)
        for category in product.category.all():
            models.save_product_to_category(product, category)
        return product

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductInBusketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductInBusket
        fields = '__all__'
