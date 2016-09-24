# -*- coding: utf-8 
from django.core.management.base import BaseCommand
from dejavo.apps.zabo.models import Article, Timeslot
from datetime import datetime, timedelta, time, date
from django.utils import timezone
from django.db.models import Q
from dejavo.apps.account.models import ZaboUser
import requests
import time
import urllib
import json
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Portal crawling start!'
    def handle(self, *args, **options):
       # -*- coding: utf-8 -*-

        def get_event_infos(html ,session):
            soup = BeautifulSoup("".join(html), "html.parser")
            table = soup.find('table',{"class":"req_tbl_02"})
            rows = table.findAll('tr')


            try:
                event_title = rows[0].findAll('td')[0].text.strip()
                event_day = rows[1].findAll('td')[0].text.strip()
                event_place = rows[1].findAll('td')[1].text.strip()
                event_writer = rows[2].findAll('td')[0].text.strip()
                event_createdPoint = rows[2].findAll('td')[1].text.strip()
                event_text = "<p>" + "</p><p>".join(p.text for p in rows[4].findAll('td')[0].findAll('p')) + "</p>"
                event_img = rows[4].findAll('td')[0].find('img')
            except:
                event_title = ""
                event_day = ""
                event_place = ""
                event_writer = ""
                event_createdPoint = ""
                event_text = ""
                event_img = ""
            try:
                event_img = event_img['src']
            except:
                event_img = ""
            img_name = ""
            if not Article.objects.filter(title = event_title).exists() and event_img:
                r = session.get(event_img, stream=True)
                if r.status_code == 200:
                   img_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
                   img_name = "poster/" + img_time + ".jpg"
                   with open( "media/poster/" + img_time + ".jpg", 'wb') as f:
                       f.write(r.content)
                       f.close()

            ctx = {
                'event_title' : event_title,
                'event_day' : event_day,
                'event_place' : event_place,
                'event_writer' : event_writer,
                'event_createdPoint' : event_createdPoint,
                'event_text' : event_text,
                'event_img' : img_name,
            }
            return ctx


        my_id = ''
        my_pw = ''
        with open('my_account.txt', 'r') as f:
            my_id = f.readline().strip()
            my_pw = f.readline().strip()
        htmls = []

        session = requests.Session()
        cur_time = int(time.time())
        return_url = 'portal.kaist.ac.kr/user/ssoLoginProcess.face?timestamp=' + str(cur_time - 30);
        return_url = '?returnURL=' + urllib.quote(return_url, safe='~()*!.\'') + \
                     ' &timestamp=' + str(cur_time)
        base_url = 'https://portalsso.kaist.ac.kr/ssoProcess.ps'
        r = session.post(base_url + return_url, data={'userId': my_id, 'password': my_pw})

        data = {
            'boardId': 'seminar_events',
            'start': (date.today() + timedelta(days=0)).isoformat(),
            'end': (date.today() + timedelta(days=60)).isoformat(),
        }


        r = session.post('https://portal.kaist.ac.kr/board/scheduleList.brd', data=data)
        event_list =json.loads(r.text)['Data'];
        event_id_list = list(i['scheduleId'] for i in event_list)
        for event_id in event_id_list:
            htmls.append(session.get('https://portal.kaist.ac.kr/board/read.brd?cmd=READ&boardId=seminar_events&bltnNo=' + event_id + '&lang_knd=ko&userAgent=Chrome&isMobile=false&'))




 
        def create_article(ctx):

            if ctx['event_img']:
                title = ctx['event_title']
                location = ctx['event_place']
                content = ctx['event_text']
                image = ctx['event_img']
                category = "etc" 
                host_name = ctx['event_writer']
                host_description = "포탈에서 등록된 포스터입니다"
                article = Article(title=title, location=location, content=content,image=image,category=category,host_name=host_name, host_description=host_description, is_published = True)
                article.save()
                article.owner.add(ZaboUser.objects.get(id=1))
                article.save()
                parse_time1 = ctx['event_day'].split(" ")
                parse_time2 = parse_time1[0].split(".")
                parse_time3 = parse_time1[1].split(":")
                time_year = int(parse_time2[0])
                time_month = int(parse_time2[1])
                time_day = int(parse_time2[2])
                time_hour = int(parse_time3[0])
                time_minitue = int(parse_time3[1])
                date = timezone.make_aware(datetime(time_year,time_month,time_day,time_hour,time_minitue,0), timezone.get_current_timezone()) 
                timeslot = Timeslot(article=article,timeslot_type='point',start_time=date ,is_main = True)
                timeslot.save()

        for html in htmls:
            info = get_event_infos(html,session)
            create_article(info) 

