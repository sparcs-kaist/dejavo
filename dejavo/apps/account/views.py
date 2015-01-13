from django.http import HttpResponse
from django.shortcuts import render

import sys

def main(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name) 

def create(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name) 

def edit(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name) 

def unsubscribe(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name) 

