# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import re


def camel_dict_to_snake_dict(camel_dict, reversible=False, ignore_list=()):
    """
    reversible allows two way conversion of a camelized dict
    such that snake_dict_to_camel_dict(camel_dict_to_snake_dict(x)) == x

    This is achieved through mapping e.g. HTTPEndpoint to h_t_t_p_endpoint
    where the default would be simply http_endpoint, which gets turned into
    HttpEndpoint if recamelized.

    ignore_list is used to avoid converting a sub-tree of a dict. This is
    particularly important for tags, where keys are case-sensitive. We convert
    the 'Tags' key but nothing below.
    """

    def value_is_list(camel_list):

        checked_list = []
        for item in camel_list:
            if isinstance(item, dict):
                checked_list.append(camel_dict_to_snake_dict(item, reversible))
            elif isinstance(item, list):
                checked_list.append(value_is_list(item))
            else:
                checked_list.append(item)

        return checked_list

    snake_dict = {}
    for k, v in camel_dict.items():
        if isinstance(v, dict) and k not in ignore_list:
            snake_dict[_camel_to_snake(k, reversible=reversible)] = camel_dict_to_snake_dict(v, reversible)
        elif isinstance(v, list) and k not in ignore_list:
            snake_dict[_camel_to_snake(k, reversible=reversible)] = value_is_list(v)
        else:
            snake_dict[_camel_to_snake(k, reversible=reversible)] = v

    return snake_dict


def snake_dict_to_camel_dict(snake_dict, capitalize_first=False):
    """
    Perhaps unexpectedly, snake_dict_to_camel_dict returns dromedaryCase
    rather than true CamelCase. Passing capitalize_first=True returns
    CamelCase. The default remains False as that was the original implementation
    """

    def camelize(complex_type, capitalize_first=False):
        if complex_type is None:
            return
        new_type = type(complex_type)()
        if isinstance(complex_type, dict):
            for key in complex_type:
                new_type[_snake_to_camel(key, capitalize_first)] = camelize(complex_type[key], capitalize_first)
        elif isinstance(complex_type, list):
            for i in range(len(complex_type)):
                new_type.append(camelize(complex_type[i], capitalize_first))
        else:
            return complex_type
        return new_type

    return camelize(snake_dict, capitalize_first)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def _camel_to_snake(name, reversible=False):

    def prepend_underscore_and_lower(m):
        return '_' + m.group(0).lower()

    import re
    if reversible:
        upper_pattern = r'[A-Z]'
    else:
        # Cope with pluralized abbreviations such as TargetGroupARNs
        # that would otherwise be rendered target_group_ar_ns
        upper_pattern = r'[A-Z]{3,}s$'

    s1 = re.sub(upper_pattern, prepend_underscore_and_lower, name)
    # Handle when there was nothing before the plural_pattern
    if s1.startswith("_") and not name.startswith("_"):
        s1 = s1[1:]
    if reversible:
        return s1

    # Remainder of solution seems to be https://stackoverflow.com/a/1176023
    first_cap_pattern = r'(.)([A-Z][a-z]+)'
    all_cap_pattern = r'([a-z0-9])([A-Z]+)'
    s2 = re.sub(first_cap_pattern, r'\1_\2', s1)
    return re.sub(all_cap_pattern, r'\1_\2', s2).lower()
