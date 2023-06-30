from rest_framework import serializers

from .models import Category, Product, File

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'Title', 'Description', 'Avatar', 'IsEnable', 'CreatedTime', 'url')

class FileSerializer(serializers.ModelSerializer):
    FileType = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'Title', 'file', 'FileType')

    def get_FileType(self, obj):
        return obj.get_FileType_display()

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    Category = CategorySerializer(many=True)
    files = FileSerializer(many=True)
    mixing = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'Title', 'Description', 'Avatar', 'Category', 'files', 'mixing', 'url')

    def get_mixing(self, obj):
        return '{}-{} have got {} cetegory.'.format(obj.id, obj.Title, obj.Category.count())



