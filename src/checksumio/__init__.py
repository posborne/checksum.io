from pyramid.config import Configurator
from sqlalchemy import create_engine


def make_checksumio_wsgiapp(*args, **settings):
    """This function returns a Pyramid WSGI application"""
    engine = create_engine('sqlite:///foo.db')
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("checksumio:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('revcheck', '/revcheck')
    config.scan()
    return config.make_wsgi_app()


def main(global_config, **settings):
    """Return a pyramid WSGI application"""
    return make_checksumio_wsgiapp(**settings)
