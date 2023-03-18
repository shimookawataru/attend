from django import forms
from .models import SubmitAttendance, SubmitError, SubmitForget

class SubmitAttendanceForm(forms.ModelForm):

    class Meta:
        model = SubmitAttendance
        widgets = {
            'in_out': forms.RadioSelect()
        }
        fields = ('in_out',)

class SubmitErrForm(forms.ModelForm):

    class Meta:
        model = SubmitError
        widgets = {
            'err_cause': forms.RadioSelect()
        }
        fields = ('err_cause', )


class SubmitForgetForm(forms.ModelForm):
    date_time_forget = forms.DateTimeField(
        input_formats = ['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )
    class Meta:
        model = SubmitForget
        fields = ('date_time_forget',)
    