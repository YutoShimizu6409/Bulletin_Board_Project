from django.shortcuts import render, redirect
from .forms import BoardForm, SignUpForm
from .models import Board
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

# Create your views here.

def index(request):
    boards = Board.objects.all().order_by('-updated_at')
    return render(request, 'index.html', {'boards': boards})

def new(request):
    form = BoardForm()
    return render(request, 'new.html', {'form': form})

def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BoardForm()
    return render(request, 'new.html', {'form': form})

def show(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'show.html', {'board': board})

def edit(request, pk):
    board = Board.objects.get(pk=pk)
    form = BoardForm(instance=board)
    return render(request, 'edit.html', {'form': form, 'board': board})

def update(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('show', pk=pk)
    else:
        form = BoardForm(instance=board)
    return render(request, 'edit.html', {'form': form, 'board': board})

def delete(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        board.delete()
        return redirect('index')
    return redirect('index')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        # else:
        #     return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})
