from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Channel, Message
from .forms import RegisterForm
from django.http import HttpResponse

def only_admin(user): 
    return user.role == 'admin'

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def tylko_admin(request):
    if not only_admin(request.user):
        return HttpResponse("Brak dostępu")

@login_required
def home(request):
    channels = Channel.objects.all()
    return render(request, 'home.html', {'channels': channels})

@login_required
def channel(request, id):
    channel = Channel.objects.get(id=id)
    channels = Channel.objects.all()
    messages = Message.objects.filter(channel=channel)

    if request.method == "POST":
        content = request.POST.get('content', '').strip()
        image_url = request.POST.get('image_url', '').strip()

        if content or image_url:
            Message.objects.create(
                user=request.user,
                channel=channel,
                content=content,
                image_url=image_url
            )
        return redirect(f'/channel/{id}/')

    return render(request, 'channel.html', {
        'channel': channel,
        'channels': channels,
        'messages': messages
    })

@login_required
def delete_message(request, id):
    msg = Message.objects.get(id=id)

    if request.user.role in ['admin', 'mod']:
        msg.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))
