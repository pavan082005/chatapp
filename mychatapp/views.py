from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from mychatapp.models import Friend, Profile, Message
from .forms import MessageForm

# Create your views here.
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user" : user, "friends" : friends}
    return render(request, 'mychatapp/index.html', context)

def detail(request, pk):
    friend =  Friend.objects.get(profile_id = pk)
    user = request.user.profile
    profile = Profile.objects.get(id = friend.profile.id)
    chats = Message.objects.all()
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.recipient = profile
            message.save()
            return redirect("detail", pk = friend.profile.id)
    context = {"friend" : friend, "form" : form, "user" : user, "profile" : profile, "chats" : chats}
    return render(request, 'mychatapp/detail.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password and confirm password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Username length check
        if len(username) > 10:
            messages.error(request, "Username is too long")
            return redirect('register')

        # Password length check
        if len(password) < 3:
            messages.error(request, "Password is too short")
            return redirect('register')

        # Create the user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()
        profile = Profile.objects.create(user = myuser, name = username)
        Friend.objects.create(profile = profile);
        messages.success(request, "Your account has been created successfully")
        return redirect('signin')

    return render(request, "mychatapp/register.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

   # return render(request, "authentication/signin.html")
    return render(request, "mychatapp/signin.html")

def find_friends(request):
    friends = Friend.objects.all()

    context = {
        "friends" : friends
    }
    return render(request, "mychatapp/find_friends.html", context)



def add_friend(request):
    if request.method == "POST":
        user_profile = request.user.profile

        # Get the friend's profile ID from the POST request
        friend_id = request.POST.get('friend_id')

        # Ensure the friend_id is valid and corresponds to an existing Profile
        friend_profile = get_object_or_404(Profile, id=friend_id)

        # Ensure Friend instances are used
        friend_instance, created = Friend.objects.get_or_create(profile=friend_profile)

        # Add the friend to the user's friend list
        user_profile.friends.add(friend_instance)

        # Optionally, add the user to the friend's friend list for mutual friendship
        user_friend_instance, created = Friend.objects.get_or_create(profile=user_profile)
        friend_profile.friends.add(user_friend_instance)

        # Redirect to the find friends page
        return redirect('find_friends')  # Adjust this if needed

    # If not a POST request, redirect to find friends
    return redirect('find_friends')

def signout(request):
    if request.method == "POST":
        # Log out the user
        logout(request)
        # Redirect to the login page or another page after logout
        return redirect('register')  # Replace 'login' with the name of your login URL
    return redirect('index')  # Replace 'index' with the name of your home page URL


