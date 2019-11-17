# Generated by Django 2.2.6 on 2019-11-13 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('image', models.FileField(blank=True, null=True, upload_to='media/images/')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('description', models.TextField(blank=True, default='', max_length=100, null=True)),
                ('category', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('category2', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='food.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
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
