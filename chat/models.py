from django.db import models

from chat.aes import AESCipher


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    user = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    @property
    def decrypted_message(self):
        aes = AESCipher(self.room.key)
        return aes.decrypt(self.message)
