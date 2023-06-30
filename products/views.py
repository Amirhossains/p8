from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, File
from .serializers import CategorySerializer, ProductSerializer, FileSerializer

class ProductsListView(APIView):

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDetailView(APIView):

    def found(self, pk):
        try:
            p = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
        return p

    def get(self, request, pk):
        product = self.found(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    # def post(self, request):
class CategoryListView(APIView):

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryDetailView(APIView):

    def found(self, pk):
        try:
            c = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
        return c

    def get(self, request, pk):
        category = self.found(pk)
        serializer = CategorySerializer(category, context={'request':request})
        return Response(serializer.data)

class FileListVeiw(APIView):

    def get(self, request, product_id):
        file = File.objects.filter(Product_id=product_id)
        serializer = FileSerializer(file, many=True, context={'request':request})
        return Response(serializer.data)

class FileDetailView(APIView):
    def get(self, request, product_id, pk):
        try:
            file = File.objects.get(pk=pk, Product_id=product_id)
        except File.DoesNotExist:
            raise Http404
        serializer = FileSerializer(file, context={'request':request})
        return Response(serializer.data)