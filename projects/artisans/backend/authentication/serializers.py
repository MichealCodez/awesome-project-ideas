from rest_framework import serializers
from django.contrib.auth.models import User


# This is the serializer class for registering a user.
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # We defined the model to be the User model(default django User model).
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']  # Fields we need to register a user.

        # This code snippet is used to make the password field write only(not among user's data that'll be returned) for security reasons.
        extra_kwargs = {
            'password':{'write_only':True}
        }

    # Let us hash the password for security reasons.
    def create(self, validated_data):
        password = validated_data.pop('password', None) # We are getting the password from the validated data.
        instance = self.Meta.model(**validated_data) # We are creating an instance of the User model with the validated data.
        if password is not None:
            instance.set_password(password) # We are hashing the password here.
            instance.save() # We are saving the instance.
            return instance # We are returning the instance.

# This second serializer class is for resetting a forgotten password using the email field.
class ResetPasswordSerializer(serializers.Serializer):
    user = User
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(max_length=68, required=True)
    confirm_password = serializers.CharField(max_length=68, required=True)
