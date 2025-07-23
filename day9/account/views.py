from django.shortcuts import render
from .models import MyModel
from django.http import JsonResponse

async def my_view(request):
    # Use aiterator for async iteration
    items = []
    async for item in MyModel.objects.all().aiterator():
        items.append({
            "id": item.id,
            "name": item.name,
            "email": item.email,
            "created_at": item.created_at.isoformat()
        })

    # Create a new object asynchronously
    await MyModel.objects.acreate(name="New Object", email="new@example.com")

    # Get the latest object asynchronously
    latest_obj = await MyModel.objects.alatest("created_at")
    
    if latest_obj is None:
        
        return JsonResponse({"status": "error", "message": "No objects found"}, status=404)
    print(f"Latest object: {latest_obj.name},\nEmail: {latest_obj.email},\ncreated at: {latest_obj.created_at}")
    # Delete the latest object
    
    await latest_obj.adelete()

    return JsonResponse({"status": "success", "data": items})

from django.views import View
from django.http import JsonResponse

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name='dispatch')
class MyView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        return JsonResponse({
            "status": "success",
            "message": f"Class view accessed with id: {id}"
        })
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        return JsonResponse({
            "status": "success",
            "message": "Post request received",
            "data": {"id": id}
        })