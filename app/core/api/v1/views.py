import logging

from health_check.views import MainView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger("project")


class HealthAPIView(MainView, APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR if self.errors else status.HTTP_200_OK
        response = self.render_to_response_json(self.plugins, status_code)
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.info(f"Django health check response: {response.content}")

        return Response(status=response.status_code)
