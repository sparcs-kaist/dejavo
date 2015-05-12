from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.db.models import Q

from accept_checker.decorators import require_accept_formats, auth_required 
from jwt_auth.token import generate_jwt, refresh_jwt
from social.apps.django_app.utils import psa
from social.exceptions import NotAllowedToDisconnect

from dejavo.apps.account.models import Participation, RegistrationProfile
from dejavo.apps.zabo.models import Article

import json

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
def login_view(request):

    if request.user.is_authenticated():
        if request.ACCEPT_FORMAT == 'html':
            next_link = request.GET.get('next', '/')
            return HttpResponseRedirect(next_link)

        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Already logged in'}
                    )

    if request.method == 'GET':
        return render(request, "account/login.html")

    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    
    if not email or not password:
        # invalid format
        if request.ACCEPT_FORMAT == 'html':
            return render(request, "account/login.html", {
                'error_msg' : 'Fail to login'
                })

        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(status = 400,
                    data = {'error' : 'Invalid format'}
                    )

    user = authenticate(username = email, password = password)

    if user is None:
        # login fail page. wrong password, email 
        if request.ACCEPT_FORMAT == 'html':
            return render(request, "account/login.html", {
                'error_msg' : 'Fail to login'
                })

        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Failed to login'}
                    )

    if not user.is_active:
        # user inactive
        if request.ACCEPT_FORMAT == 'html':
            # XXX user blocked page??
            return HttpResponse(
                    status = 403,
                    content = 'User is blocked'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 403,
                    data = {'error' : 'User is blocked'}
                    )
    else:
        login(request, user)
        # login success
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponseRedirect(request.GET.get(REDIRECT_FIELD_NAME, '/')
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 200,
                    data = user.as_json()
                    )

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def logout_view(request):
    logout(request)
    if request.ACCEPT_FORMAT == 'html':
        return HttpResponse(
                status = 200,
                content = 'Successfully logout'
                )
    elif request.ACCEPT_FORMAT == 'json':
        return JsonResponse(
                status = 200,
                data = {'msg' : 'Successfully logout'}
                )

