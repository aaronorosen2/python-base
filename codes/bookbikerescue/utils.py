# calendarapp/utils.py

from datetime import datetime, timedelta , date
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar ):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day

	def formatday(self, day, events ):
		events_per_day = events.filter(date__day=day )
		d = ''
		for event in events_per_day:
			d += f"""
				<li class="list-group-item"> {event.get_html_url} </li>
				"""
		
		if day != 0:
			x = date(self.year, self.month, day)
			if x.weekday() == 1:
				return f"""<td  class="text-danger" >

				<span class="list-group custom"> Closed </span> 
 				<span class='date'>
				<a href="#eventmodel" data-toggle="modal" class="open-AddBookDialog" data-val="{x}"   > {day}</a>
					</span>
					<ul class="list-group custom"> {d} </ul>  
					
					</td>"""
			else:
				return f"""<td><span class='date'>
				<a href="#eventmodel" data-toggle="modal" class="open-AddBookDialog" data-val="{x}" > {day}</a>
				</span>
				<ul class="list-group custom"> {d} </ul>  </td>"""
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events ):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events )
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self,  withyear=True):
		events = Event.objects.filter( date__year=self.year, date__month=self.month )
		cal = f'<table  class="calendar" style="width:100%" >\n'
		# cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()} \n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events  )} \n'
		return cal