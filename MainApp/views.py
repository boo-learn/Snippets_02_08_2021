from django.contrib import auth
from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', "form": form}
        return render(request, 'pages/add_snippet.html', context)

    form = SnippetForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('snippets-list')
    context = {'pagename': 'Добавление нового сниппета', "form": form}
    return render(request, 'pages/add_snippet.html', context)


def delete_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    snippet.delete()
    return redirect('snippets-list')


def edit_snippet_page(request, id):
    if request.method == "GET":
        snippet = Snippet.objects.get(pk=id)
        context = {
            'pagename': 'Страница сниппета',
            "snippet": snippet,
            "edit": True
        }
        return render(request, 'pages/snippet_info.html', context)
    # обрабатываем данные от формы и изменяем Сниппет


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', "snippets": snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    snippet = Snippet.objects.get(pk=id)
    context = {'pagename': 'Страница сниппета', "snippet": snippet}
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