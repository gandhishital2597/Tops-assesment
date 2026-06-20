from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Public display name for the profile.', max_length=50, unique=True)),
                ('age', models.IntegerField(help_text="User's age in years. Must be 13 or older (see UserProfileForm.clean_age).")),
                ('is_public', models.BooleanField(default=True, help_text='If True, the profile is visible to everyone; if False, it is private.')),
                ('bio', models.TextField(blank=True, help_text='Optional short bio shown on the profile page.', max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
