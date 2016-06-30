Vanguard is a simple API authentication library for Django REST Framework

Quick start
-----------

1. Add "vanguard" to your INSTALLED_APPS setting like this::
```
INSTALLED_APPS = [
            ...
            'rest_framework',
            'vanguard',
            ...
        ]
```

2. Include the vanguard URLconf in your project urls.py like this::
```
from django.conf.urls import include
:
url(r'^vanguard/', include('vanguard.urls')),
```

3. Run `python manage.py migrate` to create the vanguard models.

4. Available vanguard endpoints
```
Signup [vanguard/, vanguard/signup]
Login [vanguard/login]
Password Retieval [vanguard/forgotpassword]
Logout [vanguard/logout]
```

5. Use @validate_token as the inner most annotation for any API end point method
you wanna authenticate
``` 
from vanguard.utils import validate_token
:
.
@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer,))
@validate_token
def my_api(request):
    #On successful authentication, HTTP_TOKEN's value will be replaced by
    #authenticated user's email
    user_email=request.META['HTTP_TOKEN']
    :
```