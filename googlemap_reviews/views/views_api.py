from django.shortcuts import render, redirect
from django.db.models import F, Avg
# 將資料解析為「共通格式」Json, 並回傳至Web(讓前端可以使用)
from django.http import JsonResponse
# 資料表
from googlemap_reviews.models import ShopReviews, KeyWordReviews,StoreList
from datetime import datetime, timedelta

"""
    TODO:Api
    1. 查詢店家關鍵字資料(獨立一張資料表)
    2. 查詢好/負評關鍵字統計資料
    3. 統計資料
    4. 用戶的好評與負評

"""


def get_shop_keywords(request):
    """
    獲取關鍵字正負評,並整理成api

    Returns:
        Json: _description_
    """
    if request.method == "GET":
        # 取得date變數, 未傳值則預設為今天日期
        date_str = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
        # 轉換為date類型
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 計算當月第一天和最後一天
        first_day_of_month = date.replace(day=1)
        last_day_of_month = (first_day_of_month +
                             timedelta(days=32)).replace(day=1)

        # 找尋指定的place_name, 預設為P1
        place_name = request.GET.get("place_name", "屏東民生")
        category = request.GET.get("category")
        # 根據category過濾評論
        # 修改查詢已過濾當月的所有評論
        result_positive = KeyWordReviews.objects.filter(
            date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            category=True
        ).values("place_name", "date", "keywords", "keywordCount")

        result_negative = KeyWordReviews.objects.filter(
            date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            category=False
        ).values("place_name", "date", "keywords", "keywordCount")

        response_date = {
            'positive': list(result_positive),
            'negative': list(result_negative),
        }

        return JsonResponse(response_date, safe=False)


def reviews_data(request):
    if request.method == "GET":
        # 取得date變數, 未傳值則預設為今天日期
        date_str = request.GET.get(
            "published_date", datetime.now().strftime("%Y-%m-%d"))
        # 轉換為date類型
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 計算當月第一天和最後一天
        first_day_of_month = date.replace(day=1)
        last_day_of_month = (first_day_of_month +
                             timedelta(days=32)).replace(day=1)

        # 找尋指定的place_name, 預設為P1
        place_name = request.GET.get("place_name", "屏東民生")

        rating = request.GET.get("rating")

        result_positive_text = (ShopReviews.objects.filter(
            published_date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            rating__gte=4,  # 大於等於
            review_text__isnull=False,  # 過濾文本為空值
            review_text__gt="",  # 過濾文本為空字符串
        )
            # rename
            .annotate(
                # store_id=F("place_name"),
                date=F("published_date"),
        )
            # 取出需要的欄位
        ).values("place_name", "date", "user_name", "review_text")

        result_negative_text = (ShopReviews.objects.filter(
            published_date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            rating__lte=3,  # 小於等於
            review_text__isnull=False,  # 過濾文本為空值
            review_text__gt="",  # 過濾文本為空字符串
        )
            # rename
            .annotate(
                # store_id=F("place_name"),
                date=F("published_date")
        )
        ).values("place_name", "date", "user_name", "review_text")
        response_data = {
            'positive': list(result_positive_text),
            'negative': list(result_negative_text)
        }

        return JsonResponse(response_data, safe=False)

def get_storelist(request):
    store_names = StoreList.objects.values_list('store_name',flat=True)
    place_name = StoreList.objects.values_list('place_name',flat=True)
    stores = list(StoreList.objects.all())
    # 定義排序順序
    sort_order = ['屏東', '高雄', '台南', '嘉義', '雲林', '台中', '新竹', '桃園']
    # 自定義排序
    stores.sort(key=lambda x: sort_order.index(x.store_name[:2]) if x.store_name[:2] in sort_order else len(sort_order))

    response_data = {
        'options': [
            {'label': store.store_name, 'value': store.place_name} for store in stores
        ]
    }
    return JsonResponse(response_data,safe=False)

def statistic_card(request):
    if request.method == "GET":
        place_name = request.GET.get("place_name", "屏東民生")
        # 計算rating平均值, 儲存於字典中
        avg_curRating = ShopReviews.objects.filter(place_name=place_name).aggregate(Avg('rating'))
        # 從字典中提取平均值
        curRating = avg_curRating.get('rating__avg')
        totalPositiveReviews = ShopReviews.objects.filter(place_name=place_name,rating__gte=4).count()
        totalNegativeReviews = ShopReviews.objects.filter(place_name=place_name,rating__lte=3).count()

        response_data = {
            'curRating':curRating,
            'totalPositiveReviews':totalPositiveReviews,
            'totalNegativeReviews':totalNegativeReviews,
        }
        return JsonResponse(response_data,safe=False)

def statistic_footer(request):
    if request.method == 'GET':
        place_name = request.GET.get('place_name','屏東民生')
        date_str = request.GET.get(
            "published_date", datetime.now().strftime("%Y-%m-%d"))
        # 轉換為date類型
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 計算當月第一天和最後一天
        first_day_of_month = date.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1)
        newPositiveReviewsThisMonth = ShopReviews.objects.filter(
            published_date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            rating__gte=4,).count()
        newNegativeReviewsThisMonth = ShopReviews.objects.filter(
            published_date__range=(first_day_of_month, last_day_of_month),
            place_name=place_name,
            rating__gte=3,).count()
        response_data ={
            'newPositiveReviewsThisMonth':newPositiveReviewsThisMonth,
            'newNegativeReviewsThisMonth':newNegativeReviewsThisMonth
        }
        return JsonResponse(response_data,safe=False)