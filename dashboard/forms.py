from django import forms
from .models import *

class WhitelistForm(forms.ModelForm):
  class Meta:
        # specify model to be used
        model = Whitelist
  
        # specify fields to be used
        fields = [
          'wl_domain', 'wl_comment'
        ]
        labels = {
          'wl_domain': 'Domain',
          'wl_comment': 'Comment',
        }

  def __init__(self, *args, **kwargs):
        super(WhitelistForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class BlacklistForm(forms.ModelForm):
  class Meta:
        # specify model to be used
        model = Blacklist
  
        # specify fields to be used
        fields = [
          'bl_domain', 'bl_comment'
        ]
        labels = {
          'bl_domain': 'Domain',
          'bl_comment': 'Comment',
        }

  def __init__(self, *args, **kwargs):
        super(BlacklistForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProfileConfigForm(forms.ModelForm):
  class Meta:
    model = profileConfig

    fields = [
      'cat_status',
    ]
    