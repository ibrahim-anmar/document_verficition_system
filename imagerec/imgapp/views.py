
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageUploadSerializer
import os
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import cv2
from skimage.metrics import structural_similarity as ssim
import base64
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate


class RegisterView(APIView):   #to handle user registration
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):      #to handle user login
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            # User is authenticated, create a token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            # Invalid credentials
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class LogoutAPIView(APIView):        #to handle user logout 
    def post(self, request):
        # Clear session or token associated with the user's authentication
        request.session.flush()  # For session authentication
        # For TokenAuthentication, you may revoke or delete the token associated with the user
        # For example: request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)



# class TestLoggedIn(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": "You are logged in."}, status=200)




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = BASE_DIR.replace("\imagerec","")
global IMG_DIR
global MATCH_DIR

class UploadImageView(APIView):
    authentication_classes = [SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            image = serializer.validated_data['image']
            image_path = os.path.join('C:/Users/ALMWUSHOOR/Desktop/signtures/', image.name)

            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

            matching_image_data = get_matchedImage_data_from_path(BASE_DIR + "/myimgs/1.jpg")
            global IMG_DIR
            IMG_DIR = os.path.join(BASE_DIR, 'signtures/', image.name)
            global MATCH_DIR
            MATCH_DIR = os.path.join(BASE_DIR, 'myimgs/1.jpg')
            return Response({
                'message': 'Image uploaded and processed successfully!',
                'yourImage': image_data,
                'matchingImage': matching_image_data
            }, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_matchedImage_data_from_path(image_path):
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    return image_data

def image_processing(image_path, matching_image_data):
    img1 = cv2.imread(image_path)
    img2 = cv2.imread(matching_image_data)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    similarity_value = ssim(img1, img2)
    return similarity_value

class SimilarityCheckView(APIView):
    def post(self, request, format=None):
        global IMG_DIR
        global MATCH_DIR

        similarity_value = image_processing(IMG_DIR, MATCH_DIR)

        if similarity_value < 65:
            return Response({'message': 'Signture are similar!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Signture are not similar!'}, status=status.HTTP_200_OK)








#an example of how to set the front end , could be removed OR replaced with your own front-end, removing this home page and the index.html file does not imapct the back-end processes
def home(request):
    #sqlite instrection
    return render(request,"index.html")
def login(request):
    return render(request,"login.html")
def register(request):
    return render(request,"register.html")














