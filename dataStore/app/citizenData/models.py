from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, get_user_model, user_logged_in, user_logged_out
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import uuid
import os
from django import forms

from django.db import models

# def validate_image_size(value):
#     # Define the maximum allowed size in bytes (e.g., 2MB)
#     max_size = 2 * 1024 * 1024  # 2MB
#
#     if value.size > max_size:
#         raise ValidationError(f"Image size exceeds {max_size/1024/1024}MB. Please upload a smaller image."

def aadhar_image_upload_path(instance, filename):
    # Customize the local folder path as needed
    local_folder = 'uploads/aadhar_images'

    # Generate the full file path
    full_path = f"{local_folder}/{filename}"

    return full_path

# Define default image paths using callable functions
def default_front_page_image():
    return 'aadhar/default_front_page.jpg'

def default_back_page_image():
    return 'aadhar/default_back_page.jpg'


class LastFetchedRow(models.Model):
    row_number = models.IntegerField(default=1)

    def __str__(self):
        return f"Last Fetched Row: {self.row_number}"


class Citizen(models.Model):
    timestamp = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=255, null=True, blank=True)
    adhar = models.CharField(max_length=255, null=True, blank=True)
    epic = models.CharField(max_length=255, null=True, blank=True)
    no_response = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Citizen, self).save(*args, **kwargs)
