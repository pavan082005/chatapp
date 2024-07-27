from django.shortcuts import render, redirect
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

