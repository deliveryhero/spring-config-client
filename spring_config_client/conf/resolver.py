import os
import re

from spring_config_client.dot_dict import DotDict


class Resolver:
    @staticmethod
    def resolve(value):
        """
        Resolver function for
            ${<local_environ_key>}
            ${<local_environ_key>:<fallback>}
        this format represents that value should be taken from local environment
        in case its not found ${<local_environ_key>} -> returns None
        ${<local_environ_key>:<fallback>} -> returns fallback value

        :param value:
        :return:
        """
        if isinstance(value, dict):
            return DotDict(value)

        if not isinstance(value, str):
            return value

        matcher = r"\$\{(\w*):?(\w*)\}"
        result = re.search(matcher, value)

        if not result:
            return value

        key, default_value = result.groups()
        env_value = os.environ.get(key)

        if not default_value:
            return env_value

        if env_value:
            return env_value

        return default_value
