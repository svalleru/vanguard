import logging

from rest_framework.renderers import status
from rest_framework.response import Response

from vanguard.models import Users, Sessions

logger = logging.getLogger('vanguard')


def validate_token(func):
    def new_func(*args, **kwargs):
        if len(args) != 1:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        if 'HTTP_TOKEN' not in args[0].META.keys():
            return Response({'error': 'token missing from HTTP headers'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            http_token = args[0].META['HTTP_TOKEN']
            session = Sessions.objects.filter(key__exact=http_token)
            # sha1 hash collision - this is almost impossible, but let's have a check
            if len(session) > 1:
                logger.debug("validate_token: session collision found")
                return Response({'error': 'something terribly went wrong!'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif len(session) < 1:
                logger.debug("validate_token: session collision found")
                return Response({'error': 'invalid token / no active session'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                session = session.first()
                # if the token is valid, replace token with respective user email which
                # will be used later on while creating the client
                args[0].META['HTTP_TOKEN'] = Users.objects.filter(id=session.user_id)[0].email
                return func(*args, **kwargs)
        except Exception as ex:
            str_ex = str(ex)
            logger.debug("validate_token: %s" % str_ex)
            return Response({'error': 'something terribly went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_func
