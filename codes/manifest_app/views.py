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

from .extras import transact, generate_client_token, create_customer, create_subscription


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


class ManifestMonthCalendar(XFrameOptionsExemptMixin, View):
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
        context['client_token'] = generate_client_token()
        return render(request, "manifest_calendar.html", context)


class ManifestCreateEvent(XFrameOptionsExemptMixin, View):
    def post(self, request, *args, **kwargs):
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        result = transact({
            'amount': 100,
            'payment_method_nonce': request.POST.get('payment_method_nonce'),
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            Event.objects.create(date=date, title=title,
                                start_time=start_time,
                                end_time=end_time,
                                description=description,
                                is_payment=True,
                                braintreeID=result.transaction.id)
            messages.success(request, "Event has been createds .")
            return redirect('manifest')
        else:
            Event.objects.create(date=date, title=title,
                                start_time=start_time,
                                end_time=end_time,
                                description=description,
                                is_payment=False,
                                braintreeID="")
            messages.error(request, "Event is Not created because Transaction is not successful.")
            return redirect('manifest')
        


class ManifestEventDetailView(XFrameOptionsExemptMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        event = Event.objects.get(id=id)
        context = {}
        context['event'] = event
        return render(request, "manifest-event/manifest_eventdetail.html", context)


class ManifestEventDeleteView(XFrameOptionsExemptMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        e = Event.objects.get(id=id)
        e.delete()
        messages.warning(request, f"Event has been deleted successfuly !")
        return redirect('manifest')


class ManifestDateEventAll(XFrameOptionsExemptMixin, View):
    def get(self, request, *args, **kwargs):
        date = kwargs.get('date')
        evets = Event.objects.filter(date=date).order_by('-created_date')
        context = {
            'date': date,
            'events': evets
        }
        return render(request, 'manifest-date/manifest_datedetail.html', context)
