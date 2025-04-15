from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete'), ('restore', 'Restore'), ('login', 'Login'), ('logout', 'Logout'), ('password_change', 'Password Change'), ('password_reset', 'Password Reset')], max_length=20, verbose_name='action')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('details', models.TextField(blank=True, verbose_name='details')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'activity log',
                'verbose_name_plural': 'activity logs',
                'ordering': ['-created_at'],
            },
        ),
    ]
