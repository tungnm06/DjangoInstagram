# Generated by Django 2.0.7 on 2018-08-05 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('followings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='cusdetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cusdetail', to='customers.Customer'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='customers.Customer'),
        ),
    ]