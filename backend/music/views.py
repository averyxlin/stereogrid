from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from django.utils import timezone

# ViewSets bundle CRUD operations (GET/POST/PUT/DELETE) into a single class
# ModelViewSet provides default implementations for all actions
# the default actions are: list, create, retrieve, update, partial_update, destroy
# these get overriden to customize the respone
class SongViewSet(viewsets.ModelViewSet):
    """
    - CRUD endpoints for Song model 
    - inherits from ModelViewSet which provides default CRUD operations

    APIs:
    - GET /songs/ - list all songs
    - GET /songs/<id>/ - retrieve a single song
    - POST /songs/ - create a new song
    - PUT /songs/<id>/ - update a song
    - DELETE /songs/<id>/ - delete a song
    """

    # queryset: defines which data to expose (all songs in this case)
    queryset = Song.objects.all().order_by('-created_at')
    serializer_class = SongSerializer # serializer class to convert model instances to JSON

    def list(self, request, *args, **kwargs):
        """
        - list endpoint: GET /songs/
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to list songs",
                "error": str(e),
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
            

    def retrieve(self, request, *args, **kwargs):
        """
        - retrieve endpoint: GET /songs/<id>/
        """
        try: 
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": serializer.data, 
                "links": {
                    "collection": request.build_absolute_uri('/songs/'),
                    "spotify": instance.spotify_url,
                },
                "timestamp": timezone.now().isoformat()
            }

            return Response(response, status=status.HTTP_200_OK)

        except Song.DoesNotExist:

            return Response({
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Song does not exist. Please check the ID.",
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to retrieve song",
                "error": str(e),
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        """
        - create endpoint: POST /songs/
        """ 
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Song created successfully",
                "data": serializer.data,
                "timestamp": timezone.now().isoformat()
            }

            headers = self.get_success_headers(serializer.data)
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create song",
                "error": str(e),
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def update(self, request, *args, **kwargs):
        """
        - update endpoint: PUT /songs/<id>/
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Song updated successfully",
                "data": serializer.data,
                "timestamp": timezone.now().isoformat()
            }

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to update song",
                "error": str(e),
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        - delete endpoint: DELETE /songs/<id>/
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            return Response({
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Song deleted successfully",
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_204_NO_CONTENT)
        
        except Song.DoesNotExist:
            return Response({
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Cannot delete song that does not exist. Please check the ID.",
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to delete song",
                "error": str(e),
                "timestamp": timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)