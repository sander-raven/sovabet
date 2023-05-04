# Generated by Django 4.0.6 on 2022-07-20 18:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('info', models.TextField(blank=True, verbose_name='информация')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='начало')),
            ],
            options={
                'verbose_name': 'игра',
                'verbose_name_plural': 'игры',
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('total_points', models.FloatField(default=0.0, verbose_name='сумма баллов')),
                ('winners', models.IntegerField(default=0, verbose_name='угадано победителей')),
                ('runners_up', models.IntegerField(default=0, verbose_name='угадано вторых призёров')),
                ('third_places', models.IntegerField(default=0, verbose_name='угадано третьих призёров')),
                ('prize_winners', models.IntegerField(default=0, verbose_name='угадано попаданий в призёры')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='predictions.game', verbose_name='игра')),
            ],
            options={
                'verbose_name': 'прогноз',
                'verbose_name_plural': 'прогнозы',
            },
        ),
        migrations.CreateModel(
            name='Predictor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('info', models.TextField(blank=True, verbose_name='информация')),
                ('name', models.CharField(max_length=50, verbose_name='имя')),
                ('vk_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='VK ID')),
            ],
            options={
                'verbose_name': 'прогнозист',
                'verbose_name_plural': 'прогнозисты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('info', models.TextField(blank=True, verbose_name='информация')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='начало')),
            ],
            options={
                'verbose_name': 'сезон',
                'verbose_name_plural': 'сезоны',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('info', models.TextField(blank=True, verbose_name='информация')),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('info', models.TextField(blank=True, verbose_name='информация')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='начало')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tournaments', to='predictions.season', verbose_name='сезон')),
            ],
            options={
                'verbose_name': 'турнир',
                'verbose_name_plural': 'турниры',
            },
        ),
        migrations.CreateModel(
            name='PredictionEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('result', models.IntegerField(choices=[(1, 'Победитель'), (2, 'Второй призёр'), (3, 'Третий призёр')], verbose_name='результат')),
                ('points', models.FloatField(default=0.0, verbose_name='баллы')),
                ('prediction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_events', to='predictions.prediction', verbose_name='прогноз')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prediction_events', to='predictions.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'событие прогноза',
                'verbose_name_plural': 'события прогноза',
            },
        ),
        migrations.AddField(
            model_name='prediction',
            name='predictor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='predictions.predictor', verbose_name='прогнозист'),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменение')),
                ('is_active', models.BooleanField(default=True, verbose_name='актив?')),
                ('result', models.IntegerField(blank=True, choices=[(1, 'Победитель'), (2, 'Второй призёр'), (3, 'Третий призёр')], null=True, verbose_name='результат')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='predictions.game', verbose_name='игра')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='predictions.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'выступление',
                'verbose_name_plural': 'выступления',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='teams',
            field=models.ManyToManyField(related_name='games', through='predictions.Performance', to='predictions.team', verbose_name='команды'),
        ),
        migrations.AddField(
            model_name='game',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games', to='predictions.tournament', verbose_name='турнир'),
        ),
    ]