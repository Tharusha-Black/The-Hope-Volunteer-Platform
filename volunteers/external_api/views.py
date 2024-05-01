from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from volunteer_oppertunities.models import VolantProjects
from .serializers import EventSerializer

class EventListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Retrieve all Events from the database
        events = VolantProjects.objects.all()

        # Serialize the Events data
        serializer = EventSerializer(events, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data)