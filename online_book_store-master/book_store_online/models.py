from django.db import  models

class Customer(models.Model):
    user_id = models.CharField(max_length = 10, primary_key = True)
    email = models.EmailField()
    password = models.CharField()
    first_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 50)

class Book_store(models.Model):
    store_id = models.CharField(max_length = 10, primary_key = True)
    store_name = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField()
    website = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 10)
    rating = models.IntegerField()
    address_line1 = models.CharField(max_length = 100)
    address_line2 = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50)
    district = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip_code = models.CharField(max_length = 6)


class Customer_address(models.Model):
    user_id = models.ForeignKey(Customer, 
        on_delete= models.CASCADE
    )
    address_id = models.AutoField(primary_key = True)
    address_no = models.IntegerField()
    address_line1 = models.CharField(max_length = 100)
    address_line2 = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50)
    district = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip_code = models.CharField(max_length = 6)


class Book(models.Model):
    book_id = models.CharField(max_length = 10, primary_key = True)
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    publisher = models.CharField(max_length = 50)
    genre = models.CharField(max_length = 20)
    year_of_publish = models.IntegerField()
    price = models.IntegerField()
    copies_sold = models.IntegerField()
    rating = models.IntegerField()

class Order(models.Model):
    STATUS_CHOICES= (
        ('D', 'Delivered'),
        ('P', 'Processing'),
        ('C', 'Cancelled'),
    )
    order_id = models.CharField(max_length = 10,primary_key = True)
    user_id = models.ForeignKey(Customer,
    on_delete = CASCADE
    )
    store_id  = models.ForeignKey(Book_store,
    on_delete = SET_NULL
    )
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES)
    date_of_order = models.DateTimeField(auto_now = True)
    expected_delivery_date = models.DateField(null = True)
    deliverd_date = models.DateField(null = True)
    total_price = models.FloatField()

class Complaint_record(models.Model):
    order_id = models.ForeignKey(
        Order,
        on_delete = CASCADE,
    )
    complain_no = models.AutoField(primary_key = True)
    description= models.CharField(max_length = 200)

class Cart(models.Model):
    user_id = models.ForeignKey(
        Customer, 
        on_delete = CASCADE,
    )
    book_id = models.ForeignKey(
        Book, 
        on_delete = CASCADE
    )
    cart_id = models.AutoField(primary_key = True)
    date_of_entry = models.DateField()

class To_read_list(models.Model):
    user_id = models.ForeignKey(
        Customer,
        on_delete = CASCADE
    )
    book_id = models.ForeignKey(
        Book, 
        on_delete= CASCADE
    )
    read_list_id = models.AutoField(primary_key = True)

class Review( models.Model):
    user_id = models.ForeignKey(
        Customer,
        on_delete = CASCADE
    )
    book_id = models.ForeignKey(
        Book, 
        on_delete= CASCADE
    )
    description = models.CharField(max_length = 200)
    review_id = models.AutoField(primary_key = True)

class Book_ordered(models.Model):
    book_id = models.ForeignKey(
        Book, 
        on_delete= CASCADE
    )
    order_id = models.ForeignKey(
        Order,
        on_delete = CASCADE,
    )
    Book_ordered_id = models.AutoField(primary_key = True)

class user_list(models.Model):
    user_id = models.ForeignKey(
        Customer,
        on_delete = CASCADE
    )
    store_id = models.ForeignKey(
        Book_store, 
        on_delete = CASCADE
    )
    user_list_entry = models.AutoField(primary_key = True)

class Book_available(models.Model):
    book_id = models.ForeignKey(
        Book, 
        on_delete= CASCADE
    )
    user_id = models.ForeignKey(
        Customer,
        on_delete = CASCADE
    )
    no_of_copies = models.IntegerField()
    book_available_id = models.AutoField()

