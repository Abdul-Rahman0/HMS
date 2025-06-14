from django.contrib import admin
from .models import Room , GuestLog

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'type', 'capacity', 'status')
    list_filter = ('type', 'status')
    search_fields = ('room_number',)




from django import forms
class GuestLogForm(forms.ModelForm):
    class Meta:
        model = GuestLog
        fields = '__all__'
        widgets = {
            'check_in_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            
        }


@admin.register(GuestLog)
class GuestLogAdmin(admin.ModelAdmin):
    # form = GuestLogForm
    list_display = ('name', 'purpose', 'check_in_time', 'check_out_time', 'associated_student')
    search_fields = ('name', 'purpose', 'associated_student__user__username')
    list_filter = ('check_in_time', 'check_out_time')