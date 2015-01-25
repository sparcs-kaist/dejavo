from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from accept_checker.decorators import require_accept_formats
from dejavo.apps.zabo.models import Article, Question, Answer

import sys

def main(request):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST'])
def create(request):
    if not request.user.is_authenticated():
        return JsonResponse(
                status = 401,
                data = {
                    'error' : 'User does not authorized'
                    },
                )

    owner = set(request.POST.getlist('owner', [request.user.username]))
    new_article = Article()
    new_article.save()
    new_article.owner.add(*map(lambda o : get_user_model().objects.get(username = o), owner))
    new_article.save()

    if request.ACCEPT_FORMAT == 'json':
        response = JsonResponse(
                status = 201,
                data = new_article.as_json()
                )
        response['Location'] = '/article/' + str(new_article.id) + '/edit/'
        return response

    elif request.ACCEPT_FORMAT == 'html':
        response = HttpResponse(status = 201, content = '')
        response['Location'] = '/article/' + str(new_article.id) + '/edit/'
        return response

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

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST'])
def edit_article(request, article_id):

    if not request.user.is_authenticated():
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(status = 401, content = 'User does not authorized')
        else:
            return JsonResponse(
                    status = 401,
                    data = {
                        'error' : 'User does not authorized'
                        },
                    )

    try:
        article = Article.objects.get(id = article_id)
        if request.user not in article.owner.all():
            msg = 'User does not own the article'
            if request.ACCEPT_FORMAT == 'html':
                return HttpResponse(status = 403, content = msg)
            elif request.ACCEPT_FORMAT == 'json':
                return JsonResponse(status = 403, data = { 'error' : msg })

    except Article.DoesNotExist:
        msg = 'Article(' + str(article_id) + ') does not exist'
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(status = 404, content = msg)
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(status = 404, data = { 'error' : msg })

    if request.ACCEPT_FORMAT == 'html':
        # TODO Give article editing page
        return HttpResponse(status = 200, content = 'Article editing page')

    update_fields = request.POST.getlist('fields', None)
    if not update_fields:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'fields parameter is required'
                    }
                )

    model_fields = Article._meta.get_all_field_names()
    real_update_field = set(update_fields) & set(model_fields)

    try:
        article.set_fields(real_update_field, request.POST, request.FILES)
        article.full_clean()
        article.save()

        return JsonResponse(
                status = 200,
                data = {
                    'updated_fields' : list(real_update_field), 
                    'article' : article.as_json()
                    }
                )

    except ValidationError as e:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid format',
                    'msg' : e.message_dict,
                    },
                )

def create_timeslot(request, article_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)

def delete_timeslot(request, article_id, timeslot_id):
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

def edit_announcement(request, article_id, announcement_id):
    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name)
