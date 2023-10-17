from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

from .viewModel import Role
from .viewSerializer import RoleSerializer
from django.http import JsonResponse
        
class RoleList(APIView):
    @swagger_auto_schema(responses={200: 'Success'})
    def get(self, request):
        roles = Role.objects.all()
        role_list = []
        for role in roles:

            role_data = {
                'id':role.id,
                'name': role.name,
            }
            
            role_list.append(role_data)

        return JsonResponse({'roles':role_list}, safe=False)
class RoleDelete(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    name='id',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_STRING,
                    required=True,
                    description='Role ID'
                ),
            ],
            responses={200: 'Success', 404:'Role not found'}
    )
    def delete(self, request):
         role_id = request.query_params.get('id')
         if role_id:
            try:
                role= Role.objects.get(id=role_id)
                role.delete()
                return Response('Role deleted', status=200)
            except Role.DoesNotExist:
                return Response('Role not found', status=404)
         else:
            return Response('Role ID not provided', status=400)

class RoleUpdate(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Role Name'),
            },
        ),
        responses={200: 'Success', 400: 'Invalid Request', 404: 'Role not found'}
    )
    def put(self, request, role_id):  # Add role_id as a parameter here
        try:
            role = Role.objects.get(id=role_id)
            for key, value in request.data.items():
                if key != 'id' and key in role.__dict__:
                    setattr(role, key, value)
            role.modified_date_time = datetime.now()
            role.save()
            return Response('Role updated', status=200)
        except Role.DoesNotExist:
            return Response('Role not found', status=404)


class RoleCreate(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name':openapi.Schema(type=openapi.TYPE_STRING, description='Role Name'),
            },
        ),
        responses={200: 'Success', 400:'Invalid Request'}
    )
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Success', status=200)
        return Response(serializer.errors, status=400)
    
