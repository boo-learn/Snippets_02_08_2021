from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', "form": form}
        return render(request, 'pages/add_snippet.html', context)

    form = SnippetForm(request.POST, request.FILES)
    # print("user = ", request.user)
    if form.is_valid():
        snippet = form.save(commit=False)
        if request.user.is_authenticated:
            snippet.user = request.user
        snippet.save()
        return redirect('snippets-list')
    context = {'pagename': 'Добавление нового сниппета', "form": form}
    return render(request, 'pages/add_snippet.html', context)


@login_required
def delete_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    if snippet.user != request.user:
        raise HttpResponseForbidden
    snippet.delete()
    return redirect('snippets-list')


@login_required
def edit_snippet_page(request, id):
    if request.method == "GET":
        snippet = Snippet.objects.get(pk=id)
        form = SnippetForm(instance=snippet)
        # if snippet.user == request.user:
        context = {
            'pagename': 'Страница сниппета',
            "snippet": snippet,
            "edit": True,
            "form": form
        }
        return render(request, 'pages/snippet_info.html', context)
    # обрабатываем данные от формы и изменяем Сниппет


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', "snippets": snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    snippet = Snippet.objects.get(pk=id)
    form_comment = CommentForm()
    context = {'pagename': 'Страница сниппета', "snippet": snippet, "form_comment": form_comment}
    return render(request, 'pages/snippet_info.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {"form": form}
        return render(request, 'pages/register_page.html', context)

    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home')
    context = {"form": form}
    return render(request, 'pages/register_page.html', context)


@login_required
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST["snippet_id"]
        if comment_form.is_valid():
            snippet = Snippet.objects.get(id = snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()

        return redirect(f'/snippet/{snippet_id}')

    raise Http404