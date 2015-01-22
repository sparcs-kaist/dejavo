from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.core.exceptions import ValidationError

from accept_checker.decorators import require_accept_formats
from dejavo.apps.zabo.models import Article, Question, Answer

import sys

def main(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def view_article(request, article_id):

    if request.ACCEPT_FORMAT == 'html':
        return render(request, 'zabo/article.html', {})

    try:
        article = Article.objects.get(id = article_id)
        return JsonResponse(status=200, data=article.as_json())
    except Article.DoesNotExist:
        return JsonResponse(
                status=404,
                data={'error':'Not Found: article_id : ' + article_id}
                )

def edit_article(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def view_qna(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

@require_accept_formats(['application/json'])
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
        is_private = True if request.POST.get('is_private', False) == 'true' else False
        question = Question(article = article, writer = request.user,
                content = request.POST.get('content', ''),
                is_private = is_private)
        question.full_clean()
        question.save()

        return JsonResponse(
                status = 200,
                data = question.as_json()
                )

    except Article.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'article(' + article_id + ') does not exist'
                    },
                )

    except ValidationError as e:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid format',
                    'msg' : e.message_dict,
                    },
                )


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
def load_question(request, article_id):
    try:
        question_list = []
        article = Article.objects.get(id = article_id)
        for q in Question.objects.filter(article__id = article_id):
            question_list.append(q.as_json())
        return JsonResponse(status=200, data={'questions':question_list})
    except Article.DoesNotExist:
        return JsonResponse(
                status=404,
                data={'error':'Not Found: article_id : ' + article_id}
                )


def delete_question(request, article_id, question_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)


@require_accept_formats(['application/json'])
@require_http_methods(['POST', 'PUT'])
def create_answer(request, article_id, question_id):

    if not request.user.is_authenticated():
        return JsonResponse(
                status = 401,
                data = {
                    'error' : 'User dose not authorized'
                    },
                )
    
    try:
        question = Question.objects.get(id=question_id)
        if question.article.id != int(article_id):
            return JsonResponse(
                    status = 400,
                    data = {
                        'error' : 'Question(' + str(question_id) + \
                                ') does not belong to Article(' + \
                                str(article_id) + ')'
                        },
                    )

        answer = Answer(question = question, writer = request.user,
                content = request.POST.get('content', ''))
        answer.full_clean()
        answer.save()

        return JsonResponse(
                status = 200,
                data = answer.as_json(),
                )

    except Question.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'question(' + question_id+ ') does not exist'
                    },
                )

    except ValidationError as e:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid format',
                    'msg' : e.message_dict,
                    },
                )

def delete_answer(request, article_id, question_id, answer_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def create_announcement(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def edit_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)
