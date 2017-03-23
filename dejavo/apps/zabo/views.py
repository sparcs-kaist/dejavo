from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.db.models import Count, Q

from accept_checker.decorators import require_accept_formats, auth_required
from dejavo.apps.zabo.models import Article, Timeslot, Question, Answer
from dejavo.apps.account.models import Participation
from dejavo.settings import TIME_ZONE

from datetime import datetime, date

import json
import pytz
import random


@require_accept_formats(['text/html'])
@require_http_methods(['GET'])
def main(request):
    article_list = []
    articles_set = Article.objects.filter(timeslot__start_time__gte=datetime.now(),
            is_published=True, is_deleted=False, is_blocked=False).distinct()
    for article in articles_set:
        article_j = article.as_json()
        article_j['date'] = get_day(article)
        if article_j['date'] is not None:   #None if main timeslot passed
            article_list.append(article_j)

    return render(request, 'zabo/main.html', {'articles': article_list})


@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@auth_required
@csrf_exempt
def create(request):

    remove_draft = request.GET.get('force', False)
    draft = Article.objects.filter(owner__id = request.user.id,
            is_published = False, is_deleted = False, is_blocked = False)

    if remove_draft:
        draft.delete()

    elif (len(draft) > 0):
        draft_article = draft[0]
        template = loader.get_template('zabo/article_draft_check.html')
        context = RequestContext(request, {'article' : draft_article})
        html = template.render(context)
        response = JsonResponse(
                status = 200,
                data = {
                    'html' : html,
                    'location' : '/article/' + str(draft_article.id) + '/edit/'
                })
        return response

    owner = set(request.POST.getlist('owner', [request.user.email]))
    new_article = Article(is_published = False)
    new_article.save()
    new_article.owner.add(*map(lambda o : get_user_model().objects.get(email = o), owner))
    new_article.save()

    response = JsonResponse(status = 201, data = {})
    response['Location'] = '/article/' + str(new_article.id) + '/edit/'
    return response


