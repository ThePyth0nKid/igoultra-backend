# api/v1/user/views.py

from django.http import JsonResponse

def test_user_view(request):
    return JsonResponse({"message": "User route works ✅"})
