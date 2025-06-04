from django import forms

from product.models import Category, Product, Review, ShippingAddress

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


# class ReviewForm(forms.ModelForm):
#     rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.Select())

#     class Meta:
#         model = Review
#         fields = ['rating', 'comment']
        

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'phone', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
        }