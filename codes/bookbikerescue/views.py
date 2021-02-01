# from sortedcontainers import SortedSet
import calendar
from datetime import date, datetime, timedelta

from datetimerange import DateTimeRange
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views import View

from .models import Event
from .utils import Calendar
from django.views.decorators.clickjacking import xframe_options_exempt

from    sfapp2.utils.twilio import send_sms
from form_lead.utils.email_util import send_raw_email

class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class MonthCalendar(XFrameOptionsExemptMixin, View):
    def get(self, request, *args, **kwargs):
        date = get_date(request.GET.get('month', None))
        cal = Calendar(date.year, date.month)
        cal.setfirstweekday(6)
        html_cal = cal.formatmonth(withyear=True)
        context = {}
        context['calendar'] = mark_safe(html_cal)
        context["date"] = date
        context['prev'] = prev_month(date)
        context['next'] = next_month(date)
        return render(request, "calendar.html", context)


class CreateEvent(XFrameOptionsExemptMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        choices            = request.POST.get('choices')
        date_obj           = datetime.strptime(date, "%Y-%m-%d")

        Event.objects.create(
            date=date,
            start_time=start_time,
            end_time=end_time,
            name=name,
            email=email,
            phone=phone, 
            frequency = choices
            )
        send_sms('8434259777', 'test body')
        send_raw_email(
            to_email= ['aaronorosen@gmail.com',],
             reply_to=['test@test.com',], 
              subject='test Subject',
            message_text='test message',
        )

        
#! Daily Event Creation

        list_of_mnth = calendar.monthcalendar( date_obj.year  , date_obj.month)
        
        if choices == "bg-primary":
            
            for i in list_of_mnth:
                for j in i:
                    if j > date_obj.day:
                        date_updated=date_obj.replace(day=j)
                        Event.objects.create(
                            date= date_updated , 
                            start_time= start_time , 
                            end_time=end_time ,
                            name= name, 
                            email=email, 
                            phone=phone,
                            frequency = choices
                            )

#! Weekly Event Creation

                        
        if choices == "bg-success":
            date = date_obj
            for_week_recurring = []
            for i in range(7):
                date =  date + timedelta(days=7)
               
               
                for_week_recurring.append(date)
            
            for i in for_week_recurring:
                
                Event.objects.create(
                    date= i , 
                    start_time= start_time , 
                    end_time=end_time ,
                    name= name, 
                    email=email, 
                    phone=phone,
                    frequency = choices
                    )
                
#! BiWeekly Event Creation
        
        
        if choices == "bg-danger":
            date = date_obj
            for_week_recurring = []
            for i in range(7):
                date =  date + timedelta(days=14)
                
                for_week_recurring.append(date)
            
            for i in for_week_recurring:
                
                Event.objects.create(
                    date= i , 
                    start_time= start_time , 
                    end_time=end_time ,
                    name= name, 
                    email=email, 
                    phone=phone,
                    frequency = choices
                    )
    
            

        messages.success(request,
                         f"Event has been created {start_time} - {end_time}.")
        return redirect('bookbikerescue:calendar')


class EventDetailView(XFrameOptionsExemptMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        event = Event.objects.get(id=id)
        context = {}
        context['event'] = event
        return render(request, "event/eventdetail.html", context)


class EventDeleteView(XFrameOptionsExemptMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        e = Event.objects.get(id=id)
        e.delete()
        messages.warning(request, f"Event has been deleted successfuly ! ")
        return redirect('bookbikerescue:calendar')


class DateEventAll(XFrameOptionsExemptMixin, View):
    def get(self, request,  *args, **kwargs):
        date = kwargs.get('date')
        evets = Event.objects.filter(date=date).order_by('-created_date')
        context = {
            'date': date,
            'events': evets,
        }
        return render(request, 'date/datedetail.html',  context)
