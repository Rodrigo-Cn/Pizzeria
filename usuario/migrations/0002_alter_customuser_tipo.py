# Generated by Django 5.0.4 on 2024-05-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo',
            field=models.CharField(choices=[('A', 'Administrador'), ('B', 'Usuário')], default='A', max_length=1),
        ),
    ]
