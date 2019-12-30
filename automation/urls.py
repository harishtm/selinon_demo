from django.urls import path
import automation.views as automationview 
urlpatterns = [
    path('automation_nodes', automationview.get_all_nodes, name='automation-nodes'),
    path('automation', automationview.atomation),
    path('saveautomation', automationview.save_automation, name='automation-save'),
    path('automation_editor/<int:pk>/', automationview.automation_editor, name='automation-editor'),
    path('getautomation', automationview.get_automation),
    path('listAutomations', automationview.list_automation),
    path('deleteAutomations', automationview.delete_automation),
]
