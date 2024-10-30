# mess_app/context_processors.py

def admin_status(request):
    return {
        'profile': request.user,  # Adjust this logic if needed
    }