@require_accept_formats(['text/html', 'application/json', '*/*'])
@require_http_methods(['GET'])
def view_article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)

        error_flag = False
        if article.is_deleted or article.is_blocked:
            error_flag = True
            msg = 'Article is deleted'
        elif not article.is_published:
            error_flag = True
            msg = 'Article is not published'

        if error_flag:
            if request.ACCEPT_FORMAT == 'json':
                return JsonResponse(status = 404, data = {'error' : msg})
            else:
                return HttpResponse(status = 404, content = msg)

        if request.ACCEPT_FORMAT == 'json':
            return JsonResponse(status = 200, data = article.as_json())
        else:
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)

            question = Question.objects.filter(article=article).extra(select = {
                        'num_a' : 'SELECT COUNT(*) FROM zabo_answer WHERE zabo_question.id=zabo_answer.question_id',
                        'num_d_a' : 'SELECT COUNT(*) FROM zabo_answer WHERE zabo_answer.is_deleted = 1' + \
                                ' and zabo_question.id=zabo_answer.question_id'
                        }, where = ['zabo_question.is_deleted = 0 OR ' + \
                                'zabo_question.is_deleted = 1 AND "num_a" > "num_d_a"'])

            return render(request, 'zabo/article.html', {
                'article' : article,
                'site' : site,
                'question' : question,
                'participant' : map(lambda x : x.user,
                    Participation.objects.filter(article = article)),
                'is_participating' : Participation.objects.filter(user = request.user.id,
                    article = article).exists(),
                'is_owner' : len(article.owner.filter(id = request.user.id)) > 0,
                'request' : request,
                })

    except Article.DoesNotExist:
        if request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 404,
                    data = {'error' : 'Not Found: article_id : ' + article_id}
                    )
        else:
            return HttpResponse(
                    status = 404,
                    content = 'Not Found: article_id : ' + article_id
                    )

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
@auth_required
@csrf_exempt
def edit_article(request, article_id):
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
        return render(request, 'zabo/article_edit.html', {
            'article' : article,
            })

    update_fields = request.POST.get('fields', '').split(',')
    if len(update_fields) == 0:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'fields value should exist at least one'
                    }
                )

    model_fields = map(lambda f : f.name, Article._meta.local_fields)
    real_update_field = set(update_fields) & set(model_fields)

    try:
        error_dict = {}

        if 'timeslot' in update_fields:

            post_timeslot_str = request.POST.get('timeslot')
            post_timeslot_list = json.loads(post_timeslot_str)

            keep_timeslot = {}
            new_timeslot = []
            for ts in post_timeslot_list:
                if 'id' in ts:
                    keep_timeslot[int(ts['id'])] = ts
                else:
                    new_timeslot.append(ts)

            curr_timeslot_list = Timeslot.objects.filter(article = article)
            keep_timeslot_list = Timeslot.objects.filter(article = article, id__in = keep_timeslot.keys())
            remove_list = set(curr_timeslot_list) - set(keep_timeslot_list)

            for k_ts in keep_timeslot_list:
                k_ts.is_main = keep_timeslot[k_ts.id]['is_main']
                k_ts.save()

            if (len(new_timeslot) + len(keep_timeslot) <= 0):
                error_dict['timeslot_count'] = ['At least one time slot is needed']
                # we should stop updating timeslots right now.

            else:
                new_ts_list = []
                for ts in new_timeslot:
                    try:
                        new_ts = Timeslot(article = article, timeslot_type = ts['type'],
                                # editedit
                                start_time = ts['start_time'], end_time = ts['end_time'],
                                exist_end = ts['exist_end'],
                                is_am_start = ts['is_am_start'], is_am_end = ts['is_am_end'],
                                is_main = ts['is_main'], label = ts['label'])
                        new_ts.full_clean()
                        new_ts_list.append(new_ts)
                    except ValidationError as e:
                        if 'timeslot' in error_dict:
                            error_dict['timeslot'].append('Wrong time format: ' + str(ts))
                        else:
                            error_dict['timeslot'] = ['Wrong time format: ' + str(ts)]

                for new_ts in new_ts_list:
                    new_ts.save()
                for r_ts in remove_list:
                    r_ts.delete()
                    

        else :
            timeslot_list = Timeslot.objects.filter(article = article).values('id')
            if (len(timeslot_list) <= 0):
                error_dict['timeslot_count'] = ['At least one time slot is needed']

        if 'owner' in update_fields:
            post_owner_str = request.POST.get('owner')
            post_owner_list = map(lambda x : int(x), json.loads(post_owner_str))

            if (len(post_owner_list) <= 0):
                error_dict['owner'] = ['At leat one owner is needed']

            article.owner.clear()
            article.owner.add(*post_owner_list)

        article.set_fields(real_update_field, request.POST, request.FILES)
        if article.is_published:
            article.full_clean()

            if len(error_dict) > 0:
                raise ValidationError('Invalid Format on time slot or owner')

        article.save()
        response = JsonResponse(
                status = 200,
                data = {
                    'updated_fields' : list(real_update_field), 
                    'article' : article.as_json()
                    }
                )
        response['Location'] = '/article/' + str(article.id) + '/'
        return response

    except ValidationError as e:
        e_dict = getattr(e, 'message_dict', {})
        e_dict.update(error_dict)

        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid format',
                    'msg' : e_dict,
                    },
                )

@require_accept_formats(['application/json'])
@require_http_methods(['POST', 'GET'])
@auth_required
@csrf_exempt
def delete_article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
        if len(article.owner.filter(id = request.user.id)) > 0:
            article.is_deleted = True
            article.save()
            return JsonResponse(status = 200, data = article.as_json())
        else:
            return JsonResponse(
                    status = 400,
                    data = { 'error' : 'User dose not own article' }
                    )

    except Article.DoesNotExist:
        msg = 'Article(' + str(article_id) + ') does not exist'
        return JsonResponse(status = 404, data = { 'error' : msg })


@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@auth_required
def create_timeslot(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
        if request.user not in article.owner.all():
            msg = 'User does not own the article'
            return JsonResponse(status = 403, data = { 'error' : msg })
        timeslot = Timeslot(article = article,
                timeslot_type = request.POST.get('type', ''),
                start_time = request.POST.get('start_time', None),
                end_time = request.POST.get('end_time', None),
                exist_end = request.POST.get('exist_end', False),
                is_am_start = request.POST.get('is_am_start', False),
                is_am_end = request.POST.get('is_am_end', False),
                label = request.POST.get('label', '')
                )
        timeslot.full_clean()
        timeslot.save()

        return JsonResponse(
                status = 200,
                data = timeslot.as_json()
                )

    except Article.DoesNotExist:
        msg = 'Article(' + str(article_id) + ') does not exist'
        return JsonResponse(status = 404, data = { 'error' : msg })

    except ValidationError as e:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid format',
                    'msg' : e.message_dict,
                    },
                )


