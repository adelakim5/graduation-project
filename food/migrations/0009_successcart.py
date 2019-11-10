# Generated by Django 2.2.6 on 2019-11-10 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('food', '0008_auto_20191111_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.PositiveIntegerField(default=0)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receiver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('sender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.Food')),
            ],
        ),
    ]
