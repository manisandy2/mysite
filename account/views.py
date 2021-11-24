from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import generics

from .forms import RegistrationForm
from .models import CustomUser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import RegistrationSerializers,CustomUserSerializers,ChangePasswordSerializer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import login
from rest_framework.authtoken.models import Token

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer



def home_page(request):
    name = request.user
    return render(request,"index.html",{"nm":name})


# Create your views here.
def registration(request):
    if request.method == "POST":
        user = RegistrationForm(request.POST)
        if user.is_valid():
            messages.info(request,"Registration is successfully")
            user.save()
            return HttpResponseRedirect('/')
    else:
        user = RegistrationForm()
    return render(request,"RegistrationForm.html",{'usr':user})


@api_view(['POST'])
def registration_api(request):
    if request.method == 'POST':
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            messages.info(request,"Registration is successfully")
            serializer.save()
            response = {
                'status':status.HTTP_201_CREATED,
                'message': 'Registration successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# def token_key(request):
#     token = AuthToken.objects.create(request.user)
#     print(token)
#     return HttpResponseRedirect("/")


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request,template_name="LoginForm.html",context={"form": form})


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_api(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    response = {
        'message':"login successfully",
        'status':status.HTTP_200_OK,
        'token': token.key
    }
    
    return Response(response)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect("/")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')



@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        user = CustomUser.objects.all()
        serializer = CustomUserSerializers(user, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CustomUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializers(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomUserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# def login_page(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return HttpResponseRedirect('/')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = AuthenticationForm()
#     return render(request=request,template_name="LoginForm.html",context={"form": form})
#
#
# def logout_page(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return HttpResponseRedirect("/")