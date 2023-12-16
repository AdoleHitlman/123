from django.contrib.auth import authenticate, login
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserSerializer
from .models import Habit
from .paginators import HabitPagination
from .permissions import IsOwnerOrReadOnly, IsPublicOnly
from .serializers import HabitSerializer


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Habit.objects.filter(is_public=True)
    serializerclass = HabitSerializer
    permissionclasses = IsPublicOnly


@method_decorator(csrf_exempt, name='dispatch')
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsPublicOnly]
    pagination_class = HabitPagination

    def list(self, request, **kwargs):
        habits = Habit.objects.all()
        paginator = Paginator(habits, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serialized_habits = serializers.serialize('json', page_obj)

        return JsonResponse(serialized_habits, safe=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_habits(self, request):
        habits = Habit.objects.filter(user=request.user)
        paginator = Paginator(habits, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = HabitSerializer(page_obj, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = HabitSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
