from serpng.lib.utils.dotted_dict import DottedDict
from config import * 


def get_configs_from_module(module):
    """
    Returns a dictionary-like object that contains the definitions in the 
    passed-in module as key-value pairs.

    Args:
        module: module object that contains definitions.

    Returns:
        A DottedDict object that contains the definitions in the passed-in
        module as key-value pairs. The values in the DottedDict object
        can be accessed with the dot notation.
    """
    configs = DottedDict()

    if module:
        for config_name in dir(module):
            # Do not copy over any builtin definitions.
            if not config_name.startswith('__'):
                configs[config_name] = getattr(module, config_name, None)

    return configs

def get_configs(language_code='en-us'):
    """
    Returns a dictionary-like object that contains the configurations for 
    the locale corresponding to the passed-in language_code as key-value pairs.

    Args:
        language_code: A string that represents a language code. E.g., 'fr-ca'.

    Returns:
        A DottedDict object that contains, as key-value pairs, the configurations
        for the locale corresponding to the passed-in language_code.
    """
    # Initialize a DottedDict object with default configurations.
    configs = get_configs_from_module(default_configs) # pylint: disable=E0602

    # Based on the passed-in language code, determine the configs module for
    # that language code and update the default configurations with locale-
    # specific configurations.
    locale_module_name = language_code.replace("-", "_") + '_configs'
    configs.update(get_configs_from_module(globals()[locale_module_name]))

    return configs
