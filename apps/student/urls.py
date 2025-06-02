from django.urls import path
from . import views

urlpatterns = [
    # Placeholder URLs (will update with actual views later)
    path('apply/', views.ApplyForHostelView.as_view(), name='student_apply_hostel'),
    path('application-status/', views.ViewApplicationStatusView.as_view(), name='student_application_status'),
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('pay/', views.PayHostelFeeView.as_view(), name='student_pay_fee'),
    path('payments/', views.ViewPaymentHistoryView.as_view(), name='student_payment_history'),
    path('maintenance-request/', views.SubmitMaintenanceRequestView.as_view(), name='student_submit_maintenance'),
    path('maintenance-requests/', views.ViewMaintenanceRequestsView.as_view(), name='student_view_maintenance'),
    path('certificate/', views.DownloadHostelCertificateView.as_view(), name='student_download_certificate'),
] 