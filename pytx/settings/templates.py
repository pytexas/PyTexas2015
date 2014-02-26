from collections import OrderedDict

PIZZA_TEMPLATES = OrderedDict([
  ('pages/home.html', {
    'name': 'Home Page',
    'regions': OrderedDict([
        ('content', ('rich', 'Content')),
    ]),
    'inlines': OrderedDict([]),
  })
])
