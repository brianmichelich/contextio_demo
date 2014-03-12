import env_setup; env_setup.setup()

from django.template import add_to_builtins
add_to_builtins('agar.django.templatetags')

from webapp2 import RequestHandler, Route, WSGIApplication

from agar.env import on_production_server
from agar.django.templates import render_template


class MainHandler(RequestHandler):
    def get(self):
        render_template(self.response, 'index.html')


def contextio_accounts():
    import contextio as c

    CONSUMER_KEY = 'CONSUMER_KEY'
    CONSUMER_SECRET = 'CONSUMER_SECRET'
    EMAIL = ''

    context_io = c.ContextIO(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET
    )

    return context_io.get_accounts(email=EMAIL)


class AccountHandler(RequestHandler):
    def get(self):
        account = None
        accounts = contextio_accounts()

        # since we return a list, let's be sure we have a result
        if accounts:
            account = accounts[0]

        self.response.out.write('context %s' % account)


application = WSGIApplication(
    [
        Route('/', MainHandler, name='main'),
        Route(
            '/account',
            handler=AccountHandler,
            name='account'
        ),
    ],
    debug=not on_production_server
)