@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@auth_required
def delete_timeslot(request, article_id, timeslot_id):
    try:
        timeslot = Timeslot.objects.get(id = timeslot_id)
        if request.user not in timeslot.article.owner.all():
            return JsonResponse(
                    status = 403,
                    data = {
                        'error' : 'User does not have the permission'
                        },
                    )

        timeslot.delete()

        return JsonResponse(status = 200, data = {})

    except Timeslot.DoesNotExist:
        msg = 'Timeslot(' + str(timeslot_id) + ') does not exist'
        return JsonResponse(status = 404, data = { 'error' : msg })


@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def view_qna(request, article_id):

    try:
        article = Article.objects.get(id = article_id)
        qna = []
        for q in Question.objects.filter(article__id = article_id):
            qna.append(q.as_json())
        
        # TODO render page showing only questions and answers
        if request.ACCEPT_FORMAT == 'html':
            #return render(request, 'zabo/qna.html', {})
            return HttpResponse()

        return JsonResponse(status = 200, data = { 'qna' : qna })

    except Article.DoesNotExist:
        msg = 'Article(' + str(article_id) + ') does not exist'
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(status = 404, content = msg)
        else:
            return JsonResponse(status = 404, data = { 'error' : msg })


@require_accept_formats(['application/json'])
@require_http_methods(['POST', 'PUT'])
@auth_required
@csrf_exempt
def create_question(request, article_id):
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

        return JsonResponse(status=200, data={ 'questions' : question_list })

    except Article.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'article(' + article_id + ') does not exist'
                    },
                )


@require_accept_formats(['application/json'])
@require_http_methods(['GET', 'DELETE'])
@auth_required
@csrf_exempt
def delete_question(request, article_id, question_id):
    try:
        question = Question.objects.get(id = question_id, article__id = article_id)
        if question.writer != request.user:
            return JsonResponse(status = 403,
                    data = {'error' : 'User does not own the question'})

        question.is_deleted = True
        question.save()
        return JsonResponse(status = 200, data = {})

    except Question.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'question(' + question_id + ') does not exist'
                    },
                )


@require_accept_formats(['application/json'])
@require_http_methods(['POST', 'PUT'])
@auth_required
@csrf_exempt
def create_answer(request, article_id, question_id):
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


@require_accept_formats(['application/json'])
@require_http_methods(['GET', 'DELETE'])
@auth_required
@csrf_exempt
def delete_answer(request, article_id, question_id, answer_id):
    try:
        answer = Answer.objects.get(id = answer_id, question__id = question_id,
                question__article__id = article_id)
        if answer.writer != request.user:
            return JsonResponse(status = 403,
                    data = {'error' : 'User does not own the question'})
        answer.is_deleted = True
        answer.save()

        return JsonResponse(status = 200, data = {})

    except Article.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'article(' + article_id + ') does not exist'
                    },
                )

    except Question.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'question(' + question_id + ') does not exist'
                    },
                )

    except Answer.DoesNotExist:
        return JsonResponse(
                status = 404,
                data = {
                    'error' : 'answer(' + answer_id + ') does not exist'
                    },
                )


@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def view_category(request):
    return render(request, 'zabo/category.html', {})


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
def get_category(request, category):
    article_list = []

    article_set = Article.objects.filter(timeslot__start_time__gte=datetime.now(),
            is_published=True, is_deleted=False, is_blocked=False).distinct()
    if category != "all":
        article_set = article_set.filter(category = category)

    for a in article_set:
        article_j = a.as_json(['subtitle', 'owner', 'location', 'announcement', 'created_date', 'updated_date', 'content', 'contact', 'timeslot', 'host', 'attachment'])
        article_j['date'] = get_day(a)
        if article_j['date'] is not None:   #None if main timeslot passed
            article_list.append(article_j)

    article_list = sorted(article_list, key=lambda y: y['date'], reverse=False)
    
    return JsonResponse(
            status = 200,
            data = {
                'articles' : article_list
                }
            )

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def get_articles(request):
    return get_n_articles(request, 5)

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def get_n_articles(request, n):
    article_list = []
    article_set = Article.objects.filter(timeslot__start_time__gte=datetime.now())
    
    for a in article_set:
        if not article_list or not article_list[-1].get("id") == a.id:
            article_list.append(a.as_json())
            
    if len(article_list) > int(n):
        article_list = random.sample(article_list, int(n))
        
    return JsonResponse(
            status = 200,
            data = {
                'articles' : article_list
                }
            )

def get_day(article):
    times = Timeslot.objects.filter(article = article, is_main = True).order_by('start_time')
    if not times:
        #no main timeslot
        times = Timeslot.objects.filter(article = article).order_by('start_time')
    for t in times:
        if t.start_time > pytz.timezone(TIME_ZONE).localize(datetime.now()):
            return t.start_time

    return None
