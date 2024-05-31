from django.shortcuts import render, HttpResponse,redirect
from googlemap_reviews import models
from ..forms import KeyWordReviewsForm

def googlemap_reviews(request):
    KeyWordReviews = models.KeyWordReviews.objects.all()
    return render(request,'googlemap_reviews.html',{'KeyWordReviews':KeyWordReviews})

# Create your views here.
