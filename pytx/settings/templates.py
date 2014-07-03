from collections import OrderedDict

PIZZA_TEMPLATES = OrderedDict([
  ('pages/standard-page.html', {
    'name': 'Standard Page',
    'regions': OrderedDict([
        ('content', ('rich', 'Content')),
    ]),
    'inlines': OrderedDict([]),
  }),
  
  ('pages/about-page.html', {
    'name': 'About Page',
    'regions': OrderedDict([
        ('content', ('rich', 'Content')),
    ]),
    'inlines': OrderedDict([]),
  }),
  
  ('pages/talk-page.html', {
    'name': 'Submit Talk Page',
    'regions': OrderedDict([
        ('content', ('rich', 'Content')),
    ]),
    'inlines': OrderedDict([]),
  })
])
