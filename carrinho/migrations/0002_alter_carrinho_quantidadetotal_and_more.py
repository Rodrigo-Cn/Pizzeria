# Generated by Django 5.0.4 on 2024-05-31 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='quantidadeTotal',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='carrinho',
            name='valorTotal',
            field=models.FloatField(default=None),
        ),
    ]
