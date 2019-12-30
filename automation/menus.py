from django.urls import reverse
from settings.adminmenus import AdminMenu, AdminMenuItem

AdminMenu.add_item("Automation_list", 
    AdminMenuItem("Actions", "#", slug='automation_actions', target='#', 
        children = [
            AdminMenuItem("Delete","#", slug='deleteautomation', target='#automationactiondelete'), 
            ], header=True ))