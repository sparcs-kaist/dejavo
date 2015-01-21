from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from accept_checker.decorators import require_accept_format
from dejavo.apps.zabo.models import Article

import sys

def main(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_article(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_article(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_qna(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

@require_accept_format('application/json')
@require_http_methods(['POST', 'PUT'])
def create_question(request, article_id):

    if not request.user.is_authenticated():
        return JsonResponse(
                status = 401,
                data = {
                    'error' : 'User dose not authorized'
                    },
                )

    try:
        article = Article.objects.get(id = article_id)
        #question = Question(article = article, content = request.POST.['

    except Article.DoesNotExist:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'article(' + article_id + ') does not exist'
                    },
                )

    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_question(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_answer(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_answer(request, article_id, question_id, answer_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_announcement(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)
