# Generated by Django 3.2.8 on 2021-10-27 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('passcode', models.CharField(blank=True, max_length=15, null=True)),
                ('person_passcodes_required', models.BooleanField(blank=True, default=False)),
                ('use_dates', models.BooleanField(blank=True, default=False)),
                ('use_categories', models.BooleanField(blank=True, default=False)),
                ('use_pictures', models.BooleanField(blank=True, default=False)),
                ('use_descriptions', models.BooleanField(blank=True, default=False)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('currency', models.CharField(default='usd', max_length=7)),
                ('url_hash', models.CharField(max_length=6, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('payment_algorithm', models.CharField(default='reg', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('passcode', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user_login', models.CharField(blank=True, max_length=30, null=True)),
                ('header_color', models.CharField(max_length=6)),
                ('finalized', models.BooleanField(default=False)),
                ('group_ID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='splitter.group')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('person_ID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='splitter.person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='administrator_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='splitter.person'),
        ),
    ]
