import subprocess
import sys
import os
import logging
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer, SearchSerializer
from .models import Search


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "healthy",
            "version": "1.0.0",
            "database": "connected" if Search.objects.exists() or True else "disconnected"
        })


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] #TODO Specify this

class SearchListCreate(generics.ListCreateAPIView):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Search.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class PubmedSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        searchterm = request.data.get("searchterm")
        mode = request.data.get("mode", "overview")
        email = request.user.email
        searchnumber = int(request.data.get("searchnumber", 10))
        sortby = request.data.get("sortby", "relevance")

        if not searchterm:
            return Response({"error": "Missing search term"}, status=status.HTTP_400_BAD_REQUEST)

        # Build CLI command
        cli_args = [
            sys.executable,
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cli/main.py')),
            f'"{searchterm}"',
            "-m", mode,
            "-e", email,
            "-n", str(searchnumber),
            "-s", sortby
        ]
        allowed_modes = {"overview", "emails"}
        allowed_sort = {"relevance", "pub_date", "Author", "JournalName"}
        if mode not in allowed_modes:
            return Response({"error": "Invalid mode"}, status=status.HTTP_400_BAD_REQUEST)
        if sortby not in allowed_sort:
            return Response({"error": "Invalid sort option"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = subprocess.run(
                cli_args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True
            )
            output = result.stdout
        except subprocess.CalledProcessError as e:
            logging.error("PubmedSearch subprocess error: %s", e.stderr or str(e))
            return Response({"error": "An internal error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the search to the database
        search_obj = Search(user=request.user, query=searchterm)
        search_obj.save()
        serializer = SearchSerializer(search_obj)

        return Response({
            "result": output,
            "search": serializer.data
        }, status=status.HTTP_200_OK)

