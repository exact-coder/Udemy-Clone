# Generated by Django 4.1.7 on 2023-03-04 06:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Course Title')),
                ('description', models.TextField(verbose_name='Course Description')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('language', models.CharField(max_length=50, verbose_name='Language')),
                ('image_url', models.ImageField(upload_to='course_images', verbose_name='Course Image')),
                ('course_uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Course Unique ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Course Price')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title Of Episode')),
                ('file', models.FileField(upload_to='course_vedios', verbose_name='Courses Vedio')),
                ('length', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Vedio Length')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Sector Name')),
                ('sector_uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Sector Unique Id')),
                ('sector_image', models.ImageField(upload_to='sector_image', verbose_name='Sector Image')),
                ('releted_course', models.ManyToManyField(to='courses.course', verbose_name='Releted Courses')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=250, verbose_name='Section Title')),
                ('episodes', models.ManyToManyField(to='courses.episode', verbose_name='Episode')),
            ],
        ),
    ]
