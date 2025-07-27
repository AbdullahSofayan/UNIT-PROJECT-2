from django import forms
from .models import MenuItem, MenuCategory, MenuItemOption

class MenuItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=MenuCategory.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Category",
        required=True,
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'calories','category',  'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        if shop:
            self.fields['category'].queryset = MenuCategory.objects.filter(shop=shop)


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }



class MenuItemOptionForm(forms.ModelForm):
    class Meta:
        model = MenuItemOption
        fields = ['name', 'extra_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option name (e.g., Add Cheese)'
            }),
            'extra_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Extra price (e.g., 2.00)'
            }),
        }
