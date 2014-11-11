from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext

import json


def main(request):
    return HttpResponse("<p>apps.account.views.main</p><p>/account/</p>")

def login(request):

    if request.is_ajax() and request.method == "POST":
        # handle login process
        userid = request.POST.get("id", None)
        passwd = request.POST.get("passwd", None)

        if userid == None or passwd == None:
            return HttpResponse(json.dump({
                "error" : 400, "msg" : "Invalid id or password"
                }),
                status = 400)

        user = authenticate(username = userid, password = passwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dump({
                    "error" : None,
                    "msg" : "ok",
                    }))

    else:
        # login page
        return render_to_response("login.html")


@login_required
def logout(request):

    logout(request)
    return redirect("/")

@login_required
def ch_passwd(request):

    if request.is_ajax() and request.method == "POST":

        new_password = request.POST.get("new_password", None)
        if new_password == None:
            return HttpResponse(json.dump({
                "error" : 400, "msg" : "Invalid password parameter"
                }),
                status = 400)

        user = request.user
        user.set_password(new_password)
        user.save()

        return HttpResponse(json.dump({
            "error" : None,
            "msg" : "ok",
            }))

    else:
        # invalid request
        return HttpResponse(json.dump({
            "error" : 400, "msg" : "Invalid request"
            }),
            status = 400)
