"""
    The code includes views for user authentication, creating, updating, and deleting rooms, as well as
    displaying user profiles and messages in a chat application.
    
    :param request: The `request` parameter in Django represents the HTTP request that was sent to the
    server. It contains information about the request, such as the user making the request, any data
    sent with the request, and other metadata. The view functions in Django take the `request` parameter
    to process the request and
    :return: The code provided contains various views and functions related to user authentication, room
    management, and messaging within a Django web application.
"""

from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.views import View
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from .forms import RoomForm, TopicForm, UserForm, MyUserCreationForm
from django.core.paginator import Paginator


def login_page(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email", "").lower()
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email or password")
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            messages.error(request, "Invalid Email or password")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    # request.session.flush()
    return redirect("login")


def register_page(request):

    page = "register"
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login(request, user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
        else:
            messages.error(request, "Invalid form")

    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q", "").strip()

    rooms = Room.objects.select_related("host", "topic")
    if q == "" or q.lower() == "all":
        rooms = rooms.order_by("-created")
    else:
        rooms = rooms.filter(
            Q(topic__name__icontains=q)
            | Q(name__icontains=q)
            | Q(description__icontains=q)
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))

    # Pagination logic for rooms
    paginator = Paginator(rooms, 3)  # Show 3 rooms per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "rooms": page_obj.object_list,
        "topics": topics,
        "room_count": room_count,
        "room_message": room_message,
        "page_obj": page_obj,
    }
    return render(request, "base/home.html", context)


# @login_required(login_url='login')
def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You are not logged in.")
            return redirect("room", pk=room.id)

        Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userprofile(request, pk):
    p_user = get_object_or_404(User, id=pk)
    rooms = p_user.room_set.select_related("host", "topic")
    room_message = p_user.message_set.all()
    topics = Topic.objects.all()
    # rooms = Room.objects.filter(participants=p_user)
    context = {
        "p_user": p_user,
        "rooms": rooms,
        "room_message": room_message,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid():

        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect("home")
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in!")
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # form = RoomForm(initial=room)
    if request.user != room.host:
        return HttpResponse("<h2/>You are not allowed here")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


def topic_room(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, "base/topic.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponse("<h2/>You are not allowed here")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return HttpResponse("<h2/>You are not allowed here")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})


def activityPage(request):
    room_message = Message.objects.select_related("user", "room")
    return render(request, "base/activity.html", {"room_message": room_message})
