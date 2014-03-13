from collections import OrderedDict

PIZZA_TEMPLATES = OrderedDict([
  ('pages/standard-page.html', {
    'name': 'Standard Page',
    'regions': OrderedDict([
        ('content', ('rich', 'Content')),
    ]),
    'inlines': OrderedDict([]),
  })
])
