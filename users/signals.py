from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    roles = ["Employer", "Hunter", "Admin"]
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)

        if role == "Admin":
            all_permissions = Permission.objects.all()
            group.permissions.set(all_permissions)
            group.save()

    print("Default groups created successfully.")


