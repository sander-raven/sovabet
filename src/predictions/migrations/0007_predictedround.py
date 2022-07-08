# Generated by Django 4.0.6 on 2022-07-08 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0006_event_created_at_event_modified_at_round_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictedRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.FloatField(default=0.0, verbose_name='сумма баллов')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='изменён')),
                ('predictor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predicted_rounds', to='predictions.predictor', verbose_name='прогнозист')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predicted_rounds', to='predictions.round', verbose_name='раунд')),
            ],
            options={
                'verbose_name': 'прогнозируемый раунд',
                'verbose_name_plural': 'прогнозируемые раунды',
            },
        ),
    ]
