from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status, filters
from rest_framework.response import Response

from tasks.permissions import IsOwnerOrReadOnly
from tasks.serializers import UserSerializer, TaskSerializer, LabelSerializer
from tasks.models import Task, Label
from tasks.filters import IsOwnerFilterBackend
from tasks.decorators import log_action, active_user_required


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('title')
    serializer_class = TaskSerializer
    filter_backends = [IsOwnerFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'description', 'completion_status']
    ordering_fields = ['owner']
    # IsOwnerOrReadOnly permission has turned obsolete after implementing IsOwnerFilterBackend, but I'll keep it anyway. 
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated] 

    @log_action('Create Task')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class LabelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows labels to be viewed or edited.
    """
    queryset = Label.objects.all().order_by('name')
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    filter_backends = [IsOwnerFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['owner']

    @active_user_required
    @log_action('Delete Label Attempt') # this could be more deterministic, but you get the idea
    def destroy(self, request, *args, **kwargs):
    # Implementation to delete an existing object
        if Task.objects.filter(label__id=kwargs['pk']).count() > 0:
            return Response({'error':'label has related tasks'}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().destroy(request, *args, **kwargs)
