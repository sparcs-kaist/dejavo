from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def main(request):
    return HttpResponse("<p>apps.post.views.main</p><p>/main/</p>")

def main_redirect(request):
    return HttpResponseRedirect("/main/")

def category(request):
    return HttpResponse("<p>apps.post.views.category</p><p>/post/category/</p>")

def club(request):
    return HttpResponse("<p>apps.post.views.club</p><p>/post/club/</p>")

def register(request):
    return HttpResponse("<p>apps.post.views.register</p><p>/post/register/</p>")

def search(request):
    return HttpResponse("<p>apps.post.views.search</p><p>/post/search/</p>")
