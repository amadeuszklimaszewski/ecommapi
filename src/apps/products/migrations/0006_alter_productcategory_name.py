# Generated by Django 4.0 on 2022-04-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_productcategory_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]