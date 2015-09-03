import json
import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count, Sum
from django.core.mail import EmailMessage
from django.utils.html import strip_tags

from twospaces.conference.models import (Session, Invoice, Sponsor)


class EventBriteAPI(object):

  def __init__(self, event_id, oauth_token):
    self.requests = requests
    self.base_url = settings.EVENTBRITE_API_URL
    self.event_id = event_id
    self.oauth_token = oauth_token

  def _build_url(self, path):
    return '{}/{}'.format(self.base_url, path)

  def _make_request(self, url, method, params):
    params.update({'token': self.oauth_token})

    if method == 'GET':
      response = self.requests.get(url, params=params)

    return response.json()

  def get(self, url, params):
    return self._make_request(url, 'GET', params)

  def events(self, endpoint, params={}):
    path = 'events/{}/{}'.format(self.event_id, endpoint)
    url = self._build_url(path)
    return self.get(url, params)


class Command(BaseCommand):
  """Send a weekly stats email"""

  args = '<console>'

  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self.eventbrite = EventBriteAPI(
        settings.EVENTBRITE_EVENT_ID, settings.EVENTBRITE_OAUTH_TOKEN)

    self.questions = {
        '10258511': {'question': 'Attend Tutorials',
                     'answers': {}},
        '10080265': {'question': 'Skill Level',
                     'answers': {}},
        '10080266': {'question': 'T-Shirt Size',
                     'answers': {}},
        '10080267': {'question': 'Food Accomodations',
                     'answers': {}},
    }

  def eb_orders(self, page=1):
    """Get orders from and eventbrite event and cache it"""
    key = 'eventbrite.orders.{}'.format(page)
    orders = cache.get(key)

    if not orders:
      orders = self.eventbrite.events(
          'orders', {'page': page,
                     'status': 'active',
                     'expand': 'attendees'})
      cache.set(key, orders)

    return orders

  def eb_total_attendees(self, total=0, page=1):
    """Get total number of attendees
    
    :param float total: the net total of attendees
    :param int page: the query page that contains the attendees
    """
    orders = self.eb_orders(page)
    page_count = orders['pagination']['page_count']

    for order in orders['orders']:
      for attendee in order['attendees']:
        if not attendee['refunded']:
          for ans in attendee['answers']:
            if 'answer' in ans:
              a = ans['answer']

            else:
              a = 'No Answer'

            key = ans['question_id']
            if a in self.questions[key]['answers']:
              self.questions[key]['answers'][a] += 1

            else:
              self.questions[key]['answers'][a] = 1

          total += 1

    if page_count == page:
      return total

    if page_count > 1:
      page += 1
      return self.eb_total_attendees(total, page)

  def eb_orders_gross_amount(self, total=0.00, page=1):
    """Get the gross dollar amount of all eventbrite event orders

    :param float total: the net total of orders
    :param int page: the query page that contains the orders
    """
    orders = self.eb_orders(page)
    page_count = orders['pagination']['page_count']

    for order in orders['orders']:
      costs = order['costs']
      gross = costs['gross']['value']
      total += (gross / 100)

    if page_count == page:
      return total

    if page_count > 1:
      page += 1
      return self.eb_orders_gross_amount(total, page)

  def eb_orders_net_amount(self, total=0.00, page=1):
    """Get the net dollar amount of all eventbrite event orders

    :param float total: the net total of orders
    :param int page: the query page that contains the orders
    """
    orders = self.eb_orders(page)
    page_count = orders['pagination']['page_count']

    for order in orders['orders']:
      costs = order['costs']
      gross = costs['gross']['value']
      payment_fee = costs['payment_fee']['value']
      eventbrite_fee = costs['eventbrite_fee']['value']
      total += gross - (payment_fee + eventbrite_fee)

    if page_count == page:
      return total / 100

    if page_count > 1:
      page += 1
      return self.eb_orders_net_amount(total, page)

  def handle(self, *args, **options):
    # get the total number of orders
    eb_total_attendees = self.eb_total_attendees()

    # get the gross sales for all event orders
    eb_gross_sales = self.eb_orders_gross_amount()

    # get the net sales for all event orders
    eb_net_sales = self.eb_orders_net_amount()

    # get the session counts
    session_total = Session.objects.filter(conference__slug='2015').count()
    session_total_approved = Session.objects.filter(
        conference__slug='2015',
        status='accepted',).count()

    session_qs = Session.objects.filter(conference__slug='2015')
    session_ap = session_qs.filter(status='accepted')

    # get the sponsors count and invoice totals
    sponsors = Sponsor.objects.filter(active=True).count()
    invoice_total = Invoice.objects.aggregate(Sum('amount'))
    invoice_paid_total = Invoice.objects.filter(
        paid_on__isnull=False).aggregate(Sum('amount'))

    # setup the message parameters for string formatting
    html_params = {
        'eb_total_attendees': eb_total_attendees,
        'eb_gross_sales': eb_gross_sales,
        'eb_net_sales': eb_net_sales,
        'sponsors': sponsors,
        'invoice_total': invoice_total['amount__sum'],
        'invoice_paid_total': invoice_paid_total['amount__sum'],
        'sessions': session_total,
        'sessions_approved': session_total_approved,
        'sessions_beginner': session_qs.filter(level='beginner').count(),
        'sessions_intermediate':
        session_qs.filter(level='intermediate').count(),
        'sessions_advanced': session_qs.filter(level='advanced').count(),
        'sessions_lightning': session_qs.filter(stype='lightning').count(),
        'sessions_short': session_qs.filter(stype='talk-short').count(),
        'sessions_long': session_qs.filter(stype='talk-long').count(),
        'sessions_beginner_approved': session_ap.filter(
            level='beginner').count(),
        'sessions_intermediate_approved': session_ap.filter(
            level='intermediate').count(),
        'sessions_advanced_approved': session_ap.filter(
            level='advanced').count(),
        'sessions_lightning_approved': session_ap.filter(
            stype='lightning').count(),
        'sessions_short_approved': session_ap.filter(
            stype='talk-short').count(),
        'sessions_long_approved': session_ap.filter(stype='talk-long').count(),
    }

    questions = ''
    for key, question in self.questions.items():
      questions += '<tr>'
      questions += '<td style="text-align: left;padding: 5px; vertical-align: top;">{}</td>\n'.format(
          question['question'])
      answers = ''
      for answer, count in question['answers'].items():
        answers += '{}: {}<br>\n'.format(answer, count)

      questions += '<td style="text-align: left;padding: 5px; vertical-align: top;">{}</td>'.format(
          answers)
      questions += '</tr>\n'

    html_params['questions'] = questions

    html_message = """
      <h2>EventBrite</h2>
      <table>
          <tr>
              <th style="text-align: left;padding: 5px;">Name</th>
              <th style="text-align: left;padding: 5px;">Total</ht>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Attendees</td>
              <td style="text-align: left;padding: 5px;">{eb_total_attendees}</td>
          </tr>
          {questions}
          <tr>
              <td style="text-align: left;padding: 5px;">Gross Sales</td>
              <td style="text-align: left;padding: 5px;">{eb_gross_sales}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Net Sales</td>
              <td style="text-align: left;padding: 5px;">{eb_net_sales}</td>
          </tr>
      </table>
      <h2>Sponsorship</h2>
      <table>
          <tr>
              <th style="text-align: left;padding: 5px;">Name</th>
              <th style="text-align: left;padding: 5px;">Total</ht>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Sponsors</td>
              <td style="text-align: left;padding: 5px;">{sponsors}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Invoiced Amount</td>
              <td style="text-align: left;padding: 5px;">{invoice_total}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Paid Invoiced Amount</td>
              <td style="text-align: left;padding: 5px;">{invoice_paid_total}</td>
          </tr>
      </table>
      <h2>Sessions</h2>
      <table>
          <tr>
              <th style="text-align: left;padding: 5px;">Name</th>
              <th style="text-align: left;padding: 5px;">Total</ht>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Sessions</td>
              <td style="text-align: left;padding: 5px;">{sessions}, Approved: {sessions_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Beginner</td>
              <td style="text-align: left;padding: 5px;">{sessions_beginner}, Approved: {sessions_beginner_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Intermediate</td>
              <td style="text-align: left;padding: 5px;">{sessions_intermediate}, Approved: {sessions_intermediate_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Advanced</td>
              <td style="text-align: left;padding: 5px;">{sessions_advanced}, Approved: {sessions_advanced_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Lightning (5min) </td>
              <td style="text-align: left;padding: 5px;">{sessions_lightning}, Approved: {sessions_lightning_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Short (25 min)</td>
              <td style="text-align: left;padding: 5px;">{sessions_short}, Approved: {sessions_short_approved}</td>
          </tr>
          <tr>
              <td style="text-align: left;padding: 5px;">Long (50 min)</td>
              <td style="text-align: left;padding: 5px;">{sessions_long}, Approved: {sessions_long_approved}</td>
          </tr>
      </table>
    """.format(**html_params)

    if 'console' in args:
      print(strip_tags(html_message))

    elif 'quiet' in args:
      pass

    else:
      email = EmailMessage(
          'PyTexas Weekly Stats', html_message,
          settings.WEEKLY_STATS_FROM_EMAIL, [settings.WEEKLY_STATS_EMAIL,])
      email.content_subtype = "html"
      email.send()
