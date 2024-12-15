from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Posts
from posts.serializers.post_serializer import PostSerializer

from django.shortcuts import get_object_or_404

@api_view(http_method_names=['GET', 'POST'])
def getOrCreatePosts(request:Request):
    if request.method == "POST":
        try:
            data = request.data
            if data:
                serializer = PostSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    response = {'status': True, 'message': 'Post created', 'data': serializer.data}
                    return Response(data=response, status=status.HTTP_201_CREATED)
                else:
                    formatted_errors = ''
                    print(serializer.errors)
                    for field, errors in serializer.errors.items():
                        formatted_errors = f"{errors[0].lower().replace('this', f'{field}')}"
                    response = {'status': False, 'message': formatted_errors, 'data': None}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': 'No data provided', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    
    else:  # Handling GET requests
        try:
            data = Posts.objects.all()
            if data.exists():
                serializer = PostSerializer(data, many=True)
                response = {'status': True, 'message': 'Success', 'data': serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {'status': True, 'message': 'No posts found', 'data': []}
                return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': []}
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['GET'])
def getSinglePost(request: Request, post_id:int):
    if post_id is None:
        response = {'status': False, 'message': 'Post ID is required.', 'data': None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    try:
        # data = Posts.objects.get(id=post_id)
        data = get_object_or_404(Posts, pk=post_id)
        serializer = PostSerializer(data)
        response = {'status': True, 'message': 'Success', 'data': serializer.data}
        return Response(data=response, status=status.HTTP_200_OK)
    except Posts.DoesNotExist:
        response = {'status': False, 'message': "Post not found.", 'data': None}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {'status': False, 'message': str(e), 'data': None}
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def updatePost(request: Request, post_id: int):
    try:
        post = get_object_or_404(Posts, pk=post_id)
        body = request.data
        if body:
            serializer = PostSerializer(post, data=body, partial=True)
            unexpected_fields = set(body.keys()) - set(serializer.fields.keys())
            if unexpected_fields:
                response = {
                    'status': False,
                    'message': f"Unexpected fields: {', '.join(unexpected_fields)}",
                    'data': None
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                response = {'status': True, 'message': 'Success', 'data': serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                formatted_errors = []
                for field, errors in serializer.errors.items():
                    error_message = f"{errors[0].lower().replace('this', f'{field}')}"
                    formatted_errors.append(error_message)

                response = {'status': False, 'message': ', '.join(formatted_errors), 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'status': False, 'message': 'No data provided', 'data': None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        response = {'status': False, 'message': str(e), 'data': None}
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
    
    
@api_view(http_method_names=['DELETE'])
def deletePost(request: Request, post_id:int):
    if post_id is None:
        response = {'status': False, 'message': 'Post ID is required.', 'data': None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    try:
        data = get_object_or_404(Posts, pk=post_id)
        data.delete()
        response = {'status': True, 'message': 'Post deleted', 'data': None}
        return Response(data=response, status=status.HTTP_204_NO_CONTENT) 
    except Posts.DoesNotExist:
        response = {'status': False, 'message': "Post not found.", 'data': None}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {'status': False, 'message': str(e), 'data': None}
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)