# Generated by Django 3.2.5 on 2021-08-09 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films_app', '0006_film_id_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='id_user',
        ),
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='movie/%Y/%m/%d/', verbose_name='Видео'),
        ),
        migrations.AlterField(
            model_name='film',
            name='video_poster',
            field=models.ImageField(blank=True, null=True, upload_to='poster/%Y/%m/%d/', verbose_name='Постер'),
        ),
        migrations.CreateModel(
            name='Film_to_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films_app.film')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Фильм пользователя',
                'verbose_name_plural': 'Фильмы пользователя',
                'ordering': ['id_film'],
            },
        ),
        migrations.AddField(
            model_name='film',
            name='id_user',
            field=models.ManyToManyField(through='films_app.Film_to_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