@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@csrf_exempt
def jwt_login(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if not email or not password:
        # invalid format
        return JsonResponse(status = 400, data = {'error' : 'Invalid format'})

    user = authenticate(username = email, password = password)

    if user is None:
        # login fail page. wrong password, email 
        return JsonResponse(status = 400, data = {'error' : 'Failed to login'})

    if not user.is_active:
        # user inactive
        return JsonResponse(status = 403, data = {'error' : 'User is blocked'})
    
    try:
        user_token = generate_jwt(user)
        return JsonResponse(status = 200, data = user_token)
    except:
        return JsonReponse(status = 500, data = {'error' : 'Internal server error'})


@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@csrf_exempt
def jwt_refresh(request):
    user_token = request.POST.get('token', None)

    if user_token is None:
        return JsonResponse(status = 400, data = {'error' : 'Invalid format'})

    try:
        new_user_token = refresh_jwt(request.user, user_token)
        return JsonResponse(status = 200, data = new_user_token)
    except:
        return JsonReponse(status = 500, data = {'error' : 'Internal server error'})


@require_accept_formats(['application/json'])
@psa()
def auth_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    try:
        if request.user.is_authenticated():
            user = request.backend.do_auth(token, user=request.user)
        else:
            user = request.backend.do_auth(token)

    except ValidationError as e:
        return JsonResponse(status = 400,
                data = {'error' : 'Email address denied'})

    if user and user.is_active:
        login(request, user)
        data = user.as_json()
        social = request.user.social_auth.filter(provider='facebook')[0]
        data['social_url'] = 'http://www.facebook.com/' + social.uid
        return JsonResponse(status = 200, data = data)
    else:
        return JsonResponse(
                status = 401,
                data = { 'error' : 'User cannot be authorized' }
                )


@require_http_methods(['POST', 'GET'])
@require_accept_formats(['application/json'])
@auth_required
@psa()
@csrf_exempt
def disconnect_access_token(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    try:
        request.backend.disconnect(user=request.user, association_id=association_id)

    except NotAllowedToDisconnect as e:
        return JsonResponse(
                status = 400,
                data = {'error' : 'User should set password first'}
                )

    return JsonResponse(status = 200, data = request.user.as_json())


@require_accept_formats(['text/html'])
@require_http_methods(['GET'])
@auth_required
def main(request):
    # User notification, owning article, history, else else else...
    # TODO create user page

    #return HttpResponse(
    #        status = 200,
    #        content = 'User editing page'
    #        )

    from_activate = False
    has_social = len(request.user.social_auth.all()) > 0
    has_passwd = request.user.has_usable_password()
    try:
        from_activate = request.session.pop('first_login')
    except:
        pass

    section = request.GET.get('section')
    social = None
    if has_social:
        social = request.user.social_auth.filter(provider='facebook')[0]

    return render(request, "account/main.html", {
        'from_activate' : from_activate,
        'social_url' : 'http://www.facebook.com/' + social.uid if social else '',
        'has_social' : has_social,
        'has_password' : has_passwd,
        })

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
def register(request):
    # User creation page
    if request.user.is_authenticated():
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'User is already logged in'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    content = 'User is already logged in'
                    )

    if request.method == 'GET':
        return HttpResponse(
                status = 200,
                content = 'User creating page'
                )

    # create user
    email = request.POST.get('email', None)
    password1 = request.POST.get('password1', None)
    password2 = request.POST.get('password2', None)

    if not email or not password1 or not password2:
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'Invalid format'
                    )

        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Invalid format'}
                    )

    try:
        validate_email(email)
    except ValidationError as e:
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'Email validation fail'
                    )

        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Email Validation fail'}
                    )

    if password1 != password2:
        return JsonResponse(
                status = 400,
                data = {'error' : 'Password does not match'}
                )

    new_user = get_user_model().objects.create_user(email = email,
            password = password1)

    new_user.last_name = request.POST.get('lastname', '')
    new_user.first_name = request.POST.get('firstname', '')

    profile = new_user.profile
    profile.phone = request.POST.get('phone', '')
    profile.bio = request.POST.get('bio', '')

    profile.save()

    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    new_user.save()

    new_user_register = RegistrationProfile.objects.create_inactive_user(
        new_user=new_user,
        site=site,
        send_email=True,
        request=request,
    )
    new_user_register.save()

    if request.ACCEPT_FORMAT == 'html':
        response = HttpResponse(
                status = 201,
                content = 'User create complete')
        response['Location'] = '/account/edit/'
        return response

    elif request.ACCEPT_FORMAT == 'json':
        response = JsonResponse(
                status = 201,
                data = new_user.as_json()
                )
        response['Location'] = '/account/edit/'
        return response

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
def email_check(request):

    email = request.GET.get('email', None)
    user_model = get_user_model()
    if email:
        try:
            validate_email(email)
            user = user_model.objects.get(email = email)
            return JsonResponse(status = 409,
                    data = {
                        'email' : email,
                        'msg' : 'Already registed email address',
                        }
                    )
        except user_model.DoesNotExist as e:
            return JsonResponse(status = 200, data = {'email' : email})
        except ValidationError as e:
            return JsonResponse(
                    status = 400,
                    data = {
                        'error' : 'Invalid email address',
                        'msg' : 'Invalid email address',
                        }
                    )
    else:
        return JsonResponse(
                status = 400,
                data = {
                    'error' : 'Invalid request (email parameter empty',
                    'msg' : 'Email is empty',
                    }
                )

