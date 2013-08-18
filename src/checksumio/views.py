from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError


@view_config(route_name='index', renderer='index.jinja2')
def index(request):
    return {}

@view_config(route_name="revcheck")
def revcheck(request):
    payload = request.params["payload"]
    checksum = request.params["checksum"]
    return Response(
        "<strong>%s</strong>: %s" % (payload, checksum))
