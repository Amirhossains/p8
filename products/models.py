from django.db import models
# from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    Parent = models.ForeignKey(to='self', blank=True, null=True, verbose_name='parent', on_delete=models.CASCADE)
    Title = models.CharField(max_length=50, verbose_name='title')
    Description = models.TextField(blank=True, verbose_name='description')
    Avatar = models.ImageField(blank=True, upload_to='categories/')
    IsEnable = models.BooleanField(default=False, verbose_name='is enable')
    PublishTime = models.DateField(verbose_name='publish time')
    CreatedTime = models.DateTimeField(auto_now_add=True)
    UpdatedTime = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.Title

class Product(models.Model):
    Title = models.CharField(verbose_name='title', max_length=50)
    Description = models.TextField(verbose_name='description', blank=True)
    Avatar = models.ImageField(verbose_name='poster', upload_to='products/')
    IsEnable = models.BooleanField(verbose_name='is enable', default=False)
    Category = models.ManyToManyField(to='Category', verbose_name='categories', blank=True)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    UpdatedTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.Title

class File(models.Model):
    Title       = models.CharField(verbose_name='title', max_length=50)
    file        = models.FileField(verbose_name='file', upload_to='files/%Y/%m/%d/')
    Product     = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='files')
    IsEnable    = models.BooleanField(verbose_name='is enable', default=True)
    Created     = models.DateTimeField(auto_now_add=True)
    UpdatedTime = models.DateTimeField(auto_now=True)
    FileAudio = 1
    FileVideo = 2
    FileImage = 3
    FileTypes = ((FileAudio, 'audio'), (FileVideo, 'video'), (FileImage, 'image'))
    FileType  = models.PositiveIntegerField('file type', choices=FileTypes, default=2)

    class Meta:
        db_table = 'files'
        verbose_name = 'file'
        verbose_name_plural = 'files'

        def __str__(self):
            return self.Title