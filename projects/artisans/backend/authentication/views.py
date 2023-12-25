from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta

# This is the view logic for registering a user.
# We defined the class and it inherits from the APIView class.
class RegisterUserView(APIView):
    def post(self, request):  # We defined a post method that takes in a request from a user.
        # We defined a serializer variable that takes in the RegisterUserSerializer class and passes in the request data.
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # We are checking if the serializer is valid(we raise an exception if it is not valid).
        serializer.save()  # We save the serializer.
        return Response(serializer.data)  # We return the serializer data.

# This is the view logic for logging a user in.
class LoginUserView(APIView):
    def post(self, request): # We defined a post method that takes in a request from a user.
        email = request.data['email'] # We are getting the inputted email from the request data.
        password = request.data['password'] # We are getting the inputted password from the request data.
            
        # Let's check if the user exists in our database.
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
            
        # Let's check if the password is correct.
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        # Let's create a payload variable that takes in the user's id and the current time.
        payload = {
            'id':user.id,
            'exp':datetime.utcnow() + timedelta(minutes=60),
            'iat':datetime.utcnow()
        }

        # Let's create a token variable that takes in the payload and the secret key.
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        # We are setting the cookie to the token.
        response.set_cookie(key='jwt', value=token, httponly=True)

        # We are returning the response data and making sure it is in string format.
        response.data = {
            'jwt':token.encode('utf8')
        }
        return response

# This is the view logic to retrieve a user's data using the token.
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        # We are getting the payload from the token.
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        # We are getting the user from the payload.
        user = User.objects.filter(id=payload['id']).first()
        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)
    
# This is the view logic to logout a user.
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt') # We are deleting the cookie.

        # We are returning the response data with a success status message.
        response.data = {
            'message':'Logout is successful'
        }
        return response
    
# This is the logic for resetting a forgotten password.
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # We are getting the user from the email.
        user = User.objects.filter(email=serializer.data['email']).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        # Lets check if the passwords match.
        if serializer.data['new_password'] != serializer.data['confirm_password']:
            raise AuthenticationFailed('Passwords do not match!')
        
        # Let's set the new password.
        user.set_password(serializer.data['new_password'])
        user.save() # We are saving the user.
        return Response(
            {'message':'Password reset is successful!'}
        )