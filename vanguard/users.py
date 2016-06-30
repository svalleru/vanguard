import logging
import time
from datetime import datetime

# import re
import hashlib

from models import Users, Sessions

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, status
from rest_framework.response import Response
from vanguard.settings import KEY as SECRET
from cryptography.fernet import Fernet

from utils import validate_token

logger = logging.getLogger('vanguard')


def encrypt(message):
    """encrypts the message"""
    try:
        cipher_suite = Fernet(SECRET)
        cipher_text = cipher_suite.encrypt(bytes(message))
    except Exception as ex:
        logger.debug("encrypt: %s", str(ex))
    return cipher_text


def decrypt(enc_message):
    """decrypts the enc_message"""
    try:
        cipher_suite = Fernet(SECRET)
        plain_text = cipher_suite.decrypt(bytes(enc_message))
    except Exception as ex:
        logger.debug("decrypt: %s", str(ex))
    return plain_text


def sha1hash(message):
    """returns sha1 hash for message"""
    try:
        _sha1 = hashlib.sha1()
        _sha1.update(message)
    except Exception as ex:
        logger.debug("sha1hash: %s", str(ex))
    return _sha1.hexdigest()


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer,))
def user_signup(request):
    """
    Create a new user
    Accepts:
        "email": <string>
        "first_name": <string>
        "last_name": <string>
        "password": <string>
    Returns:
        HTTP_200_OK: if the association is successful
        or
        "error": <string> Exception msg string
    Example POST payload:
    {
        "first_name": "foo",
        "last_name": "bar",
        "email": "foo@bar.com",
        "password": "this_is_secret"
    }
    """
    if request.method == 'POST':
        start_time = time.time()
        if set(['email', 'first_name', 'last_name', 'password']) != set(request.data.keys()):
            return Response({'error': "invalid params"}, status=status.HTTP_400_BAD_REQUEST)
        # if not re.match(r'[^@]+@[^@]+\.[^@]+', request.data['email']):
        #     return Response({'error': "invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(email__iexact=request.data['email']):
            return Response({'error': "user exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_user = Users(email=request.data['email'], first_name=request.data['first_name'],
                             last_name=request.data['last_name'], password=encrypt(request.data['password']))
            new_user.save()
            logger.debug("user_signup: elapsed time: %s" % (time.time() - start_time))
            return Response(status=status.HTTP_200_OK)
        except Exception as ex:
            str_ex = str(ex)
            logger.debug(("user_signup: %s", str_ex))
            logger.debug("user_signup: elapsed time: %s" % (time.time() - start_time))
            return Response({'error': str_ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        err_dict = {
            'error': 'invalid request',
            'example POST payload': {
                "first_name": "foo",
                "last_name": "bar",
                "email": "foo@bar.com",
                "password": "this_is_secret"
            }
        }
        return Response(err_dict, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer,))
def user_login(request):
    """
    Authenticates a user
    Accepts:
        "email": <string>
        "password": <string>
    Returns:
        "token": if the credentials are valid; this key has to be used in HTTP headers for accessing
               any of the backend APIs
        "email": email of the authenticated user
        "first_name": <string>
        "last_name": <string>
        or
        "error": <string> Exception msg string
    Example POST payload:
    {
        "email": "foo@bar.com",
        "password": "this_is_secret"
    }
    """
    if request.method == 'POST':
        start_time = time.time()
        if set(['email', 'password']) != set(request.data.keys()):
            return Response({'error': "invalid params"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.filter(email__iexact=request.data['email'])
        except Exception as ex:
            logger.debug("user_login: %s", str(ex))
        if user:
            # since user_signup ensures that there will always be one user, let's pluck the first
            user = user.first()
            if decrypt(user.password) == str(request.data['password']):
                old_session = Sessions.objects.filter(user_id__exact=user.id)
                if old_session:
                    old_session.update(last_used=datetime.now())
                    old_session = old_session.first()
                    logger.debug("user_login: elapsed time: %s" % (time.time() - start_time))
                    return Response({'token': old_session.key,
                                     'email': user.email,
                                     'first_name': user.first_name,
                                     'last_name': user.last_name}, status=status.HTTP_200_OK)
                else:
                    new_session = Sessions(user=user, last_used=datetime.now(), key=sha1hash(request.data['email'] +
                                                                                             request.data['password'] +
                                                                                             SECRET))
                    new_session.save()
                    logger.debug("user_login: elapsed time: %s" % (time.time() - start_time))
                    return Response({'token': new_session.key,
                                     'email': user.email,
                                     'first_name': user.first_name,
                                     'last_name': user.last_name}, status=status.HTTP_200_OK)
            else:
                logger.debug("user_login: invalid password for %s", request.data['email'])
                return Response({'error': 'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.debug("user_login: invalid email %s", request.data['email'])
            return Response({'error': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer,))
@validate_token
def forgot_password(request):
    # TBD
    pass


@api_view(['POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer,))
@validate_token
def user_logout(request):
    """
    Accepts:
        "token" HTTP header
    Returns:
        HTTP_200_OK: if the logout is successful
        HTTP_500_INTERNAL_SERVER_ERROR: in bizarre situations
    """
    user_email = request.META['HTTP_TOKEN']
    user = Users.objects.filter(email__iexact=user_email).first()
    try:
        Sessions.objects.filter(user_id__exact=user.id).delete()
        return Response({'info': "logout success!"}, status=status.HTTP_200_OK)
    except Exception as ex:
        logger.debug("user_logout: %s", str(ex))
        return Response({'error': "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
