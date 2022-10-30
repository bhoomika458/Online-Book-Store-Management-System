from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from . forms import *
from django.views import  generic

def index(request):
    try:
        if request.session['user_id']:
            return redirect('profile')
    finally: 
        return render(request = request, template_name = 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newUser = Customer()
            newUser.user_id = form.cleaned_data.get('user_id')
            newUser.email = form.cleaned_data.get('email')
            newUser.password = form.cleaned_data.get('password')
            newUser.first_name = form.cleaned_data.get('first_name')
            newUser.middle_name = form.cleaned_data.get('middle_name')
            newUser.last_name = form.cleaned_data.get('last_name')
            newUser.phone_no = form.cleaned_data.get('phone_no')
            newUser.save()

            #username = form.cleaned_data.get('user_id')
            #raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            #messages.info(request, "Welcome to KGP")
            return redirect('index')
        else:
            messages.error(request, "Invalid Form Details")
            form = SignupForm()
            return render(request, 'users/sign_up.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'users/sign_up.html', {'form': form})

def login(request):
    if request.method == "POST":
        print(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            #print(form);
            #return redirect('index');
            username = form.cleaned_data.get('user_id')
            raw_password = form.cleaned_data.get('password')
            user = Customer.objects.filter(user_id = username, password = raw_password)
            if user:
                messages.info(request, f"You are now logged in as {username}")
                user_id = request.POST['user_id']
                request.session['user_id'] = user_id
                return redirect('profile')
            else:
                messeags.error(request, "Invalid Username or Password")
        else:
            messages.error(request, "Invalid USERNAME or PASSWORD")
    form = LoginForm()
    return render(request, "users/login.html", context= {"form":form})

def userProfile(request):
    if request.session.has_key('user_id'):
        posts = request.session['user_id']
        query = Customer.objects.filter(user_id = posts)
        return render(request, 'users/profile.html', {"query":query})
    else:
        redirect(request,'home.html', {} )

def userLogout(request):
    try:
        del request.session['user_id']
    except :
        pass
    return redirect( 'index')
#All starting with user contains user_id in the request to help us identify different users


#Returns books added by the particular user
def userCart(request, book_id = None):
    if request.session['user_id']:
        user_id = request.session['user_id']
        if 'store_id' in request.GET:
            print(request.GET['store_id'])
            thisBookStore = Book_store.objects.get(store_id = request.GET['store_id'])
            newCart = Cart()
            newCart.user_id = Customer.objects.get(user_id = user_id)
            newCart.book_id = Book.objects.get(book_id = book_id)
            newCart.store_id = thisBookStore
            newCart.price = Book_available.objects.get(store_email = thisBookStore.email, book_id = book_id).price
            #newCart.price = request.GET['store'].price
            newCart.no_of_copies = request.GET['no_of_copies']
            newCart.save()
        books_in_cart = Cart.objects.filter(user_id = user_id)
        total_price = 0
        num_order = 0
        seller_list = []
        for book in books_in_cart:
                total_price += book.price*book.no_of_copies
        return render(request, 'users/userCart.html', {'books_in_cart' : books_in_cart, 'total_price' : total_price})
    else:
        messages.warning(request, 'You are not logged in. Please log in to continue')
        redirect('index')    
    return HttpResponse("Cart Page for user")

def userConfirmAddress(request):
    if request.session['user_id']:
        user_id = request.session['user_id']
        addresses= Customer_address.objects.filter(user_id = user_id)
        primary_address = ''
        other_address = []
        for address in addresses:
            if(address.is_current):
                primary_address = address
            else:
                other_address.append(address)
        obj  = {
            'primary_address': primary_address,
            'other_address': other_address
        }
        return render(request, 'users/confirmAddress.html', obj)
    else:
        messages.warning(request, "You are not logged in. Please log in")
        return redirect('index')
        
def userAddAsPrimaryAddress(request, address_id):
    if request.session['user_id']:
        user_id = request.session['user_id']
        print(address_id)
        all_address = Customer_address.objects.filter(user_id = user_id)
        for address in all_address:
            address.is_current = False
            address.save()
        p_address = Customer_address.objects.get(address_id = address_id)
        p_address.is_current = True
        p_address.save()
        messages.success(request, 'Address Set As Primary')
        return redirect('confirmAddress')
    else:
        messages.error(request, "Please Log In First")
        return redirect('index')


def userPlaceOrder(request, address_no):
    if request.session['user_id']:
        user_id = request.session['user_id']
        all_orders = Cart.objects.filter(user_id = user_id)
        store_list = []
        price_list = []
        book_store_ind = []
        count = 0
        for books in all_orders:
            if books.store_id in store_list:
                price_list[store_list.index(books.store_id)] += books.price*(books.no_of_copies)
                
            else:
                store_list.append(books.store_id)
                price_list.append(books.price)
            
            book_store_ind.append(store_list.index(books.store_id))
            count += 1
        
        order_id= [] 
        for i in range(0,len(store_list)):
            newOrder = Order()
            print("The order Id is ", newOrder.order_id)
            newOrder.user_id = Customer.objects.get(user_id = user_id)
            newOrder.store_id = store_list[i]
            newOrder.total_price = price_list[i]
            newOrder.address_no = address_no
            newOrder.status = 'Processing'
            newOrder.save()
            print("This ID: ", newOrder.order_id)
            order_id.append(newOrder.order_id)

        count =0
        for book in all_orders:
            newBook = Book_ordered()
            print("New Book Book_ordered_id:", newBook.Book_ordered_id)
            newBook.book_id = book.book_id
            newBook.store_id = book.store_id
            newBook.order_id = Order.objects.get(order_id = order_id[book_store_ind[count]])
            newBook.no_of_copies = book.no_of_copies
            newBook.save()
            print("New Book Book_ordered_id:", newBook.Book_ordered_id)
            count +=1
        
        Cart.objects.filter(user_id = user_id ).delete()
        messages.success(request, 'Order Placed Successfully')
        return redirect('profile')
    else:
        messages.error(request, 'Please Log In First')
        return redirect('index')

#Returns all the order made by the user
def userOrders(request):
    return HttpResponse("Orders by the user")

def userOrderComplain(request):
    return HttpResponse("Return Complain correspoding to this user and a given order")

def userBookReveiw(request):
    return HttpResponse("Helps in reviewing a book by user")


#To display the To Read List of the user
def userBookList(request):
    if request.session['user_id'] :
        user_id = request.session['user_id']
        if request.method == 'POST':
            return redirect('index')
        BookObjectList = To_read_list.objects.filter(user_id= user_id)
        book_list= []
        for book in BookObjectList:
            book_object = Book.objects.filter(book_id = book.book_id.book_id)
            for book_fin in book_object:
                book_list.append({'title':book_fin.title, 'author': book_fin.author, 'book_id':book_fin.book_id})
        return render(request, 'users/book_list.html', {'book_list':book_list})
    else:
        messages.warning(request,'You are logged in. Please Log in')
        return redirect('index')

#To remove Book from user's read list
def userRemoveBook(request, book_id):
    if request.session['user_id'] :
        user_id = request.session['user_id']
        if request.method == 'POST':
            return redirect('profile')
        To_read_list.objects.filter(book_id = book_id, user_id = user_id).delete()
    else:
        messages.warning(request,'You are logged in. Please Log in')
        return redirect('index')

def userAddAddress(request):
    if request.session['user_id']:
        user_id = request.session['user_id']
        if request.method == "POST":
            form = userAddressForm(request.POST)
            count_add = Customer_address.objects.filter(user_id = user_id)
            add_num = 0
            for add in count_add:
                add_num += 1
            if form.is_valid():
                print(form)
                address = Customer_address()
                address.user_id = Customer.objects.get(user_id =user_id)
                address.address_line1 = form.cleaned_data.get('address_line1')
                address.address_line2 = form.cleaned_data.get('address_line2')
                address.city = form.cleaned_data.get('city')
                address.district = form.cleaned_data.get('district')
                address.state = form.cleaned_data.get('state')
                address.zip_code = form.cleaned_data.get('zip_code')
                address.address_no = add_num +1
                address.save()
                messages.success(request, "Address saved successfully")
                return redirect('profile')
        else:
            form = userAddressForm()
            print(form)
            return render(request, 'users/addAddress.html', {'form': form})
    else:
        messages.error(request,"Please Login First!")
        return redirect('index')


def viewBook(request, book_id):
    print(book_id)
    sellers= Book_available.objects.filter(book_id = book_id)

    book = Book.objects.get(book_id = book_id)
    return render(request, 'users/viewBook.html', {'book': book, 'sellers': sellers})


def searchBooks(request):
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        filter = request.GET['filter']
        if(filter == 'title'):
            books = Book.objects.filter( title__contains=search_term )
        if(filter == 'genre'):
            books = Book.objects.filter( genre__contains=search_term )
        if(filter == 'publisher'):
            books = Book.objects.filter( publisher__contains=search_term ) 
        if(filter == 'author'):
            books = Book.objects.filter( author__contains=search_term )
    # books = Book.objects.all()
    print(books)
    return render(request, 'users/searchResult.html', {'books' : books, 'search_term': search_term, 'filter': filter })
#Store Owner

def storeSignUp(request):
    if request.method == "POST":
        form = StoreSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            userCount = Book_store.objects.filter(email = email).count()
            if userCount == 0:
                form.save()
                username = form.cleaned_data.get('store_name')
                messages.info(request, f"You have now signed up as {username}")
                return redirect('index')
            else:
                messages.error(request, 'Email Address already exists')
        else:
            messages.error(request, "Invalid Fomr")
    else:
        form = StoreSignUp()
    return render(request, 'store/storeSignUp.html', {"form":form})


def storeLogin(request):
    if request.method == "POST":
        print("request received", request)
        form = storeLoginForm(request.POST)
        if form.is_valid():
            print("form received ", form);
            #return redirect('index');
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            userCount = Book_store.objects.filter(email = email, password = raw_password).count()
            #user = Book_store.objects.filter(email = email, password = raw_password)
            if userCount == 1:
                #print(user)
                messages.info(request, f"You are now logged in with Email Id: {email}")
                #curr_store = Book_store.objects.filter(email = email, password = raw_password).first()
                request.session['email'] = request.POST['email']
                return redirect('storeProfile')
            else:
                print("Invalid Form")
                messages.error(request, "Invalid Email or Password")
        else:
            print("Invalid Form Input")
            messages.error(request, "Invalid Email or PASSWORD")
    form = storeLoginForm()
    return render(request, "store/storeLogin.html", context= {"form":form})

def storeProfile(request):
    if request.session.has_key('email'):
        posts = request.session['email']
        query = Book_store.objects.filter(email = posts)
        return render(request, 'store/storeProfile.html', {"query":query})
    else:
        redirect(request,'store/storeProfile.html', {} )

def storeLogout(request):
    try:
        del request.session['email']
    except :
        pass
    return redirect( 'index')

def storeBookAdd(request):
    if request.method == "POST":
        form = bookAddForm(request.POST)
        if form.is_valid():
            newUser = Book()
            newUser.title = form.cleaned_data.get('title')
            newUser.author = form.cleaned_data.get('author')
            newUser.publisher = form.cleaned_data.get('publisher')
            newUser.genre = form.cleaned_data.get('genre')
            newUser.year_of_publish = form.cleaned_data.get('year_of_publish')
            num_copies = form.cleaned_data.get('no_of_books')
            this_book_count = Book.objects.filter(title = newUser.title, author = newUser.author).count()
            if this_book_count == 0:
                newUser.copies_sold = 0
                newUser.save()
                bookAndStore = Book_available()
                bookAndStore.store_email = Book_store.objects.filter(email = request.session['email']).first()
                bookAndStore.book_id = newUser
                bookAndStore.no_of_copies = num_copies
                bookAndStore.price = form.cleaned_data.get('price')
                bookAndStore.save()
            else:
                book_id = Book.objects.filter(title = newUser.title, author= newUser.author)[0].book_id
                store_email = Book_store.objects.filter(email = request.session['email']).first()
                myBook = Book_available.objects.filter(book_id = book_id, store_email = store_email).count()
                if myBook is 0:
                    myBook = Book_available()
                    myBook.book_id = Book.objects.get(title = newUser.title, author = newUser.author)
                    myBook.store_email = store_email
                else:
                    myBook = Book_available.objects.get(book_id = book_id, store_email = store_email)
                myBook.no_of_copies = myBook.no_of_copies + num_copies
                myBook.save()
        else:
            messages.error(request, "Invalid Book Data Entered")
    else:
        addBookForm = bookAddForm()
        return render(request, 'store/addBook.html',{"form":addBookForm})
    
    if request.session.has_key('email'):
        posts = request.session['email']
        query = Book_store.objects.filter(email = posts)
        return render(request, 'store/storeProfile.html', {"query":query})
    else:
        messages.error(request, "Please Log In First")
        return redirect('index')     

def storeBookDel(request):
    return HttpResponse("Helps in removing books for store book list")

def storeBookView(request):
    return HttpResponse("Return all the books correspoding to the store")

def storeUpdateBook(request):
    return HttpResponse("Page for updating information corresponding to a book")

def storeOrderList(request):
    return HttpResponse("Return Order List for the book")

#Extract data from order schema and returns books according to status 
def storeSalesList(request):
    return HttpResponse("Return Sales List")

#Uses user_id and store_id 

def storeUserList(request):
    return HttpResponse("Returns the user who bought books from this store")


#Independent of Store and User
def trendingList(request):
    return HttpResponse("Returns the best selling books top 10 ")

