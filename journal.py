# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import os
import datetime
from pyramid.config import Configurator
from pyramid.view import view_config
from waitress import serve


# DATABASE_URL = os.environ.get(
#     'DATABASE_URL',
#     'postgresql://jameshemmaplardh:123@localhost:5432/learning-journal'
# )



Base = declarative_base()

@view_config(route_name='home', renderer='string')
def home(request):
    return "Hello World"


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', True)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    # configuration setup
    config = Configurator(
        settings=settings
    )
    config.add_route('home', '/')
    config.scan()
    app = config.make_wsgi_app()
    return app

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://jameshemmaplardh:123@localhost:5432/learning-journal'
)

#from chris
class Entry(Base):
    __tablename__ = 'entries'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Unicode(127), nullable=False)
    text = sa.Column(sa.UnicodeText, nullable=False)
    created = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow
    )


def init_db():
    engine = sa.create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 5000)
    serve(app, host='0.0.0.0', port=port)