from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from suppliers.models import Supplier
from products.models import Product
from customers.models import Customer
from users.models import CustomUser

def setup_groups():
    # Create groups if they don't exist
    user_group, _ = Group.objects.get_or_create(name='User')
    staff_group, _ = Group.objects.get_or_create(name='Staff')
    manager_group, _ = Group.objects.get_or_create(name='Manager')

    # Get content types
    supplier_ct = ContentType.objects.get_for_model(Supplier)
    product_ct = ContentType.objects.get_for_model(Product)
    customer_ct = ContentType.objects.get_for_model(Customer)
    user_ct = ContentType.objects.get_for_model(CustomUser)

    # Get permissions
    supplier_view = Permission.objects.get(content_type=supplier_ct, codename='view_supplier')
    supplier_add = Permission.objects.get(content_type=supplier_ct, codename='add_supplier')
    supplier_change = Permission.objects.get(content_type=supplier_ct, codename='change_supplier')
    supplier_delete = Permission.objects.get(content_type=supplier_ct, codename='delete_supplier')

    product_view = Permission.objects.get(content_type=product_ct, codename='view_product')
    product_add = Permission.objects.get(content_type=product_ct, codename='add_product')
    product_change = Permission.objects.get(content_type=product_ct, codename='change_product')
    product_delete = Permission.objects.get(content_type=product_ct, codename='delete_product')

    customer_view = Permission.objects.get(content_type=customer_ct, codename='view_customer')
    customer_add = Permission.objects.get(content_type=customer_ct, codename='add_customer')
    customer_change = Permission.objects.get(content_type=customer_ct, codename='change_customer')
    customer_delete = Permission.objects.get(content_type=customer_ct, codename='delete_customer')

    # Set up User group permissions (view only)
    user_group.permissions.set([
        supplier_view,
        product_view,
        customer_view,
    ])

    # Set up Staff group permissions (view, add, change)
    staff_group.permissions.set([
        supplier_view, supplier_add, supplier_change,
        product_view, product_add, product_change,
        customer_view, customer_add, customer_change,
    ])

    # Set up Manager group permissions (view, add, change, delete)
    manager_group.permissions.set([
        supplier_view, supplier_add, supplier_change, supplier_delete,
        product_view, product_add, product_change, product_delete,
        customer_view, customer_add, customer_change, customer_delete,
    ])

    print("Groups and permissions set up successfully!")

if __name__ == '__main__':
    setup_groups() 