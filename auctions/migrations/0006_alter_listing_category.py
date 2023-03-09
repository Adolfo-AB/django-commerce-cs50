# Generated by Django 3.2.7 on 2021-10-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20211003_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('HO', 'Home'), ('EL', 'Electronics'), ('FA', 'Fashion'), ('TO', 'Toys'), ('OT', 'Other')], default='OT', max_length=2),
        ),
    ]