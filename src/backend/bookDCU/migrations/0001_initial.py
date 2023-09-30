# Generated by Django 4.1.5 on 2023-02-23 20:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('campus', models.CharField(choices=[('GLA', 'Glasnevin Campus'), ('SPD', 'St Pats Campus'), ('AHC', 'All Hallows Campus')], default='GLA', max_length=4)),
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('building', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rows', models.IntegerField()),
                ('seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seat_number', models.IntegerField()),
                ('booked_dates', models.TextField(default='')),
                ('book_time', models.DateTimeField(auto_now_add=True)),
                ('occupant_first_name', models.CharField(max_length=200)),
                ('occupant_last_name', models.CharField(max_length=200)),
                ('occupant_email', models.EmailField(max_length=200)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookDCU.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='booked_seats',
            field=models.ManyToManyField(blank='True', to='bookDCU.seat'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_booked', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(default='')),
                ('start_time', models.DateTimeField(default='2023-02-20 14:30:00')),
                ('end_time', models.DateTimeField(default='2023-02-20 16:30:00')),
                ('seat_number', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('basket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookDCU.basket')),
                ('room_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookDCU.room')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(default='')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('seat_number', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('basket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookDCU.basket')),
                ('room_id', models.ForeignKey(default='L1.29', on_delete=django.db.models.deletion.CASCADE, to='bookDCU.room')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]