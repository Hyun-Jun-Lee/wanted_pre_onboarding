# Generated by Django 4.0.3 on 2022-04-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_rename_funding_amount_product_onetime_funding_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='생성일'),
        ),
    ]
