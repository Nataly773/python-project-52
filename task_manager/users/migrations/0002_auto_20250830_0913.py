from django.db import migrations

def create_custom_group_and_permission(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    MyModel = apps.get_model('users', 'User')  # замени на реальную модель

    group, _ = Group.objects.get_or_create(name="MyGroup")

    ct = ContentType.objects.get_for_model(MyModel)
    perm, _ = Permission.objects.get_or_create(
        codename="my_custom_perm",
        content_type=ct,
        defaults={"name": "My custom permission"},
    )

    group.permissions.add(perm)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),  # замени на последнюю миграцию твоего приложения
        ('auth', '0012_alter_user_first_name_max_length'),  # зависимость на auth
    ]

    operations = [
        migrations.RunPython(create_custom_group_and_permission),
    ]
