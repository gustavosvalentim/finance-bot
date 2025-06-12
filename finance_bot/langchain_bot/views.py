from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

@user_passes_test(lambda u: u.is_superuser)
def room(request):
    return render(request, "langchain_chat/chat.html", { "room_name": request.user.id })
