from cqrs.container.dependency_injector import DependencyInjectorCQRSContainer
from cqrs.mediator import RequestMediator
from cqrs.requests import bootstrap

from .container import Container
from .mappers import map_commands, map_domain_events


def build_mediator() -> RequestMediator:
    di_container = DependencyInjectorCQRSContainer()
    di_container.attach_external_container(Container())

    return bootstrap.bootstrap(
        di_container=di_container,
        commands_mapper=map_commands,
        domain_events_mapper=map_domain_events,
    )
