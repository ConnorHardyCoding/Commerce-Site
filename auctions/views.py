from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.validators import DecimalValidator

from .models import *

class CreateForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
                                    'class':'form-control',
                                    'style': "width: 60%; height: 20vh; min-width: 500px;",
                                    'placeholder': 'Enter description here'}),                                                                                      
                                  initial="Enter desciption here")
    category = forms.ModelChoiceField(label="Choose item category:",
                                      widget=forms.Select(attrs={'class':'form-control','style':'color: #636c72'}),
                                      queryset=Category.objects.all(),
                                      empty_label="Select a category",)
    starting_bid = forms.DecimalField(validators=[DecimalValidator], decimal_places=2, widget=forms.NumberInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Starting bid',
                                    'step': '0.1',
                                    'min': '0'}),
                                    initial="Enter starting bid")
    image_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Image url'}))

def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        message = ""
        if 'next' in request.GET:
            message = "Login required to create listing"
        return render(request, "auctions/login.html", {
            "message": message
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create(request):
    form = CreateForm(request.GET)
    return render(request, "auctions/create.html", {
        "form": form
    })