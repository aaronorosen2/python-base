# from sortedcontainers import SortedSet
import calendar
from datetime import date, datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from datetimerange import DateTimeRange
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView,DetailView
from .models import Item,Event
from .utils import Calendar
from django.views.decorators.clickjacking import xframe_options_exempt
from    sfapp2.utils.twilio import send_sms
from form_lead.utils.email_util import send_raw_email
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from .serializers import ItemSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
class ItemList(View):
    def get(self,request):
        items=Item.objects.all()
        cont={'item_list':items}
        return render(request,'bookingsystem/item_list.html',cont)

class ItemDetail(DetailView):
    model=Item

class Upload(View):
    def get(self, request, *args, **kwargs):
        return render(request, "bookingsystem/upload.html")
    
@api_view(['POST'])  
def CreateItem(request):
    item_data = JSONParser().parse(request)
    item_serializer = ItemSerializer(data=item_data)
    if item_serializer.is_valid():
        item_serializer.save()
        return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateItem(UpdateView):
    model=Item
    fields='__all__'
    success_url = reverse_lazy('bookingsystem:items')
    
class DeleteItem(DeleteView):
    model=Item
    fields='__all__'
    success_url = reverse_lazy('bookingsystem:items')


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


class MonthCalendar(LoginRequiredMixin,XFrameOptionsExemptMixin, View):
    def get(self, request, *args, **kwargs):
        date = get_date(request.GET.get('month', None))
        user=self.request.user.username
        cal = Calendar(date.year, date.month,user)
        cal.setfirstweekday(6)
        html_cal = cal.formatmonth(withyear=True)
        item_id=self.request.GET.get('item',None)
        item=Item.objects.get(pk=item_id)
        context = {}
        context['calendar'] = mark_safe(html_cal)
        context["date"] = date
        context['prev'] = 'item='+item_id+'&'+prev_month(date)
        context['next'] = 'item='+item_id+'&'+next_month(date)
        context['item'] = item
        return render(request, "bookingsystem/calendar.html", context)

    
class CreateEvent(LoginRequiredMixin,XFrameOptionsExemptMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        choices            = request.POST.get('choices')
        item = request.POST.get('item')
        date_obj           = datetime.strptime(date, "%Y-%m-%d")

        Event.objects.create(
            date=date,
            start_time=start_time,
            end_time=end_time,
            name=name,
            email=email,
            phone=phone, 
            frequency = choices,
            item_id=item,
            owner = self.request.user
            )
        """
        send_sms('8434259777', 'test body')
        send_raw_email(
            to_email= ['aaronorosen@gmail.com',],
             reply_to=['test@test.com',], 
              subject='test Subject',
            message_text='test message',
        
        )
        """

        
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
                            frequency = choices,
                            item_id=item,
                            owner = self.request.user
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
                    frequency = choices,
                    item_id=item,
                    owner = self.request.user
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
                    frequency = choices,
                    item_id=item,
                    owner = self.request.user
                    )
    
            

        messages.success(request,
                         f"Your reservation has been created {start_time} - {end_time}.")
        return redirect('/bookingsystem/calendar?item='+item)


class EventDetailView(XFrameOptionsExemptMixin,LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        global back
        back=request.META.get('HTTP_REFERER')
        id = kwargs.get('event_id')
        event = Event.objects.get(id=id,owner = self.request.user)
        context = {}
        context['event'] = event
        context['back']=back
        return render(request, "bookingsystem/event/eventdetail.html", context)


class EventDeleteView(XFrameOptionsExemptMixin,LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        e = Event.objects.get(id=id,owner = self.request.user)
        e.delete()
        messages.warning(request, f"Event has been deleted successfuly ! ")
        return redirect(str(back))


class DateEventAll(XFrameOptionsExemptMixin,LoginRequiredMixin, View):
    def get(self, request,  *args, **kwargs):
        date = kwargs.get('date')
        evets = Event.objects.filter(date=date,owner=self.request.user).order_by('-created_date')
        context = {
            'date': date,
            'events': evets,
        }
        return render(request, 'bookingsystem/date/datedetail.html',  context)

class YourBookings(LoginRequiredMixin,View):
    def get(self,request):
        events=Event.objects.filter(owner=self.request.user)
        context={'events':events}
        return render(request,'bookingsystem/your_bookings.html',context)
