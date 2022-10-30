from django.db import  models

class Customer(models.Model):
    user_id         = models.CharField(max_length = 50, primary_key = True)

    email           = models.EmailField()
    password        = models.CharField(max_length = 50)
    first_name      = models.CharField(max_length = 50)
    middle_name     = models.CharField(max_length = 50)
    last_name       = models.CharField(max_length = 50)
    phone_no        = models.CharField(max_length = 50)


    class Meta:
        db_table = "Customer"





class Customer_address(models.Model):
    user_id         = models.ForeignKey(Customer, on_delete= models.CASCADE)
    address_id      = models.AutoField(primary_key = True)

    address_no      = models.IntegerField()
    address_line1   = models.CharField(max_length = 100)
    address_line2   = models.CharField(max_length = 100)
    city            = models.CharField(max_length = 50)
    district        = models.CharField(max_length = 50)
    state           = models.CharField(max_length = 50)
    zip_code        = models.CharField(max_length = 6)
    is_current      = models.BooleanField(default = False)


    class Meta:
        db_table = "Customer_address"




class Book_store(models.Model):
    store_id        = models.AutoField( primary_key = True)

    store_name      = models.CharField(max_length = 100)
    email           = models.EmailField(unique = True)
    password        = models.CharField(max_length = 50)
    website         = models.CharField(max_length = 50)
    phone_no        = models.CharField(max_length = 10)
    rating          = models.IntegerField()
    address_line1   = models.CharField(max_length = 100)
    address_line2   = models.CharField(max_length = 100)
    city            = models.CharField(max_length = 50)
    district        = models.CharField(max_length = 50)
    state           = models.CharField(max_length = 50)
    zip_code        = models.CharField(max_length = 6)


    class Meta:
        db_table = "Book_store"




class Book(models.Model):
    book_id         = models.AutoField(primary_key = True)

    title           = models.CharField(max_length = 50)
    author          = models.CharField(max_length = 50)
    publisher       = models.CharField(max_length = 50)
    genre           = models.CharField(max_length = 20)
    year_of_publish = models.IntegerField()
    copies_sold     = models.IntegerField()
    rating          = models.IntegerField(null = True)


    class Meta:
        db_table = "Book"




class Order(models.Model):
    STATUS_CHOICES  = [('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled')]
    order_id        = models.AutoField(primary_key = True)
    user_id         = models.ForeignKey(Customer, on_delete = models.CASCADE)
    store_id        = models.ForeignKey(Book_store, on_delete = models.CASCADE)

    status                  = models.CharField(max_length = 20, choices = STATUS_CHOICES)
    date_of_order           = models.DateTimeField(null = True, blank= True)
    expected_delivery_date  = models.DateField(null = True, blank = True)
    delivered_date          = models.DateField(null = True, blank = True)
    cancelled_date          = models.DateField(null = True, blank = True)
    cancelled_by            = models.CharField(max_length = 20, null = True, blank = True)
    cancellation_remarks    = models.CharField(max_length = 100, null = True, blank = True)
    total_price             = models.FloatField()
    address_no              = models.IntegerField(default = 0)


    class Meta:
        db_table = "Order"




class Complaint_record(models.Model):
    order_id    = models.ForeignKey(Order, on_delete = models.CASCADE)

    complain_no = models.AutoField(primary_key = True)
    description = models.CharField(max_length = 200)

    class Meta:
        db_table = "Complaint_record"




class Cart(models.Model):
    cart_id         = models.AutoField(primary_key = True)
    user_id         = models.ForeignKey(Customer, on_delete = models.CASCADE)
    book_id         = models.ForeignKey(Book, on_delete = models.CASCADE)
    store_id        = models.ForeignKey(Book_store, on_delete = models.CASCADE)
    
    date_of_entry   = models.DateField(auto_now_add = True)
    no_of_copies    = models.IntegerField(default = 0)
    price           = models.FloatField(default = 0)


    class Meta:
        db_table = "Cart"





class To_read_list(models.Model):
    user_id         = models.ForeignKey(Customer, on_delete = models.CASCADE)
    book_id         = models.ForeignKey(Book, on_delete= models.CASCADE)
    read_list_id    = models.AutoField(primary_key = True)

    class Meta:
        db_table = "To_read_list"




class Review(models.Model):
    user_id         = models.ForeignKey(Customer, on_delete = models.CASCADE)
    book_id         = models.ForeignKey(Book, on_delete= models.CASCADE)
    review_id       = models.AutoField(primary_key = True)

    description     = models.CharField(max_length = 200)
    rating          = models.FloatField(default=0.0)


    class Meta:
        db_table = "Review"





class Book_ordered(models.Model):
    book_id         = models.ForeignKey(Book, on_delete= models.CASCADE)
    order_id        = models.ForeignKey(Order,on_delete = models.CASCADE)
    Book_ordered_id = models.AutoField(primary_key = True)

    no_of_copies    = models.IntegerField(default = 0)


    class Meta:
        db_table = "Book_ordered"





class user_list(models.Model):
    user_id         = models.ForeignKey(Customer, on_delete = models.CASCADE)
    store_email     = models.ForeignKey(Book_store, to_field = 'email', db_column = 'store_email', on_delete = models.CASCADE, null = True)

    user_list_entry = models.AutoField(primary_key = True)


    class Meta:
        db_table = "user_list"





class Book_available(models.Model):
    book_id             = models.ForeignKey(Book, on_delete= models.CASCADE)
    store_email         = models.ForeignKey(Book_store, to_field = 'email', db_column = 'store_email', on_delete = models.CASCADE)

    no_of_copies        = models.IntegerField(default = 0)
    book_available_id   = models.AutoField(primary_key = True)
    price               = models.IntegerField(default = 0)

    class Meta:
        db_table = "Book_available"

