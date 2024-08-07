from django.shortcuts import render, redirect
from .forms import BoardForm, SignUpForm
from .models import Board
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps

# Create your views here.

def user_owns_board(view_func):
    @wraps(view_func)
    def wrapper(request, pk):
        board = get_object_or_404(Board, pk=pk)
        if board.user == request.user:
            return view_func(request, pk)
        else:
            return redirect('index')
    return wrapper

def index(request):
    boards = Board.objects.all().order_by('-updated_at')
    return render(request, 'index.html', {'boards': boards})

@login_required
def new(request):
    form = BoardForm()
    return render(request, 'new.html', {'form': form})

@login_required
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
    else:
        form = BoardForm()
    return render(request, 'new.html', {'form': form})

@login_required
def show(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'show.html', {'board': board})

@login_required
@user_owns_board
def edit(request, pk):
    board = Board.objects.get(pk=pk)
    form = BoardForm(instance=board)
    return render(request, 'edit.html', {'form': form, 'board': board})

@login_required
@user_owns_board
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

@login_required
@user_owns_board
def delete(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        board.delete()
        return redirect('index',pk=pk)
    return redirect('index')

@login_required
def my_boards(request):
    user = request.user
    boards = user.boards.all()
    return render(request, 'my_boards.html', {'boards':boards})

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
        else:
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})