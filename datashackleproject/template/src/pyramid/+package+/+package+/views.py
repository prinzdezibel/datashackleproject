from p2.datashackle.core import Session
from pyramid.view import view_config
from pyramid.response import Response
from .models import Person, Media

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    
    session = Session()
    persons = session.query(Person).all()

    return {'persons': persons}


@view_config(route_name='media')
def media(request):
    id = int(request.matchdict['id'])
    session = Session()
    image = session.query(Media).get(id)
    return Response(body=image.thumbnail, headerlist=[('Content-Type', str(image.mime_type))])

