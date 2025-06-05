from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Request body schema for registering a guest
register_guest_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['name', 'email'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Guest full name'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Guest email address'),
    },
)

# Response schema for successful guest registration
register_guest_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Guest registered successfully.'),
        'guest': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            }
        )
    }
)

# Error response schema
error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error message here')
    }
)

# Decorator for register_guest view
register_guest_decorator = swagger_auto_schema(
    method='post',
    operation_description="Register a guest for an event by event ID. Validates duplicates and capacity.",
    request_body=register_guest_request_body,
    responses={
        201: register_guest_response_schema,
        400: error_response_schema,
        404: 'Event not found'
    },
    tags=['Guests']
)

# Decorator for list_event_attendees view
list_event_attendees_decorator = swagger_auto_schema(
    method='get',
    operation_description="List paginated attendees for an event by event ID.",
    responses={
        200: openapi.Response(
            description="A paginated list of attendees.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'next': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                            }
                        )
                    ),
                }
            )
        ),
        404: 'Event not found'
    },
    tags=['Guests']
)
