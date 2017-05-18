from django.apps import AppConfig
from django.conf import settings
from pyeureka import SimpleEurekaServiceWrapper


class EndpointsConfig(AppConfig):
    name = 'endpoints'

    def ready(self):
        service = SimpleEurekaServiceWrapper(settings.EUREKA['url'], settings.EUREKA[
                                             'instance'], settings.EUREKA['heartbeat'])
        service.run()
