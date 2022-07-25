# Generated by Django 4.0.6 on 2022-07-25 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0003_alter_rawprediction_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prediction',
            options={'ordering': ('-datetime', '-created_at'), 'verbose_name': 'прогноз', 'verbose_name_plural': 'прогнозы'},
        ),
        migrations.AddField(
            model_name='prediction',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата и время'),
        ),
    ]