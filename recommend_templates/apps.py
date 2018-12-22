# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RecommedTemplatesConfig(AppConfig):
    name = 'recommend_templates'

    def ready(self):
        import recommend_templates.signals
