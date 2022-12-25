from email_notifier_api.settings import SECRET_KEY
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

def obtain_jwt(user):
    if user:
        refresh = RefreshToken.for_user(user)
        return str(refresh),str(refresh.access_token),status.HTTP_200_OK 
    else:
        return None,None,status.HTTP_400_BAD_REQUEST
    
def verify_jwt(request):
    token=request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return False,'token not present in header'
    token = token.split(' ')[1]
    try:
        jwt.decode(token, SECRET_KEY, verify=True)
        return True,'token is valid'
    except :
        return False,'token invalid or expired'

def generate_access_token(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return False,'token is not present'
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token
        return  str(new_access_token),'access token generated'
    except:
        return False,'invalid access token or expired'