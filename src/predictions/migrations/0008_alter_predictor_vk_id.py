# Generated by Django 4.0.6 on 2022-07-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0007_alter_predictor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictor',
            name='vk_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='VK ID'),
        ),
    ]
