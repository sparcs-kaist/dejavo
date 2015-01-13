from django.http import HttpResponse
from django.shortcuts import render

import sys

def create(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_article(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_article(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_qna(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_question(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_question(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_question(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_answer(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_answer(request, article_id, question_id, answer_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_answer(request, article_id, question_id, answer_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_announcement(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)
