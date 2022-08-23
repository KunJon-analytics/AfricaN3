# Generated by Django 4.1 on 2022-08-23 12:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0005_remove_sitting_wordle_sitting_attempts_sitting_word_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitting',
            name='attempts',
            field=models.PositiveIntegerField(default=1, help_text='Number of attempts for this game.', validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(1)], verbose_name='Max Words'),
        ),
        migrations.AlterField(
            model_name='wordle',
            name='reward',
            field=models.FloatField(blank=True, help_text='Total reward to be shared among winners', null=True, verbose_name='Reward'),
        ),
    ]