from drf_yasg.utils import swagger_auto_schema
from emsapp.serializers.event_serializers import EventSerializer

get_events_schema = swagger_auto_schema(
    method='get',
    responses={200: EventSerializer(many=True)},
    tags=['Events']
)

post_events_schema = swagger_auto_schema(
    method='post',
    request_body=EventSerializer,
    responses={201: EventSerializer, 400: 'Bad Request - Invalid input data'},
    tags=['Events']
)