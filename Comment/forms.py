from django.forms import ModelForm
from .models import Floor, Point, Article, WelcomeImage


class RenewFloorModelForm(ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'


class RenewPointModelForm(ModelForm):
    class Meta:
        model = Point
        fields = '__all__'


class RenewArticleModelForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class RenewWelcomeImageModelForm(ModelForm):
    class Meta:
        model = WelcomeImage
        fields = '__all__'
