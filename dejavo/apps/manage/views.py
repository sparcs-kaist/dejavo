from django.http import HttpResponse
from django.shortcuts import render

import sys

def main(request):
    return render(request, 'manage/main.html', {'content':__name__ + '.' + sys._getframe().f_code.co_name})
    #return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def list_claim(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_claim(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def list_log(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def list_block(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def set_article_block(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def set_account_block(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)
