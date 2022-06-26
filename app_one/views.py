from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from app_one.models import User, Wish
from django.shortcuts import redirect, render
import bcrypt


def index(request):
    return render(request, "Login_Reg.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            name = request.POST["name"]
            username = request.POST["username"]
            password = request.POST["password"]
            conf_pssword = request.POST["conf_pssword"]
            date_hired = request.POST["date_hired"]
            if(password == conf_pssword):
                # end of validation , start hashing ....

                # Generate some random bytes
                salt = bcrypt.gensalt()
                # .hashpw will return us the password hashed in bytes, so we need to decode it
                hash = bcrypt.hashpw(password.encode(), salt)
                # decode the hash from bytes to string to store it in the database as a string
                User.objects.create(
                    name=name, username=username, password=hash.decode(), date_hired=date_hired)
                messages.success(request, "User successfully registered")
            else:
                messages.error(
                    request, "Password must match the confirmed password")
            return redirect("/")
    return redirect("/register")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["loggedInUser"] = user.id
                return redirect("/displayList")

            messages.error(
                request, "incorrect Password")

        except User.DoesNotExist:
            messages.error(
                request, "You do not have an account ,Please Register first !")

        return redirect("/")
    return redirect("/")


def displayList(request):
    if "loggedInUser" not in request.session:
        return HttpResponse("Your List is empty")

    loggedInUser = User.objects.get(id=request.session["loggedInUser"])
    context = {
            "user": loggedInUser,
            # get all wishes created by this user
            "user_wishes": loggedInUser.wishes.all(),
            # get all wishes this user added it to his/her fav_wishes
            "user_fav_wishes": loggedInUser.fav_wishes.all(),
            # get all fav_wishes not added to this user
            "otherusers_items": Wish.objects.exclude(user_wishs=loggedInUser).exclude(users=loggedInUser),
        }
    
        
    return render(request, "wishList.html", context)


def addToFavWish(request, itemId):
    item = Wish.objects.get(id=itemId)
    loggedInUser = User.objects.get(id=request.session["loggedInUser"])
    loggedInUser.fav_wishes.add(item)
    print("item added...........")
    return redirect("/displayList")


def addToWish(request):
    if request.method == "POST":
        item_name = request.POST["item"]
        loggedInUser = User.objects.get(id=request.session["loggedInUser"])
        if len(request.POST["item"]) < 4:
            messages.error(
                request, "Product name must be al least 4 characters")
            return redirect("/viewAddWish")
        else:
            Wish.objects.create(item_name=item_name, users=loggedInUser)
        return redirect("/displayList")
    return redirect("/displayList")


def deleteItem(request, itemId):
    item = Wish.objects.get(id=itemId)
    item.delete()
    return redirect("/displayList")


def removeItem(request, itemId):
    loggedInUser = User.objects.get(id=request.session["loggedInUser"])
    wish = Wish.objects.get(id=itemId)
    wish.user_wishs.remove(loggedInUser)
    return redirect("/displayList")


def viewAddWish(request):
    return render(request, "create.html")


def logout(request):
    request.session.flush()
    return redirect("/")


def viewItem(request, itemId):
    wish = Wish.objects.get(id=itemId)
    loggedInUser = User.objects.get(id=request.session["loggedInUser"])

    context = {
        "user": loggedInUser,
        "wish": wish,
        "wish_users": wish.user_wishs.all()

    }
    return render(request, "view-item.html", context)
