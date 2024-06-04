from django import forms
from .models import KeyWordReviews  # 導入KeyWordReviews模型，表單就能與該模型進行互動

class KeyWordReviewsForm(forms.ModelForm):
    class Meta:
        # 指定KeyWordReviewsForm與KeyWordReviews模型相關聯
        model = KeyWordReviews
        # 指定需要在表單中出現的字段
        fields = ['keywords','keywordCount']
