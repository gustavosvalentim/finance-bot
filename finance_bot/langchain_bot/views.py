from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.conf import settings


@user_passes_test(lambda u: u.is_superuser)
def room(request):
    try:
        # Create context with room name and tools
        context = {
            'room_name': str(request.user.id),
            'tools': [
                {
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                }
                for tool in settings.AGENT_SETTINGS.get('tools', [])
            ]
        }
        
        return render(request, "langchain_chat/chat.html", context)
        
    except Exception as e:
        # Log the error and return an error page or message
        return render(request, "error.html", {
            'error_message': f"Failed to initialize chat: {str(e)}"
        }, status=500)
