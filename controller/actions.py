from core.utils import read_command, prn

from core.exceptions import ClientEx

from service.character import character_service
from service.room import room_service

async def actions(ws, user, data):
    if data["type"] == "me":        # Doing RP action
        pass
    if data["type"] == "drop":      # Drop something in the room
        pass
    if data["type"] == "take":      # Take something from the room
        pass
    if data["type"] == "give":      # Give something to someone
        pass
    if data["type"] == "whisper":   # Say something in private
        pass
    if data["type"] == "move":      # Move player to another room
        await character_service.move_character(ws, user, data)
    if data["type"] == "inventory": # Inspect inventory
        pass
    if data["type"] == "save":      # Save my character
        pass
    if data["type"] == "look":      # Look around the room
        await room_service.look_user_room(ws, user)
    if data["type"] == "say":       # Say something in public
        await prn(ws, user.name + " just said: " + str(data["content"]))
