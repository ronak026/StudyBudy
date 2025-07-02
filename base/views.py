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
from .models import Room,Login,Topic,Message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.views import View
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RoomForm,TopicForm,UserForm
# from rest_framework import viewsets
from .models import Login
# from .serializer import LoginSerializer

# class LoginViewSet(viewsets.ModelViewSet):
#     queryset = Login.objects.all()
#     serializer_class = LoginSerializer

# def register_view(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']

#         if Login.objects.filter(email=email).exists():
#             messages.error(request, 'Email already registered.')
#             return redirect('register')

#         Login.objects.create(name=name, email=email, password=password)
#         messages.success(request, 'Account created. Please log in.')
#         return redirect('login')

#     return render(request, 'base/register.html')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         try:
#             user = Login.objects.get(email=email, password=password)
#             request.session['user_id'] = user.id
#             return redirect('dashboard')
#         except Login.DoesNotExist:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'base/login.html')

# def dashboard_view(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')
#     user = Login.objects.get(id=user_id)
#     return render(request, 'base/dashboard.html', {'user': user})

# def logout(request):
#     request.session.flush()  # Clear session data
#     return redirect('login')

# rooms=[
#     {'id':1, 'name':'learn python'},
#     {'id':2, 'name':'learn javascript'},
#     {'id':3, 'name':'learn java'},
    
# ]


# def login(request):
#     login=Login.objects.all()
#     return render(request,'base/signup.html',{'login':login})


# Create your views here.


class myview(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world!")

    def post(self, request, *args, **kwargs):
       # Handle POST requests
        return HttpResponse("This is a POST request")
    
    
# class Home(View):
    
#     def get(self, request, *args, **kwargs):
#         return render(request, 'base/home.html')
    
#     def post(self, request, *args, **kwargs):
#         # Handle POST requests
#         rooms=Room.objects.all()
#         context={'rooms':rooms}
#         return render(request, 'base/home.html',context)
    
    
def login_page(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Invalid username or password')
            
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
        
    context={'page':page}
    return render(request, 'base/login_register.html',context)


def logout_user(request):
    logout(request)
    # request.session.flush() 
    return redirect('login')
    
def register_page(request):
    
    page ='register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            # login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form')
        
    
        
    context={'page':page,'form':form}
    return render(request, 'base/login_register.html',context)


def home(request):
    q = request.GET.get('q', '').strip()

    if q == '' or q.lower() == 'all':
        rooms = Room.objects.all().order_by('-created')
    else:
        rooms = Room.objects.filter(
            Q(topic__name__iexact=q) |
            Q(name__iexact=q) |
            Q(description__iexact=q)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_message': room_message
    }
    return render(request, 'base/home.html', context)

# @login_required(login_url='login')
def room(request,pk):
    # return HttpResponse('room')
    room=Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You are not logged in.')
            return redirect('login')

        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages, 'participants':participants}
    return render(request,'base/room.html',context)


def userprofile(request,pk):
    p_user = User.objects.get(id=pk)
    rooms=p_user.room_set.all()
    room_message= p_user.message_set.all()
    topics=Topic.objects.all()
    # rooms = Room.objects.filter(participants=p_user)
    context = {'p_user':p_user,'rooms':rooms, 'room_message':room_message ,'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics =Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid():
            
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')
    
    context={'form':form, 'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # form = RoomForm(initial=room)
    if request.user != room.host:
        return HttpResponse('<h2/>You are not allowed here')
     
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context={'form':form, 'topics':topics, 'room':room}
    return render(request,'base/room_form.html',context)

def topic_room(request):
    form = TopicForm()
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request,'base/topic.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('<h2/>You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('<h2/>You are not allowed here')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html',{'form':form})