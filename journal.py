# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import os
import datetime
from pyramid.config import Configurator
from pyramid.view import view_config
from waitress import serve
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

# DATABASE_URL = os.environ.get(
#     'DATABASE_URL',
#     'postgresql://jameshemmaplardh:123@localhost:5432/learning-journal'
# )

#request.GET

Base = declarative_base()

from pyramid.httpexceptions import HTTPNotFound

@view_config(route_name='home', renderer='templates/test.jinja2')
def home(request):
    #import pdb; pdb.set_trace() #creates and sets break point for pb prompt
    #return "Hello World"
    return {'one': 'two'}

@view_config(route_name='other', renderer='string')
def other(request):
    # import pdb; pdb.set_trace()
    return request.matchdict

def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', True)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    if not os.environ.get('TESTING', False):
        # only bind the session if we are not testing
        engine = sa.create_engine(DATABASE_URL)
        DBSession.configure(bind=engine)
    config = Configurator(
        settings=settings
    )
    config.include('pyramid_tm')
    # configuration setup
    config = Configurator(
        settings=settings
    )
    config.include('pyramid_jinja2') #added for req
    config.add_route('home', '/')
    config.add_route('other', '/other/{special_val}')
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
    # @classmethod
    # def write(cls, title=None, text=None, session=None):
    #     instance = cls(title=title, text=text)
    #     return instance
    
    @classmethod
    def write(cls, title=None, text=None, session=None):
        if session is None:
            session = DBSession
        instance = cls(title=title, text=text)
        session.add(instance)
        return instance

def init_db():
    engine = sa.create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

# def write():
#     'title': "Test Title", 'text': "Test entry text"

\

if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 5000)
    serve(app, host='0.0.0.0', port=port)
