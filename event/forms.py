from django import forms
from .models import CustomUser, Questions, Special


class CustomUserSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'contact', 'password')



class EventAnswerForm(forms.Form):
    CHOICES = [(1, 'A'),
               (2, 'B'),
               (3, 'C'),
               (4, 'D'), ]
    user_answer = forms.ChoiceField(choices=CHOICES)

    def validate(self,ID):
        actual = Questions.objects.get(number=ID).answer
        user = self.cleaned_data['user_answer']
        if int(actual) == int(user):
            return 1
        else:
            return 0

class SpecialAnswerForm(forms.Form):

    user_answer = forms.CharField(max_length=200)

    def validate(self):
        actual = Special.objects.all()
        actual_answer = actual[0].answer
        print(actual_answer)
        user = self.cleaned_data['user_answer']
        print(user)
        if actual_answer is user:
            return 1
        else:
            return 0
