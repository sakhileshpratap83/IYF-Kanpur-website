from django import forms
from .models import Devotee_detail
class BlogPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget = forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = Devotee_detail
		fields = ['title','slug','content']