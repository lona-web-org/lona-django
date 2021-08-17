from lona import Route, MATCH_ALL

from django_project.wsgi import application
from aiohttp_wsgi import WSGIHandler

wsgi_handler = WSGIHandler(application)


routes = [
    Route('/login-required/',
          'views/permission_views.py::DjangLoginView'),

    Route('/template-based-form/',
          'views/template_based_form.py::DjangoTemplateView'),

    # home
    Route('/', 'views/home.py::HomeView'),

    # django wsgi
    Route(MATCH_ALL, wsgi_handler, http_pass_through=True),
]
