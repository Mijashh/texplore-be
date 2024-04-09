from rest_framework import viewsets
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    permission_class=[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
# Create your views here.