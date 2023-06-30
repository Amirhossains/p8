# Generated by Django 4.2.2 on 2023-06-17 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50, verbose_name='title')),
                ('Description', models.TextField(blank=True, verbose_name='description')),
                ('Avatar', models.ImageField(blank=True, upload_to='categories/')),
                ('IsEnable', models.BooleanField(default=False, verbose_name='is enable')),
                ('PublishTime', models.DateField(verbose_name='publish time')),
                ('CreatedTime', models.DateTimeField(auto_now_add=True)),
                ('UpdatedTime', models.DateTimeField(auto_now=True)),
                ('Parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50, verbose_name='title')),
                ('Description', models.TextField(blank=True, verbose_name='description')),
                ('Avatar', models.ImageField(upload_to='products/', verbose_name='poster')),
                ('IsEnable', models.BooleanField(default=False, verbose_name='is enable')),
                ('CreatedTime', models.DateTimeField(auto_now_add=True)),
                ('UpdatedTime', models.DateTimeField(auto_now=True)),
                ('Category', models.ManyToManyField(blank=True, to='products.category', verbose_name='categories')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50, verbose_name='title')),
                ('file', models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='file')),
                ('IsEnable', models.BooleanField(default=True, verbose_name='is enable')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('UpdatedTime', models.DateTimeField(auto_now=True)),
                ('FileType', models.PositiveIntegerField(choices=[(1, 'audio'), (2, 'video'), (3, 'image')], default=2, verbose_name='file type')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='products.product')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'db_table': 'files',
            },
        ),
    ]
