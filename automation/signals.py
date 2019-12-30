import django.dispatch

workflow_changed = django.dispatch.Signal(providing_args=["workflowSpec"])