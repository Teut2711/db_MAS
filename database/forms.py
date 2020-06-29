from django import forms


class NSDLForm(forms.Form):
    filepath = forms.FileField(widget=forms.FileInput(
        attrs={"accept": "*.txt"}), label="Select File :")
