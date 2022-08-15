# Generated by Django 4.1 on 2022-08-15 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Enter the letter that you want displayed', max_length=1, verbose_name='Key')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
        ),
        migrations.AlterModelOptions(
            name='wordle',
            options={'get_latest_by': 'pub_date', 'ordering': ['pub_date', 'title'], 'verbose_name': 'Wordle', 'verbose_name_plural': 'Wordles'},
        ),
        migrations.AlterField(
            model_name='word',
            name='wordle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='words.wordle', verbose_name='Wordle'),
        ),
        migrations.AlterField(
            model_name='wordle',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wordles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wordle',
            name='no_of_words',
            field=models.PositiveIntegerField(default=1, help_text='Number of words to be attempted for this game.', verbose_name='Max Words'),
        ),
    ]