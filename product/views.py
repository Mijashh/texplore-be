from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Cart, CartItem, Category, Product
from .serializers import (
    CartCreateSerializer,
    CartDetailSerializer,
    CartItemCreateSerializer,
    CartItemSerializer,
    CategorySerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action == "list":
            return ProductListSerializer
        return ProductCreateSerializer

    def create(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_class = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = CategorySerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Cart.objects.all().prefetch_related("cart_items")
    serializer_class = CartCreateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CartDetailSerializer
        return self.serializer_class

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Cart.objects.filter(user=request.user).first()
        serializer = CartDetailSerializer(queryset)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return CartItemSerializer
        return self.serializer_class

    def create(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart_data = {"user": request.user.id}
            cart_serializer = CartCreateSerializer(data=cart_data)
            cart_serializer.is_valid(raise_exception=True)
            cart = cart_serializer.save()
        serializer.is_valid(raise_exception=True)
        if CartItem.objects.filter(
            cart=cart, product=serializer.validated_data["product"]
        ).exists():
            cart_item = CartItem.objects.filter(
                cart=cart, product=serializer.validated_data["product"]
            ).first()
            cart_item.quantity += serializer.validated_data["quantity"]
            cart_item.save()
            cart.calculate_total()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.save(cart=cart)
            cart.calculate_total()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        cart_item = CartItem.objects.filter(id=pk).first()
        if cart_item.cart.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        cart_item.cart.calculate_total()
        return Response(CartDetailSerializer(cart_item.cart).data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cart.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        cart = Cart.objects.filter(user=request.user).first()
        cart.calculate_total()
        if serializer.instance.quantity == 0:
            serializer.instance.delete()
        elif serializer.instance.quantity < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(CartDetailSerializer(cart).data)