@require_accept_formats(['text/html'])
@require_http_methods(['POST', 'GET'])
def activate(request, activation_key):
    """
    Given an an activation key, look up and activate the user
    account corresponding to that key (if possible).

    """
    activated_user = RegistrationProfile.objects.activate_user(activation_key)
    # a little trick to login without password
    if activated_user:
        activated_user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, activated_user)
        request.session['first_login'] = True
        return HttpResponseRedirect(reverse('account_main'))
    else:
        return render(request, "registration/activation_fail.html")

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST'])
@auth_required
@csrf_exempt
def edit(request):

    update_fields = request.POST.get('fields').split(',')
    user = request.user

    error_list = {}

    if 'password' in update_fields:
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        if not password1 or not password2 or \
                len(password1) <= 0 or len(password2) <= 0:
            error_list.setdefault('password', []).append('Password field is empty')
        elif password1 != password2:
            error_list.setdefault('password', []).append('Password does not match')
        else:
            user.set_password(password1)

    if 'profile_image' in update_fields:
        if 'profile_image' not in request.FILES:
            error_list.setdefault('profile_image', []).append('Image field is empty')
        else:
            new_profile_image = request.FILES['profile_image']
            user.profile.profile_image.save(new_profile_image.name, new_profile_image)

    if 'email' in update_fields:
        email = request.POST.get('email', None)
        try:
            validate_email(email)
            user.email = email
        except ValidationError as e:
            error_list.setdefault('email', []).append(unicode(e.message))

    if 'first_name' in update_fields:
        first_name = request.POST.get('first_name', None)
        if not first_name:
            error_list.setdefault('first_name', []).append('First name field is empty')
        else:
            user.first_name = first_name

    if 'last_name' in update_fields:
        last_name = request.POST.get('last_name', None)
        if not last_name:
            error_list.setdefault('last_name', []).append('Last name field is empty')
        else:
            user.last_name = last_name

    if len(error_list) > 0:
        if request.ACCEPT_FORMAT == 'json':
            return JsonResponse(status = 400, data = error_list)
        else:
            return HttpResponse(status = 400, content = 'Invalid format')

    user.profile.save()
    user.save()

    if request.ACCEPT_FORMAT == 'json':
        return JsonResponse(status = 200, data = user.as_json())
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def show_user(request, email):

    try:
        user_info = get_user_model().objects.get(email = email).as_json()
        if request.ACCEPT_FORMAT == 'html':
            # TODO Create user page
            return HttpResponse(
                    status = 200,
                    content = 'Show user page'
                    )
        else:
            # TODO add user's other information such as articles
            return JsonResponse(
                    status = 200,
                    data = user_info
                    )
    except get_user_model().DoesNotExist:
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 404,
                    content = 'User does not exist'
                    )
        else:
            return JsonResponse(
                    status = 404,
                    data = {'error' : 'User does not exist'}
                    )

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def search_user(request):

    query = request.GET.get('q', None)
    page = int(request.GET.get('page', 0))
    count = int(request.GET.get('count', 10))

    start = page * count
    end = start + count

    if not query:
        return JsonResponse(
                status = 400,
                data = { 'error' : 'Parameter \'q\' should be given' }
                )

    _User = get_user_model()
    user_list = _User.objects.filter(Q(email = query) |
            Q(first_name__icontains = query) | Q(last_name__icontains = query))[start:end]
    user_list_json = map(lambda x : x.as_json(), user_list)

    return JsonResponse(
        status = 200,
        data = { 'result' : user_list_json }
        )


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
def check_participate(request, article_id):

    try:
        article = Article.objects.get(id = article_id)
        check = False
        if request.user.is_authenticated():
            check = Participation.objects.filter(user = request.user,
                    article = article).exists()

        return JsonResponse(status = 200,
                data = { 'check' : check }
                )

    except Article.DoesNotExist:
        return JsonResponse(
            status = 400,
            data = { 'error' : 'Article does not exist' }
            )

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def participate(request, article_id):

    try:
        article = Article.objects.get(id = article_id)
        check = Participation.objects.filter(user = request.user, article = article)

        if check:
            return JsonResponse(status = 400,
                    data = { 'error' : 'User already participate the article' }
                    )

        p = Participation(user = request.user, article = article)
        p.save()
        return JsonResponse(status = 200, data = request.user.as_json())

    except Article.DoesNotExist:
        return JsonResponse(
            status = 400,
            data = { 'error' : 'Article does not exist' }
            )

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def unparticipate(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
        p = Participation.objects.filter(user = request.user, article = article)

        if len(p) > 0:
            p.delete()
            return JsonResponse(status = 200, data = request.user.as_json())

        return JsonResponse(status = 400,
                data = { 'error' : 'User is not participating the article' }
                )

    except Article.DoesNotExist:
        return JsonResponse(
            status = 400,
            data = { 'error' : 'Article does not exist' }
            )

@require_accept_formats(['text/html'])
@require_http_methods(['GET'])
@auth_required
def my_articles(request):
    article_list = []
    article_set = Article.objects.filter(owner = request.user)

    for a in article_set:
        article_list.append(a.as_json())

    return render(request, "account/article.html", {
        'articles' : article_list
        })
