from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required


from .models import *


# this is the default view
def index(request):
    if request.method == "POST":
        results = []
        query = request.POST["query"]
        uploads2 = Listing.objects.values('title')
        # add description search also later
        for i in uploads2:
            if query == i:
                results.append(i)
        return render(request, "edunet/searchresults.html", {
            "results": results,
        })

    else:
        return render(request, "edunet/index.html")


# this is the view for login
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # if not authenticated
        else:
            return render(request, "edunet/login.html", {
                "message": "Invalid username and/or password.",
                "msg_type": "danger"
            })
    # if GET request
    else:
        return render(request, "edunet/login.html")


# view for logging out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# view for registering
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "edunet/register.html", {
                "message": "Passwords must match.",
                "msg_type": "danger"
            })
        if not username:
            return render(request, "edunet/register.html", {
                "message": "Please enter your username.",
                "msg_type": "danger"
            })
        if not email:
            return render(request, "edunder/register.html", {
                "message": "Please enter your email.",
                "msg_type": "danger"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "edunet/register.html", {
                "message": "Username already taken.",
                "msg_type": "danger"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # if GET request
    else:
        return render(request, "edunet/register.html")


# view for dashboard
@login_required(login_url='/login')
def dashboard(request, profile):
    lst = Watchlist.objects.filter(user=profile)
    uploads = Listing.objects.filter(seller=profile)
    present = False
    products = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Listing.objects.get(id=item.listingid)
            prodlst.append(product)
    if uploads:
        present = True
    print(prodlst)
    return render(request, "edunet/dashboard.html", {
        "product_list": prodlst,
        "present": present,
        "products": uploads,
        "profile": profile
    })


# view for showing the active lisitngs
@login_required(login_url='/login')
def activelisting(request):
    # list of products available
    products = Listing.objects.all()
    products = products[::1]
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "edunet/activelisting.html", {
        "products": products,
        "empty": empty
    })


# view to create a lisiting
@login_required(login_url='/login')
def createlisting(request):
    # if user submitted the create listing form
    if request.method == "POST":
        # item is of type Listing (object)
        uploaded_file = request.FILES.get("file")
        item = Listing()
        # assigning the data submitted via form to the object
        item.school = request.POST.get("school")
        item.classgroup = request.POST.get("class")
        item.file = uploaded_file
        item.seller = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.starting_bid = request.POST.get('Grade')
        # submitting data of the image link is optional
        if request.POST.get('image_link'):
            item.image_link = request.POST.get('image_link')
        else:
            item.image_link = "https://www.aust-biosearch.com.au/wp-content/themes/titan/images/noimage.gif"
        # saving the data into the database
        item.save()
        # retrieving the new products list after adding and displaying
        products = Listing.objects.all()
        empty = False
        if len(products) == 0:
            empty = True
        return render(request, "edunet/activelisting.html", {
            "products": products,
            "empty": empty
        })
    # if request is get
    else:
        return render(request, "edunet/createlisting.html")


# view to display all the categories
@login_required(login_url='/login')
def categories(request):
    return render(request, "edunet/categories.html")

# view to display individual listing


@login_required(login_url='/login')
def upload(request, title):
    product = Listing.objects.get(id=title)
    added = Watchlist.objects.filter(
        listingid=title, user=request.user.username)
    comments = Comment.objects.filter(listingid=title)
    return render(request, "edunet/upload.html", {
        "product": product,
        "added": added,
        "comments": comments
    })


# View to add or remove products to watchlists
@login_required(login_url='/login')
def addtowatchlist(request, product_id):

    obj = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=product_id)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "edunet/upload.html", {
            "product": product,
            "added": added,
            "comments": comments
        })
    else:
        # if it not present then the user wants to add it to watchlist
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "edunet/upload.html", {
            "product": product,
            "added": added,
            "comments": comments
        })


# view for comments
@login_required(login_url='/login')
def addcomment(request, product_id):
    obj = Comment()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listingid = product_id
    obj.save()
    # returning the updated content
    print("displaying comments")
    comments = Comment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "edunet/upload.html", {
        "product": product,
        "added": added,
        "comments": comments
    })


# view to display all the active listings in that category
@login_required(login_url='/login')
def category(request, categ):
    # retieving all the products that fall into this category
    categ_products = Listing.objects.filter(category=categ)
    empty = False
    if len(categ_products) == 0:
        empty = True
    return render(request, "edunet/category.html", {
        "categ": categ,
        "empty": empty,
        "products": categ_products
    })
