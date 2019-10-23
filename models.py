# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
<<<<<<< HEAD
=======
        managed = True
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'auth_user'


class CartTable(models.Model):
    customer_id = models.CharField(db_column='Customer_Id', primary_key=True, max_length=15)  # Field name made lowercase.
    user = models.ForeignKey('self', models.DO_NOTHING, db_column='User_Id')  # Field name made lowercase.
    item = models.CharField(db_column='Item', max_length=50)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'cart_table'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InventoryTable(models.Model):
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    item = models.CharField(db_column='Item', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200)  # Field name made lowercase.
    inventory_id = models.CharField(db_column='Inventory_Id', primary_key=True, max_length=255)  # Field name made lowercase.

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'inventory_table'


class OrderitemsTable(models.Model):
    items_id = models.CharField(db_column='Items_Id', primary_key=True, max_length=11)  # Field name made lowercase.
    orders = models.ForeignKey('self', models.DO_NOTHING, db_column='Orders_Id')  # Field name made lowercase.
    item = models.CharField(db_column='Item', max_length=50)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'orderitems_table'


class OrdersTable(models.Model):
    orders_id = models.CharField(db_column='Orders_Id', primary_key=True, max_length=11)  # Field name made lowercase.
    users = models.ForeignKey('self', models.DO_NOTHING, db_column='Users_Id')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    total_price = models.IntegerField(db_column='Total_Price')  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=10)  # Field name made lowercase.

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'orders_table'


class UsersTable(models.Model):
    user_id = models.CharField(db_column='User_Id', primary_key=True, max_length=11)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=15)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=15)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_Name', max_length=15)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=15)  # Field name made lowercase.
    shipping_add = models.CharField(db_column='Shipping_Add', max_length=30)  # Field name made lowercase.

    class Meta:
<<<<<<< HEAD
=======
        managed = False
>>>>>>> da6bad7f30113f8e7cfac5c2dd5b9af9fdc24e08
        db_table = 'users_table'
