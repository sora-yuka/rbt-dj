from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from .models import OfferModel
from .serializers import OfferReadSerializer, OfferWriteSerializer
from .permissions import IsOwnerOrReadOnly


class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self) -> OfferModel:
        if self.action == "retrieve":
            return (
                OfferModel.objects.all()
                .select_related("category", "owner")
                .prefetch_related("media")
            )
        return (
            OfferModel.objects.filter(status="ACTIVE")
            .select_related("category", "owner")
            .prefetch_related("media")
        )

    def get_serializer_class(self) -> OfferReadSerializer | OfferWriteSerializer:
        if self.action in ["list", "retrieve"]:
            return OfferReadSerializer
        return OfferWriteSerializer

    def perform_create(self, serializer: OfferWriteSerializer) -> None:
        serializer.save(owner=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_instance = serializer.save(owner=self.request.user)
        read_serializer = OfferReadSerializer(
            offer_instance, context=self.get_serializer_context()
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        read_serializer = OfferReadSerializer(updated_instance, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_200_OK)


class MyOffersListView(ListAPIView):
    serializer_class = OfferReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            OfferModel.objects.filter(owner=self.request.user)
            .select_related("category", "owner")
            .prefetch_related("media")
        )
