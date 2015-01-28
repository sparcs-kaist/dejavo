from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from accept_checker.decorators import require_accept_formats, check_authentication
from dejavo.apps.zabo.models import Article

import sys

def main(request):
    return render(request, 'manage/main.html', {})

def list_claim(request):
    return render(request, 'manage/claim.html', {})

def view_claim(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def list_log(request):
    return render(request, 'manage/log.html', {})

def list_block(request):
    return render(request, 'manage/block.html', {})


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@check_authentication
def set_article_block(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
        article.is_blocked = True
        article.save()

        return JsonResponse(status = 200, data = {})

    except Article.DoesNotExist:
        msg = 'Article(' + str(article_id) + ') does not exist'
        return JsonResponse(status = 404, data = { 'error' : msg })


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@check_authentication
def set_account_block(request, account_id):
    try:
        user = User.objects.get(id = account_id)
        user.is_active = False
        user.save()

        return JsonResponse(status = 200, data = {})

    except User.DoesNotExist:
        msg = 'User(' + account_id + ') does not exist'
        return JsonResponse(status = 404, data = { 'error' : msg })
