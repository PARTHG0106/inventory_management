from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def setup_groups():
    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    staff_group, _ = Group.objects.get_or_create(name='Staff')
    user_group, _ = Group.objects.get_or_create(name='User')

    # Get all content types
    content_types = ContentType.objects.all()

    # Get all permissions
    all_permissions = Permission.objects.all()

    # Admin group gets all permissions
    admin_group.permissions.set(all_permissions)

    # Manager group gets all permissions except:
    # - Deleting users
    # - Changing user permissions
    # - Deleting suppliers
    manager_permissions = all_permissions.exclude(
        Q(codename__startswith='delete_') |
        Q(codename__startswith='change_user') |
        Q(codename__startswith='delete_supplier')
    )
    manager_group.permissions.set(manager_permissions)

    # Staff group gets permissions to:
    # - View and add products
    # - View and add categories
    # - View and add suppliers
    # - View and add orders
    staff_permissions = all_permissions.filter(
        Q(codename__startswith='view_') |
        Q(codename__startswith='add_')
    )
    staff_group.permissions.set(staff_permissions)

    # User group gets permissions to:
    # - View products
    # - View categories
    # - View suppliers
    # - View their own profile
    user_permissions = all_permissions.filter(
        Q(codename__startswith='view_') &
        ~Q(codename__startswith='view_user')
    )
    user_group.permissions.set(user_permissions)

    print("Groups and permissions have been set up successfully!")

if __name__ == '__main__':
    setup_groups() 