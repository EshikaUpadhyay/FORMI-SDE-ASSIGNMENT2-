from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import find_nearest_properties

@api_view(['GET'])
def nearest_property_view(request):
    query = request.data.get('query', '')
    if not query:
        return Response({"error": "Query parameter is required."}, status=400)

    matches = find_nearest_properties(query)
    if matches:
        return Response({"properties": matches})
    return Response({"message": "No properties found within 50 km radius."})