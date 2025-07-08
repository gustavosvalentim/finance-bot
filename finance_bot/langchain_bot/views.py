from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from .tool_manager import ToolManager


@user_passes_test(lambda u: u.is_superuser)
def room(request):
    context = {
        'room_name': request.user.id
    }

    context['tools'] = [
        {
            'name': tool.name,
            'description': tool.description,
        }
        for tool in ToolManager.instance().load_tools([])
    ]

    return render(request, "langchain_chat/chat.html", context)
