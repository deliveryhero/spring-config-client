import os

from spring_config_client.conf.resolver import Resolver
from spring_config_client.functional import LazyObject, empty
from config import ConfigClient
from requests.auth import HTTPBasicAuth


class Settings(LazyObject):
    def _setup(self):
        client = ConfigClient()
        username = os.environ.get('CONFIGSERVER_AUTH_USERNAME')
        password = os.environ.get('CONFIGSERVER_AUTH_PASSWORD')

        if not username or not password:
            raise ValueError('Authentication username or password is not configured!')

        auth = HTTPBasicAuth(username, password)

        client.get_config(auth=auth)
        self._wrapped = client.config

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self.__dict__."""
        if (_wrapped := self._wrapped) is empty:
            self._setup()
            _wrapped = self._wrapped

        return Resolver.resolve(_wrapped.get(name))

