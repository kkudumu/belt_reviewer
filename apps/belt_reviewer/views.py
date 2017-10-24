from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Author, Review
import re
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    return render(request, "belt_reviewer/index.html")

def register(request):
    logged = False
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    hashedpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    confirm_password = request.POST['confirm_password']
    if(len(first_name)<3):
        logged = True
        messages.error(request, "First Name must be longer than 3 characters", extra_tags="first_name")
    if(len(last_name)<3):
        logged = True
        messages.error(request, "Last Name must be longer than 3 characters", extra_tags="last_name")
    if not EMAIL_REGEX.match(email):
        logged = True
        messages.error(request, "Must be a Valid Email", extra_tags = "email")
    if(len(password) < 8):
        logged = True
        messages.error(request, "Password must be longer than 8 characters", extra_tags ="password")
    if(password != confirm_password):
        logged = True
        messages.error(request, "Your passwords do not match", extra_tags = "confirm_password")
    if logged:
        print "hello"
        return redirect('/')
    else:
        newuser = User.objects.create(first_name=first_name, last_name=last_name, email = email, password = hashedpassword)
        newdict = {"id": newuser.id, "first_name" : newuser.first_name, "last_name": newuser.last_name, "email":newuser.email}
        request.session['user'] = newdict
        return redirect('/bookspage')

def login(request):
    email = request.POST['login_email']
    password = request.POST['login_password']
    user = User.objects.filter(email = email)
    usercheck = user[0]
    print usercheck.password
    if bcrypt.checkpw(password.encode(), usercheck.password.encode()):
        newdict = {"id": usercheck.id,"first_name" :usercheck.first_name, "last_name": usercheck.last_name, "email":usercheck.email}
        request.session['user'] = newdict
        return redirect('/bookspage')
    else:
        return redirect('/')

def bookspage(request):
    books = Book.objects.all().order_by("-id")[:3]
    reviews = Review.objects.all()
    newlist = []

    otherbooks = Book.objects.all()
    for book in otherbooks:
        if len(book.reviews.all()) > 0:
            newlist.append(book)

    context = {
        "books" : books,
        "reviews" : reviews,
        "bookswithreviews" : newlist
    }
    return render(request, "belt_reviewer/books.html", context)

def display_addbook(request):
    authors = Author.objects.all()
    context = {
        "authors" : authors
    }
    return render(request, "belt_reviewer/add.html", context)

def display_book(request, id):
    book = Book.objects.get(id = id)
    reviews = book.reviews.all()

    context = {
        "book" : book,
        "reviews" : reviews
    }
    return render(request, "belt_reviewer/show.html", context)

def process_review(request, id):
    current_user = request.session["user"]
    user = User.objects.get(id=current_user["id"])
    book = Book.objects.get(id = id)
    newreview = Review.objects.create(user = user, book = book)
    newreview.review_des = request.POST["review_description"]
    newreview.review_rating = request.POST["rating"]
    newreview.save()
    return redirect("/book/"+str(id))

def process_addbook(request):
    current_user = request.session["user"]
    user = User.objects.get(id = current_user["id"])
    title = request.POST["book_title"]
    review = request.POST.get("review_description")
    rating = request.POST["rating"]
    if request.POST["new_author"]:
        author = request.POST["new_author"]
    else:
        author = request.POST["author_name"]
    
    if type(author) == int:
        author_add = Author.objects.get(id = author)
    else:
        author_add = Author.objects.create()
        author_add.name = author
        author_add.save()
    newbook = Book.objects.create(title = title, author = author_add)
    newbook.save()
    
    if review != "":
        newreview = Review.objects.create(user = user, book = newbook)
        newreview.review_des = review
        newreview.review_rating = rating
        newreview.save()
    return redirect("/book/"+str(newbook.id))

def display_user(request, id):
    user = User.objects.get(id = id)
    reviews = Review.objects.filter(user = user)
    reviewcount = len(reviews)
    context = {
        "user" : user,
        "reviews" : reviews,
        "reviewcount" : reviewcount
    }
    return render(request, "belt_reviewer/user.html", context)

def remove(request):
    review_id = request.POST["cancel"]
    review_deleted = Review.objects.get(id = review_id)
    review_deleted.delete()
    return redirect("/bookspage")

def logout(request):
    request.session.clear()
    return redirect("/")








