# Generated by Django 5.0.4 on 2024-04-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productproxy',
            options={},
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Бренд'),
        ),
    ]
