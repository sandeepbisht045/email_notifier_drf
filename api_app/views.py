from django.contrib.auth import authenticate
from . models import Products,Certificates,Subscribe
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProductsAddSerializer,ProductsListAllSerializer
from utils.jwt_token import obtain_jwt,verify_jwt,generate_access_token
# -------------------------------------------------------------------------------------------------------------------

class ProductsAddListAll(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsListAllSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        status_,message = verify_jwt(request)
        if not status_:
            return Response({'data':{},
            "message": message,"status_code":status.HTTP_400_BAD_REQUEST},
             status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductsAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':{},'status':status.HTTP_200_OK,'message':'data created success'})
        return Response({'data': {},'status':status.HTTP_400_BAD_REQUEST,'message':'invalid data'})

class LoginAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        refresh,access,status_ = obtain_jwt(user)
        if not refresh:
            return Response({'data':{},"message": "Invalid credentials",
            "status_code":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data':{
            "refresh": refresh,
            "access": access},"status_code":status_
        }, status=status_)
       
class GetAccessToken(APIView):
    def post(self,request,*args,**kwargs):
        access_token ,message = generate_access_token(request)
        if access_token:
             return Response({
            
            'data':{"access": access_token},"status_code":status.HTTP_200_OK 
        }, status=status.HTTP_200_OK )

        return Response({"message": message,
            "status_code":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class ProductsRetrieveUpdateDestroyAPIView(APIView):
    def get(self,request, pk):
        try:
            products =Products.objects.get(pk=pk)
            serializer = ProductsListAllSerializer(products)
            return Response({'data': serializer.data,'status':status.HTTP_200_OK,'message':'data extracted success'})

        except:
            raise Response({'data':{},'status':status.HTTP_400_BAD_REQUEST,'message':'invalid id'})

  
    def put(self, request, pk):
        status_,message = verify_jwt(request)
        if not status_:
            return Response({
            "message": message,"status_code":status.HTTP_400_BAD_REQUEST})
        product = self.get_object(pk)
        serializer = ProductsAddSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':{},'status':status.HTTP_200_OK,'message':'data update success'})
        return Response({'data':{},'status':status.HTTP_400_BAD_REQUEST,'message':'data invalid'})

    def delete(self, request, pk):
        status_,message = verify_jwt(request)
        if not status_:
            return Response({
            "message": message,"status_code":status.HTTP_400_BAD_REQUEST})
        try:
            products =Products.objects.get(pk=pk)
            products.delete()
            return Response({'data':{},'status':status.HTTP_200_OK,'message':'data deleted success'})

        except:
            return Response({'data':{},'status':status.HTTP_400_BAD_REQUEST,'message':'invalid id'})
