from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from src.apps.products.models import (
    ProductCategory,
    ProductInventory,
    Product,
    ProductReview,
)


class ProductCategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductInventoryInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(initial=0, allow_null=True)


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField(default=0, allow_null=True)
    weight = serializers.FloatField(default=0, allow_null=True, required=False)
    short_description = serializers.CharField(required=False)
    long_description = serializers.CharField(required=False)

    category = ProductCategoryInputSerializer(many=False)
    inventory = ProductInventoryInputSerializer(many=False, required=True)


class ProductCategoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name",)
        read_only_fields = fields


class ProductInventoryOutputSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ProductInventory
        fields = ("quantity", "sold", "updated")
        read_only_fields = fields


class ProductListOutputSerializer(serializers.ModelSerializer):
    inventory = ProductInventoryOutputSerializer(many=False, read_only=True)
    category = ProductCategoryOutputSerializer(many=False, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk"
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "inventory",
            "category",
            "endpoint",
            "url",
        )
        read_only_fields = fields


class ProductDetailOutputSerializer(serializers.ModelSerializer):
    inventory = ProductInventoryOutputSerializer(many=False, read_only=True)
    category = ProductCategoryOutputSerializer(many=False, read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "short_description",
            "long_description",
            "price",
            "weight",
            "inventory",
            "category",
            "created",
            "updated",
        )
        read_only_fields = fields


class ProductCategoryListOutputSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ProductCategory
        fields = ("id", "name", "created", "updated")
        read_only_fields = fields


class ProductReviewInputSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.FloatField(
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )


class ProductReviewOutputSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            "id",
            "username",
            "product_name",
            "description",
            "rating",
            "created",
            "updated",
        )
        read_only_fields = fields
