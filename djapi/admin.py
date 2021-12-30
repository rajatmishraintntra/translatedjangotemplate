from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers,status,response
from django_restful_admin import admin,RestFulModelAdmin
from django.contrib.auth.models import User
# Register your models here.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class DiffData(User):
    class Meta:
        proxy=True


@admin.register(User)
class UserModelAdmin(RestFulModelAdmin):# overriding permissions
    serializer_class = ProductSerializer
    single_serializer_class=ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

@admin.register(DiffData)
class UseModelAdmin(RestFulModelAdmin):# overriding Serializer and methods and custom actions
    serializer_class = ProductSerializer
    single_serializer_class=ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self,request):
        serializer = self.get_single_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.log_addition(request, serializer.instance, [{'added': {
            'name': str(serializer.instance._meta.verbose_name),
            'object': str(serializer.instance),
        }}])
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @admin.action(permission=AllowAny, detail=True, methods=['PUT'], url_path=r'update_email')  
    def update_email(self, request, pk=None, **kwargs):
        return super().partial_update(request,pk=pk,**kwargs)