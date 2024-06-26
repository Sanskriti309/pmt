# Generated by Django 5.0.1 on 2024-02-08 17:38

import ckeditor.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('duration', models.CharField(choices=[('3m', '3 months'), ('6m', '6 months'), ('9m', '9 months'), ('12m', '12 months')], max_length=4)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('fee', models.IntegerField(default=None)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('father_name', models.CharField(max_length=255)),
                ('mother_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=6)),
                ('contact_no', models.CharField(max_length=10)),
                ('whatsapp_no', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('discounted_fee', models.IntegerField(blank=True, default=None, null=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('enquiry_date', models.DateField(default=None)),
                ('coming_date', models.DateField(blank=True, default=None, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('course_interested', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enquiries', to='students.course')),
            ],
        ),
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_fee', models.IntegerField()),
                ('student_photo', models.FileField(blank=True, null=True, upload_to='upload/students_photos/')),
                ('qualification_docs', models.FileField(blank=True, null=True, upload_to='upload/qualification_docs/')),
                ('address_doc_type', models.CharField(choices=[('aadhaar', 'Aadhaar Card'), ('voter', 'Voter ID Card'), ('others', 'Others')], default='aadhaar', max_length=32)),
                ('address_docs', models.FileField(blank=True, null=True, upload_to='upload/address_docs/')),
                ('admission_date', models.DateField(default=None)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('enquiry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admission', to='students.enquiry')),
            ],
        ),
        migrations.CreateModel(
            name='FeeManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fee_paid_date', models.DateField(default=django.utils.timezone.now)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_entries', to='students.admission')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
