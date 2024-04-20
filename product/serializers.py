from rest_framework import serializers

from .models import Cart, CartItem, Category, Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "image", "description", "rating"]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CartItemCreateSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), required=False
    )

    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), required=False
    )
    product = serializers.ReadOnlyField(source="product.id")
    product_title = serializers.ReadOnlyField(source="product.title")
    image = serializers.ReadOnlyField(source="product.image")
    price = serializers.ReadOnlyField(source="product.price")

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product",
            "product_title",
            "quantity",
            "image",
            "price",
        ]



class CartDetailSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        cart_items = instance.cart_items.all().order_by("id")
        cart_items_data = CartItemSerializer(cart_items, many=True).data

        representation = super().to_representation(instance)
        representation["cart_items"] = cart_items_data
        return representation

    class Meta:
        model = Cart
        fields = ["total", "cart_items"]
