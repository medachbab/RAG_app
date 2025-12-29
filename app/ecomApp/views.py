from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer, UserSerializer
from .services import import_data_service  # Keep this
from django.contrib.auth.models import User

# User model
User = get_user_model()

# ---------------- USER VIEWS ----------------
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
            'is_active': user.is_active
        }
        return Response(user_data)

# ---------------- SOCIAL LOGIN ----------------
@login_required
def google_login_callback(request):
    user = request.user
    social_accounts = SocialAccount.objects.filter(user=user)
    social_account = social_accounts.first()
    if not social_account:
        return redirect('http://localhost:5173/login/callback/?error=NoSocialAccount')

    token = SocialToken.objects.filter(account=social_account, account__providers='google').first()
    if token:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return redirect(f'http://localhost:5173/login/callback/?access_token={access_token}')
    else:
        return redirect(f'http://localhost:5173/login/callback/?error=NoGoogleToken')

@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_access_token = data.get('access_token')
            if not google_access_token:
                return JsonResponse({'detail': 'Access Token is missing'}, status=400)
            return JsonResponse({'valid': True})
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

# ---------------- PRODUCT & CATEGORY VIEWS ----------------
@api_view(['GET'])
@permission_classes([AllowAny])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getProductsByCategory(request, category_name):
    category = Category.objects.filter(name=category_name).first()
    if not category:
        return Response({'error': 'Category not found'}, status=404)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_most_popular_products(request):
    top_rated_products = Product.objects.order_by('-rating')[:8]
    serializer = ProductSerializer(top_rated_products, many=True)
    return Response(serializer.data)

# ---------------- IMPORT DATA ----------------
@api_view(['GET'])
@permission_classes([AllowAny])
def import_data(request):
    result = import_data_service()
    return Response({"message": result})
