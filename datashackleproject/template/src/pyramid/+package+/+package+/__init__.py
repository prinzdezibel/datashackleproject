from pyramid.config import Configurator
from p2.datashackle.core import init_datashackle_core

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
   
    # This MUST happen after configuration scan 
    init_datashackle_core(settings)
    
    return config.make_wsgi_app()


