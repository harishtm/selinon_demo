from django.urls import reverse
from settings.informationtooltip import InformationTooltip, TooltipItem


InformationTooltip.add_item(
    "Automation",
    TooltipItem(
        title='Automation',
        id='automation-tooltip',
        desc='This section contains automation'
    ),
)

InformationTooltip.add_item(
    "Automation",
    TooltipItem(
        title='List of Automations',
        id='list-of-automations-tooltip',
        desc='This section lists the automations available'
    ),
)
