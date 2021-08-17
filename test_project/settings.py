ROUTING_TABLE = 'routes.py::routes'

MIDDLEWARES = [
    'lona_django.middlewares.DjangoSessionMiddleware',
]

ERROR_500_VIEW = 'views/error_500.py::Error500View'
