from django.db import models


class KeyWordReviews(models.Model):
    """google評論關鍵字分析"""
    place_name = models.CharField(verbose_name='店內代號', max_length=20)
    date = models.DateField(verbose_name='評論日期')
    keywords = models.CharField(verbose_name='關鍵字', max_length=12)
    keywordCount = models.IntegerField(verbose_name='關鍵字次數')
    category_choices = (
        (True, '好評'),
        (False, '負評')
    )
    category = models.BooleanField(verbose_name='類別', choices=category_choices)


class ShopReviews(models.Model):
    place_id = models.CharField(max_length=100, null=True)
    place_name = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100, null=True)
    rating = models.IntegerField(null=True)
    other_ratings = models.CharField(max_length=255, null=True)
    review_text = models.TextField(null=True)
    published_date = models.DateField(null=True)
    response_from_owner_text = models.TextField(null=True)
    response_from_owner_ago = models.CharField(max_length=100, null=True)
    response_from_owner_date = models.DateField(null=True)
    review_likes_count = models.IntegerField(null=True)
    total_number_of_reviews_by_reviewer = models.IntegerField(null=True)
    total_number_of_photos_by_reviewer = models.IntegerField(null=True)
    is_local_guide = models.BooleanField(null=True)
    review_translated_text = models.TextField(null=True)
    response_from_owner_translated_text = models.TextField(null=True)

    class Meta:
        db_table = "shop_reviews"

class StoreList(models.Model):
    place_name = models.CharField(max_length=50)
    store_name = models.CharField(max_length=50)
    def __str__(self):
        return self.store_name
