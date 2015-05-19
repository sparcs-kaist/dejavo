#-*-coding:utf8-*-

import os, csv, random, sys
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dejavo.settings')
django.setup()

from django.core.files import File
from django.utils.dateparse import parse_datetime
from django.utils.html import escape

from dejavo.apps.account.models import *
from dejavo.apps.manage.models import *
from dejavo.apps.zabo.models import *

testdata_dir = './testdata'

gen_user = True
gen_article = True
User = ZaboUser

def generate_user(user_info):

    username = user_info[0]
    password = user_info[1]
    email = user_info[2]
    first_name = user_info[3]
    last_name = user_info[4]

    image = user_info[5]
    phone = user_info[6]
    bio = user_info[7]

    user = User.objects.create_user(email, password)
    user.last_name = last_name
    user.first_name = first_name
    user.is_active = True
    user.save()

    profile = User.objects.get(email = email).profile
    profile_image = testdata_dir + '/profile/' + image
    with open(profile_image, 'rb') as image_file:
        profile.profile_image.save(image, File(image_file), save = True)
    profile.phone = phone
    profile.bio = bio
    profile.save()
    user.save()

    print 'Generate user ' + last_name + ' ' + first_name + '(' + email + '), ' + phone
    return user

def generate_article(info, user_pool):

    random.shuffle(user_pool)
    num = random.randint(1, 5)

    unique = info[0]
    owner = user_pool[0:num]
    title = info[2]
    location = info[3]
    category = info[4]
    created_date = parse_datetime(info[5])
    updated_date = parse_datetime(info[6])
    content = info[7]

    article = Article(title = title, location = location, category = category,
            content = escape(content).replace('\n', '<br>'), is_published = True)
    article.save()
    article.created_date = created_date
    article.updated_date = updated_date
    article.is_published = True
    article.save()

    # Add Poster
    poster_dir = testdata_dir + '/poster/' + unique
    file_names = [f for f in listdir(poster_dir) if isfile(join(poster_dir,f))]
    image_files = map(lambda x : os.path.join(poster_dir, x), file_names)

    with open(image_files[0], 'rb') as poster_image:
        article.image.save(file_names[0], File(poster_image), save = True)
    article.save()

    # Add Attachment
    attach_dir = testdata_dir + '/attachment/' + unique
    try:
        file_names = [f for f in listdir(attach_dir) if isfile(join(attach_dir,f))]
        attach_files = map(lambda x : os.path.join(attach_dir, x), file_names)

        for i in range(len(file_names)):
            attach = Attachment(article = article)
            with open(attach_files[i], 'rb') as attach_file:
                attach.filepath.save(file_names[i], File(attach_file), save = True)
            attach.save()

    except:
        pass

    for o in owner:
        article.owner.add(o)
    
    article.save()
    print 'Generate article ' + title + '(' + category + ')'
    return article

def set_timeslot(info, article_id):
    
    label = info[1]
    timeslot_type = info[2]
    #start_time = parse_datetime(info[3])
    #end_time = None if info[4] == 'None' else parse_datetime(info[4])
    start_time = datetime.datetime.now() + timedelta(days = random.randint(1, 31))
    end_time = None if info[4] == 'None' else start_time + timedelta(days = random.randint(1, 3))
    article = Article.objects.get(id=article_id)

    timeslot = Timeslot(article = article, label = label, start_time = start_time,
            end_time = end_time, timeslot_type = timeslot_type, is_main = bool(random.getrandbits(1)))

    article.timeslot.add(timeslot)
    article.save()
    print 'Set timeslot for article(' + article.title + ') timeslot(' + \
            str(start_time) + ', ' + str(end_time) + ')'
    return timeslot

def set_contact(info, article_id):

    contact_type = info[1]
    _info = info[2]
    article = Article.objects.get(id=article_id)

    contact = Contact(article = article, contact_type = contact_type, info = _info)
    article.contact.add(contact)
    article.save()
    print 'Set contact for article(' + article.title + ') contact(' + \
            contact_type+ ', ' + _info + ')'
    return contact

def set_question(info, article_id):
    
    article = Article.objects.get(id=article_id)
    content = info[2]
    writer = User.objects.get(email=info[3] + "@sparcs.org")
    created_date = parse_datetime(info[4])

    q = Question(article = article, content = content, writer = writer)
    q.save()

    q.created_date = created_date
    q.save()
    print 'Set question for article(' + article.title + ') question(' + info[0] + ')'
    return q

def set_answer(info, q_id):

    question = Question.objects.get(id=q_id)
    content = info[1]
    writer = User.objects.get(email=info[2] + "@sparcs.org")
    created_date = parse_datetime(info[3])

    ans = Answer(question = question, content = content, writer = writer)
    ans.save()

    ans.created_date = created_date
    ans.save()
    print 'Set answer for question(' + info[0] + ') answer(' + str(created_date) + ')'
    return ans

def load_csv_file(filepath):
    content = []
    with open(filepath, 'rb') as afile:
        reader = csv.reader(afile, delimiter = ',')
        reader.next() # skip header row

        for row in reader:
            row_arr = map(lambda x : x.decode('utf8'), row)
            content.append(row_arr)
    return content

if __name__ == '__main__':

    if len(sys.argv) >= 2:
        testdata_dir = sys.argv[1]

    if gen_user:
        # Generate User
        user_csv_file = testdata_dir + '/user.csv'
        user_info = load_csv_file(user_csv_file)

        for user_arr in user_info:
            generate_user(user_arr)

    if gen_article:
        # Generate Article
        article_unique_pk_map = {}

        user_pool = list(User.objects.all())

        article_csv_file = testdata_dir + '/article.csv'
        article_info = load_csv_file(article_csv_file)
        for article_arr in article_info:
            article = generate_article(article_arr, user_pool)
            article_unique_pk_map[article_arr[0]] = article.id


        # Set timeslot
        timeslot_csv_file = testdata_dir + '/timeslot.csv'
        timeslot_info = load_csv_file(timeslot_csv_file)
        for timeslot_arr in timeslot_info:
            unique_id = timeslot_arr[0]
            set_timeslot(timeslot_arr, article_unique_pk_map[unique_id])

        # Set contact
        contact_csv_file = testdata_dir + '/contact.csv'
        contact_info = load_csv_file(contact_csv_file)
        for contact_arr in contact_info:
            unique_id = contact_arr[0]
            set_contact(contact_arr, article_unique_pk_map[unique_id])

        question_unique_pk_map = {}
        # Set question and answer
        q_csv_file = testdata_dir + '/question.csv'
        q_info = load_csv_file(q_csv_file)
        for q_arr in q_info:
            unique_id = q_arr[1]
            q = set_question(q_arr, article_unique_pk_map[unique_id])
            question_unique_pk_map[q_arr[0]] = q.id

        ans_csv_file = testdata_dir + '/answer.csv'
        ans_info = load_csv_file(ans_csv_file)
        for ans_arr in ans_info:
            unique_id = ans_arr[0]
            set_answer(ans_arr, question_unique_pk_map[unique_id])
