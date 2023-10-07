from django.shortcuts import render
from chat.models import Room, Message


def home_page_view(request):
    return render(request, "index.html")


def chat_page_view(request):
    room_name = request.POST.get("room_name")
    user = request.POST.get("user")

    if not all([room_name, user]):
        return render(
            request,
            "index.html",
            {
                "error": "Missing room name or user",
            },
        )

    room, _ = Room.objects.get_or_create(name=room_name)
    messages = Message.objects.filter(
        room=room,
    ).order_by("created_at")

    return render(
        request,
        "chat.html",
        {
            "room_name": room.name,
            "user": user,
            "messages": messages,
        },
    )
