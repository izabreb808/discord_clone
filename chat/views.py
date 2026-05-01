from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Channel, DirectMessage, Message
from .forms import ChannelForm, ProfileForm, RegisterForm
from django.http import HttpResponse

def only_admin(user): 
    return user.role == 'admin'

def can_moderate(user):
    return user.role in ['admin', 'mod']

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
    users = get_user_model().objects.exclude(id=request.user.id)
    return render(request, 'home.html', {'channels': channels, 'users': users})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

@login_required
def create_channel(request):
    if not only_admin(request.user):
        return HttpResponse("Brak dostepu")

    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            channel.members.add(request.user)
            return redirect('/')
    else:
        form = ChannelForm()

    return render(request, 'channel_form.html', {'form': form})

@login_required
def join_channel(request, id):
    channel = Channel.objects.get(id=id)
    channel.members.add(request.user)
    return redirect(f'/channel/{id}/')

@login_required
def channel(request, id):
    channel = Channel.objects.get(id=id)
    channels = Channel.objects.all()
    messages = Message.objects.filter(channel=channel)

    if request.method == "POST":
        if request.user.is_blocked:
            return HttpResponse("Twoje konto jest zablokowane.")

        content = request.POST.get('content', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        audio_url = request.POST.get('audio_url', '').strip()

        if content or image_url or audio_url:
            Message.objects.create(
                user=request.user,
                channel=channel,
                content=content,
                image_url=image_url,
                audio_url=audio_url
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

    if can_moderate(request.user):
        msg.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def block_user(request, id):
    if not can_moderate(request.user):
        return HttpResponse("Brak dostepu")

    User = get_user_model()
    user_to_block = User.objects.get(id=id)
    if not user_to_block.role == 'admin':
        user_to_block.is_blocked = True
        user_to_block.save()

    return redirect('/')

@login_required
def unblock_user(request, id):
    if not can_moderate(request.user):
        return HttpResponse("Brak dostepu")

    User = get_user_model()
    user_to_unblock = User.objects.get(id=id)
    user_to_unblock.is_blocked = False
    user_to_unblock.save()

    return redirect('/')

@login_required
def direct_messages(request, user_id):
    User = get_user_model()
    receiver = User.objects.get(id=user_id)

    if request.method == "POST":
        if request.user.is_blocked:
            return HttpResponse("Twoje konto jest zablokowane.")

        content = request.POST.get('content', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        audio_url = request.POST.get('audio_url', '').strip()

        if content or image_url or audio_url:
            DirectMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                image_url=image_url,
                audio_url=audio_url
            )
        return redirect(f'/dm/{receiver.id}/')

    messages = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')

    users = User.objects.exclude(id=request.user.id)

    return render(request, 'dm.html', {
        'receiver': receiver,
        'messages': messages,
        'users': users
    })

def custom_404(request, exception):
    return render(request, '404.html', status=404)
