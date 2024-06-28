from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django import forms

from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404.html", {
                "title": title
            })
    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    #lower characters equal to upper
    query = request.GET.get('q', '').strip().lower()
    if not query:
        return redirect('index')
    
    entries = util.list_entries()
    if query in [entry.lower() for entry in entries]:
        return redirect('entry_page', title=query.capitalize())


    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search_result.html", {
        "query": query,
        "results": results
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Content")

def create_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if util.get_entry(title):
                return render(request, "encyclopedia/create_page.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })
            
            util.save_entry(title, content)
            return redirect("entry_page", title=title)
    
    else:
        form = NewEntryForm()
    
    return render(request, "encyclopedia/create_page.html", {
        "form": form
    })


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry_page", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/not_found.html", {
                "title": title
            })
        form = EditEntryForm(initial={"content": content})
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        title = random.choice(entries)
        return redirect("entry_page", title=title)
    return redirect("index")

