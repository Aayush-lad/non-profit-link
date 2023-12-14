from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Org

from .models import Item
from .serializers import ItemSerializer


def search_items(request):
    return render(request, "search_items.html")


# post and put requests for the model
class PostPutItemApiView(APIView):
    # creates a new item
    def post(self, request):
        # getting the current user
        user = request.user
        org = Org.objects.get(username=user.username)

        # want is a singular value, makes user feedback on frontend simpler
        want = request.data.get("want")

        serializer_data = []
        # identifying which input to send an error to on the frontend
        input_ids = []

        # accepts a list of this data
        for item in request.data.get("needsPOSTRequest"):
            new_item = {
                "item_name": item["item_name"],
                "want": want,
                "units_description": item["units_description"],
                "count": item["count"],
                "input_id": item["input_id"],
                "org": org.id,  # type: ignore
            }
            serializer_data.append(new_item)

        serializer = ItemSerializer(data=serializer_data, many=True)  # type: ignore
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # TODO: figure out how to make this work
        serializer.errors[0] = 1
        print(serializer.errors)
        # list(zip(serializer.errors, input_ids))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # getting the current user
        user = request.user
        org = Org.objects.get(username=user.username)
        org_id = org.id  # type: ignore

        # dont include org_id in this data because that would be redundant
        edited_item = {
            "old_item_name": request.data.get("old_item_name"),
            "new_item_name": request.data.get("new_item_name"),
            "want": request.data.get("want"),
            "units_description": request.data.get("units_description"),
            "count": request.data.get("count"),
        }

        if not Item.objects.filter(
            org=org_id, item_name=edited_item["old_item_name"]
        ).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # if the object does exist, then
        Item.objects.filter(org=org_id, item_name=edited_item["old_item_name"]).update(
            item_name=edited_item["new_item_name"],
            want=edited_item["want"],
            units_description=edited_item["units_description"],
            count=edited_item["count"],
        )

        return Response(status=status.HTTP_200_OK)


# get and delete methods for the item model
class GetDeleteItemApiView(APIView):
    # returns selected item info
    def get(self, request, item_name):
        # getting the current user
        user = request.user
        org = Org.objects.get(username=user.username)
        org_id = org.id  # type: ignore

        item = get_object_or_404(Item, org=org_id, item_name=item_name)

        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_name):
        # getting the current user
        user = request.user
        org = Org.objects.get(username=user.username)
        org_id = org.id  # type: ignore

        # getting and deleting the item
        item = get_object_or_404(Item, org=org_id, item_name=item_name)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
