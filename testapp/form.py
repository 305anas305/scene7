from django import forms

from testapp.models import CustomUser,blog




class signupform(forms.ModelForm):

    class Meta:
        model=CustomUser
        fields=['username','password','first_name','last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username
class blogform(forms.ModelForm):
    class Meta:
        model = blog
        fields = [ 'title','content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),

        }
