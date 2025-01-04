from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, mixins
from posts.models import Posts
from posts.serializers.post_serializer import PostSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser)


class PostListCreateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Posts.objects.all()
    def get(self,request:Request,*args, **kwargs):
        # return self.list(request, *args, **kwargs)
        try:
            data = self.list(request, *args, **kwargs)
            if data.data:
                response = {'status': True, 'message': 'Success', 'data': data.data}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {'status': True, 'message': 'No posts found', 'data': []}
                return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': None}
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def post(self, request: Request, *args, **kwargs):
        try:
            # Ensure that request.data is not empty
            data = request.data
            if not data:
                response = {'status': False, 'message': 'No data provided', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            # Use self.create() to handle post creation
            post = self.create(request, *args, **kwargs)
            response = {'status': True, 'message': 'Success', 'data': post.data}
            return Response(data=response, status=status.HTTP_200_OK)


        except Exception as e:
            # Log the error message to help identify the issue
            print(f"Error during post creation: {str(e)}")
            response = {'status': False, 'message': 'Internal server error', 'data': None}
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class PostRetriveUpdateDeleteView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    
    def get(self, request: Request, *args, **kwargs):
        try:
            data = self.retrieve(request, *args, **kwargs)
            if data.data:
                response = {'status': True, 'message': 'Success', 'data': data.data}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {'status': False, 'message': f'{str(data.exception)}', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Posts.DoesNotExist:
            response = {'status': False, 'message': "Post not found.", 'data': None}
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': None}
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request: Request, *args, **kwargs):
        try:
            body = request.data
            if body:
                data = self.update(request, *args, **kwargs)
                if data.data:
                    response = {'status': True, 'message': 'Success', 'data': data.data}
                    return Response(data=response, status=status.HTTP_200_OK)
                else:
                    response = {'status': False, 'message': f'{str(data.exception)}', 'data': None}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': 'No data provided', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            if isinstance(e.args[0], dict):
                print(True)
                formatted_errors = []
                for field, errors in e.args[0].items():         
                        error_msg = [str(v) for v in errors]
                        error_message = f"{error_msg[0].lower().replace('this', f'{field}')}"
                        formatted_errors.append(error_message)
                response = {'status': False, 'message': ', '.join(formatted_errors), 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': str(e), 'data': None}
                return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def delete(self, request: Request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            response = {'status': True, 'message': 'Post deleted', 'data': None}
            return Response(data=response, status=status.HTTP_204_NO_CONTENT) 
        except Posts.DoesNotExist:
            response = {'status': False, 'message': "Post not found.", 'data': None}
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            if isinstance(e.args[0], dict):
                print(True)
                formatted_errors = []
                for field, errors in e.args[0].items():         
                        error_msg = [str(v) for v in errors]
                        error_message = f"{error_msg[0].lower().replace('this', f'{field}')}"
                        formatted_errors.append(error_message)
                response = {'status': False, 'message': ', '.join(formatted_errors), 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': str(e), 'data': None}
                return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    