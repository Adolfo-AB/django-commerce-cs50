# Generated by Django 3.2.7 on 2021-10-07 06:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_current_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='author',
            new_name='seller',
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AddConstraint(
            model_name='listing',
            constraint=models.CheckConstraint(check=models.Q(('starting_price', 0.0)), name='Valid starting price.'),
        ),
        migrations.AddConstraint(
            model_name='listing',
            constraint=models.CheckConstraint(check=models.Q(('current_price', 0.0)), name='Valid current price.'),
        ),
    ]