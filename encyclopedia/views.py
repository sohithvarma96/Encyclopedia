from django.shortcuts import render
import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util
import random
from django.shortcuts import redirect

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='Content')
def html_to_md(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('entries'))
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def random_page(request):
    entries = util.list_entries()
    if entries:
        selected_page = random.choice(entries)
        return HttpResponseRedirect(reverse('entry', args=[selected_page]))      
    else:
        return render(request, "encyclopedia/error.html")    

def new_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)  
            return HttpResponseRedirect('/entry/' + title)  
    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/new_entry.html', {'form': form})
    
def entry(request, title):
    html_page = html_to_md(title)
    if html_page == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html",{
            "content": html_page  
        })
def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        search_query = html_to_md(query)
        if search_query is not None:
            return render(request, "encyclopedia/entry.html", {
                "content": search_query
            })
        else:
            search_lists = []
            entries = util.list_entries()
            for entry in entries:
                if query.lower() in entry.lower():
                    search_lists.append(entry)
            return render(request, "encyclopedia/search_results.html", {
                "search_lists": search_lists
            })
def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                "content": content,
                "title": title})
def save_edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = request.POST['content']
        util.save_entry(title, content)
        entry = html_to_md(content)
        return render(request, "encyclopedia/edit.html",
                      {"title": title, "content": entry})



