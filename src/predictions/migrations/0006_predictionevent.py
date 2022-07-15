# Generated by Django 4.0.6 on 2022-07-12 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0005_prediction'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('points', models.FloatField(default=0.0, verbose_name='баллы')),
                ('prediction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_events', to='predictions.prediction', verbose_name='прогноз')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='predictions.result', verbose_name='результат')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prediction_events', to='predictions.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'событие прогноза',
                'verbose_name_plural': 'события прогноза',
            },
        ),
    ]