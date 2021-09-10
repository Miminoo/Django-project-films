# Generated by Django 3.2.5 on 2021-08-05 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=300, verbose_name='Имя')),
                ('birthday_date', models.DateField(blank=True, verbose_name='Дата рождения')),
            ],
            options={
                'verbose_name': 'Актер',
                'verbose_name_plural': 'Актеры',
                'ordering': ['fullName'],
            },
        ),
        migrations.CreateModel(
            name='Film_to_actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films_app.actor')),
                ('id_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films_app.film')),
            ],
            options={
                'verbose_name': 'Актёр фильма',
                'verbose_name_plural': 'Актёры фильма',
                'ordering': ['id_film'],
            },
        ),
        migrations.AddField(
            model_name='actor',
            name='id_filma',
            field=models.ManyToManyField(through='films_app.Film_to_actor', to='films_app.Film'),
        ),
    ]