lona-django
===========

This package contains `Lona <http://lona-web.org>`_ helper to integrate with
`Django <https://www.djangoproject.com/>`_.


Django Auth
-----------

Django authentication, authorization and sessions are implemented in a Lona
middleware.

.. code-block:: python

    # settings.py

    MIDDLEWARES = [
        'lona_django.middlewares.DjangoSessionMiddleware',
    ]

To configure authorization use the view flags listed below. The flags are
all optional and can be mixed.

The Django user associated with the given request is available in
``request.user``.

.. code-block:: python

    # views.py

    from lona import LonaView

    class DjangoView(LonaView):
        DJANGO_AUTH_LOGIN_REQUIRED = False
        DJANGO_AUTH_STAFF_REQUIRED = False
        DJANGO_AUTH_STAFF_PERMISSION_OVERRIDE = True
        DJANGO_AUTH_PERMISSIONS_REQUIRED = []
        DJANGO_AUTH_GROUPS_REQUIRED = []

        def handle_request(self, request):
            user = request.user
