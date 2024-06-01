# Generated by Django 5.0.4 on 2024-05-31 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizza',
            old_name='precoG',
            new_name='preco',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='precoM',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='precoP',
        ),
        migrations.AddField(
            model_name='pizza',
            name='tamanho',
            field=models.CharField(default='Grande', max_length=100),
            preserve_default=False,
        ),
    ]