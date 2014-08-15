import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count, Sum
from django.core.mail import EmailMessage

from twospaces.conference.models import (
    Session,
    Invoice,
    Sponsor
)


class EventBriteAPI(object):
    def __init__(self, event_id, oauth_token):
        self.requests = requests
        self.base_url = settings.EVENTBRITE_API_URL
        self.event_id = event_id
        self.oauth_token = oauth_token

    def _build_url(self, path):
        return '{}/{}'.format(self.base_url, path)

    def _make_request(self, url, method, params):
        params.update({
            'token': self.oauth_token
        })

        if method == 'GET':
            response = self.requests.get(url, params=params)

        return response.json()

    def get(self, url, params):
        return self._make_request(url, 'GET', params)

    def events(self, endpoint, params={}):
        path = 'events/{}/{}'.format(
            self.event_id,
            endpoint
        )
        url = self._build_url(path)
        return self.get(url, params)


class Command(BaseCommand):
    """Send a weekly stats email"""
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.eventbrite = EventBriteAPI(
            settings.EVENTBRITE_EVENT_ID,
            settings.EVENTBRITE_OAUTH_TOKEN
        )

    def eb_orders(self, page=1):
        """Get orders from and eventbrite event and cache it"""
        key = 'eventbrite.orders.{}'.format(page)
        orders = cache.get(key)

        if not orders:
            orders = self.eventbrite.events('orders', {'page': page})
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
            total += len(order['attendees'])

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
        session_total = len(Session.objects.all())
        session_types = Session.objects.values('stype').annotate(Count('stype'))
        session_levels = Session.objects.values('level').annotate(Count('level'))

        # get the sponsors count and invoice totals
        sponsors = Sponsor.objects.filter(active=True).count()
        invoice_total = Invoice.objects.aggregate(Sum('amount'))
        invoice_paid_total = Invoice.objects.filter(paid_on__isnull=False).aggregate(Sum('amount'))

        # print 'TOTAL:', eb_total_attendees
        # print 'GROSS:',eb_gross_sales
        # print 'NET:', eb_net_sales
        # print 'TOTAL_SESSIONS:', session_total
        # print 'SESSION_TYPES:', session_types
        # print 'SESSION_LEVELS:', session_levels
        # print 'SPONSORS:', sponsors
        # print 'INVOICE_TOTAL:', invoice_total
        # print 'INVOICE_PAID_TOTAL', invoice_paid_total

        # setup the message parameters for string formatting
        html_params = {
            'eb_total_attendees': eb_total_attendees,
            'eb_gross_sales': eb_gross_sales,
            'eb_net_sales': eb_net_sales,
            'sponsors': sponsors,
            'invoice_total': invoice_total['amount__sum'],
            'invoice_paid_total': invoice_paid_total['amount__sum'],
            'sessions': session_total,
            'sessions_beginner': [d['level__count'] for d in session_levels if d['level'] == 'beginner'][0],
            'sessions_intermediate': [d['level__count'] for d in session_levels if d['level'] == 'intermediate'][0],
            'sessions_advanced': [d['level__count'] for d in session_levels if d['level'] == 'advanced'][0],
            'sessions_lightning': [d['stype__count'] for d in session_types if d['stype'] == 'lightning'][0],
            'sessions_short': [d['stype__count'] for d in session_types if d['stype'] == 'talk-short'][0],
            'sessions_long': [d['stype__count'] for d in session_types if d['stype'] == 'talk-long'][0],
        }

        html_message = """
            <h2>EventBrite</h2>
            <table align="left" cellpadding="2" cellspacing="2">
                <tr>
                    <th>Name</th>
                    <th>Total</ht>
                </tr>
                <tr>
                    <td>Attendees</td>
                    <td>{eb_total_attendees}</td>
                </tr>
                <tr>
                    <td>Gross Sales</td>
                    <td>{eb_gross_sales}</td>
                </tr>
                <tr>
                    <td>Net Sales</td>
                    <td>{eb_net_sales}</td>
                </tr>
            </table>
            <h2>Sponsorship</h2>
            <table align="left" cellpadding="2" cellspacing="2">
                <tr>
                    <th>Name</th>
                    <th>Total</ht>
                </tr>
                <tr>
                    <td>Sponsors</td>
                    <td>{sponsors}</td>
                </tr>
                <tr>
                    <td>Invoiced Amount</td>
                    <td>{invoice_total}</td>
                </tr>
                <tr>
                    <td>Paid Invoiced Amount</td>
                    <td>{invoice_paid_total}</td>
                </tr>
            </table>
            <h2>Sessions</h2>
            <table align="left" cellpadding="2" cellspacing="2">
                <tr>
                    <th>Name</th>
                    <th>Total</ht>
                </tr>
                <tr>
                    <td>Sessions</td>
                    <td>{sessions}</td>
                </tr>
                <tr>
                    <td>Beginner</td>
                    <td>{sessions_beginner}</td>
                </tr>
                <tr>
                    <td>Intermediate</td>
                    <td>{sessions_intermediate}</td>
                </tr>
                <tr>
                    <td>Advanced</td>
                    <td>{sessions_advanced}</td>
                </tr>
                <tr>
                    <td>Lightning (5min) </td>
                    <td>{sessions_lightning}</td>
                </tr>
                <tr>
                    <td>Short (25 min)</td>
                    <td>{sessions_short}</td>
                </tr>
                <tr>
                    <td>Long (50 min)</td>
                    <td>{sessions_long}</td>
                </tr>
            </table>
        """.format(**html_params)

        email = EmailMessage(
            'PyTexas Weekly Stats',
            html_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.WEEKLY_STATS_EMAIL,]
        )
        email.content_subtype = "html"
        email.send()
