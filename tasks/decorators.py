import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def log_action(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[1]
            logger.info(f"{action} action performed by {request.user}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def active_user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if hasattr(arg, 'user') and hasattr(arg, 'method'):
                request = arg
                break
        if request and not request.user.is_active:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        return func(*args, **kwargs)
    return wrapper