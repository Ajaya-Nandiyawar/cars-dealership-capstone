from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Dealer, CarMake
from .serializers import DealerSerializer, CarMakeSerializer


class DealerListView(APIView):
    """
    Retrieve all dealerships or filter dealerships by state.
    Supports path param or query parameter: ?state=Kansas (case-insensitive)
    """

    def get(self, request, state=None):
        state_param = state or request.query_params.get("state")
        queryset = Dealer.objects.all()

        if state_param:
            # Case-insensitive state filtering (matches 'Kansas', 'kansas', 'KANSAS', etc.)
            queryset = queryset.filter(state__iexact=state_param.strip())

        serializer = DealerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealerDetailView(APIView):
    """
    Retrieve a specific dealership by ID.
    """

    def get(self, request, dealer_id):
        dealer = get_object_or_404(Dealer, pk=dealer_id)
        serializer = DealerSerializer(dealer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealerByStateView(APIView):
    """
    Direct path route for state filtering: /api/dealers/state/<state>/
    """

    def get(self, request, state):
        dealers = Dealer.objects.filter(state__iexact=state.strip())
        serializer = DealerSerializer(dealers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarMakeListView(APIView):
    """
    Retrieve all car makes along with their associated models.
    Supports both direct array and Coursera {"CarMakes": ..., "CarModels": ...} format.
    """

    def get(self, request):
        makes = CarMake.objects.prefetch_related("models").all()
        serializer = CarMakeSerializer(makes, many=True)

        # If requested via Coursera get_cars endpoint, return dictionary with CarMakes and CarModels
        if "djangoapp" in request.path or "get_cars" in request.path or "fetchCars" in request.path:
            from .models import CarModel
            car_models = CarModel.objects.select_related("car_make").all()
            cars = [
                {"CarModel": m.name, "CarMake": m.car_make.name}
                for m in car_models
            ]
            return Response(
                {
                    "CarMakes": serializer.data,
                    "CarModels": cars,
                    "status": 200,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
