# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='category name', max_length=200, unique=True, verbose_name='name')),
                ('desc', models.TextField(help_text='category description', verbose_name='description')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'ordering': ['name'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, help_text="order's description", verbose_name='description')),
                ('status', models.PositiveIntegerField(choices=[(0, 'preparation'), (1, 'sent'), (2, 'received')], default=0, help_text="order's status", verbose_name='status')),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Customer', verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Order',
                'ordering': ['-modified', '-created'],
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='product name', max_length=200, verbose_name='name')),
                ('price', models.FloatField(db_index=True, help_text="product's price", verbose_name='price')),
                ('image', models.ImageField(help_text="product's image", upload_to='images/', verbose_name='image')),
                ('desc', models.TextField(help_text="product's description", verbose_name='description')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(help_text="product's category", on_delete=django.db.models.deletion.CASCADE, to='sales.Category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Product',
                'ordering': ['name'],
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1, verbose_name='number')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'ProductSet',
                'ordering': ['id'],
                'verbose_name_plural': 'ProductSets',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, through='sales.ProductSet', to='sales.Product', verbose_name='Product'),
        ),
    ]
