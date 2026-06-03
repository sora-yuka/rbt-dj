from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request

from apps.offers.models import Status as OfferStatus
from .models import OfferDealModel, DealStatus, OfferModel
from .serializers import DealReadSerializer, DealWriteSerializer


class OfferDealViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            OfferDealModel.objects.all()
            .select_related(
                "initiator",
                "responder",
                "initiator_offer",
                "responder_offer",
                "initiator_offer__category",
                "responder_offer__category",
            )
            .prefetch_related("initiator_offer__media", "responder_offer__media")
        )

    def get_serializer_class(self) -> DealReadSerializer | DealWriteSerializer:
        if self.action in ["list", "retrieve"]:
            return DealReadSerializer
        return DealWriteSerializer

    def perform_create(self, serializer: DealWriteSerializer) -> None:
        responder_offer = serializer.validated_data["responder_offer"]
        serializer.save(initiator=self.request.user, responder=responder_offer.owner)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        responder_offer = serializer.validated_data["responder_offer"]

        deal_instance = serializer.save(
            initiator=request.user, responder=responder_offer.owner
        )
        read_serializer = DealReadSerializer(
            deal_instance, context=self.get_serializer_context()
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def accept(self, request: Request, pk: str = None) -> Response:
        deal = self.get_object()

        if request.user != deal.responder:
            return Response(
                {"detail": "Only the receiving party can accept this proposal."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if deal.status != DealStatus.PROPOSED:
            return Response(
                {
                    "detail": "This deal cannot be accepted from its current phase state."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            deal.status = DealStatus.ACCEPTED
            deal.completed_at = timezone.now()
            deal.save(update_fields=["status", "completed_at"])

            deal.initiator_offer.status = OfferStatus.TRADED
            deal.responder_offer.status = OfferStatus.TRADED
            deal.initiator_offer.save(update_fields=["status"])
            deal.responder_offer.save(update_fields=["status"])

        return Response(DealReadSerializer(deal).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request: Request, pk: str = None) -> Response:
        deal = self.get_object()

        if request.user != deal.responder:
            return Response(
                {"detail": "Only the receiving party can execute this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if deal.status != DealStatus.PROPOSED:
            return Response(
                {"detail": "This proposal is no longer in an open pending state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deal.status = DealStatus.REJECTED
        deal.save(update_fields=["status"])

        return Response(DealReadSerializer(deal).data, status=status.HTTP_200_OK)


class PublicPlatformAnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        total_active_listings = OfferModel.objects.filter(status="ACTIVE").count()

        deal_stats = OfferDealModel.objects.aggregate(
            total_completed=Count("id", filter=Q(status=DealStatus.ACCEPTED)),
            total_proposed=Count("id", filter=Q(status=DealStatus.PROPOSED)),
        )

        return Response(
            {
                "active_listings_count": total_active_listings,
                "successful_trades_count": deal_stats["total_completed"] or 0,
                "pending_proposals_count": deal_stats["total_proposed"] or 0,
            }
        )


class PrivateUserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        user = request.user

        total_my_offers = OfferModel.objects.filter(owner=user).count()

        my_total_deals = OfferDealModel.objects.filter(
            Q(initiator=user) | Q(responder=user)
        ).count()

        my_successful_deals = OfferDealModel.objects.filter(
            Q(initiator=user) | Q(responder=user), status=DealStatus.ACCEPTED
        ).count()

        proposed_by_me = OfferDealModel.objects.filter(initiator=user).count()
        received_by_me = OfferDealModel.objects.filter(responder=user).count()

        return Response(
            {
                "username": user.username,
                "my_total_items_posted": total_my_offers,
                "my_total_trade_interactions": my_total_deals,
                "completed_swaps": my_successful_deals,
                "negotiation_balance": {
                    "proposals_sent": proposed_by_me,
                    "proposals_received": received_by_me,
                },
            }
        )
