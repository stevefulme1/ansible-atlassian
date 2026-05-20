#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_permission_scheme_info
short_description: >-
  Retrieve information about jira permission scheme resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira permission scheme by its identifier,
    or list all jira permission scheme resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira permission scheme to retrieve.
      - When omitted, all jira permission scheme resources are listed.
    type: str
    required: false

  name:
    description:
      - Filter results by name.
    type: str
    required: false
















  page:
    description:
      - Page number for paginated results.
      - Only applies when listing resources.
    type: int
    required: false
  page_size:
    description:
      - Number of results per page.
      - Only applies when listing resources.
    type: int
    required: false
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Get a specific jira permission scheme
  stevefulme1.atlassian.jira_permission_scheme_info:
    id: "example_id"
  register: result

- name: List all jira permission scheme resources
  stevefulme1.atlassian.jira_permission_scheme_info:
  register: result


- name: List jira permission scheme resources filtered by name
  stevefulme1.atlassian.jira_permission_scheme_info:
    name: "my_jira permission scheme"
  register: result


- name: List jira permission scheme resources with pagination
  stevefulme1.atlassian.jira_permission_scheme_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_permission_schemes:
  description: List of jira permission scheme resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    description:
      description: >-
        A description for the permission scheme.
      type: str


    expand:
      description: >-
        The expand options available for the permission scheme.
      type: str


    id:
      description: >-
        The ID of the permission scheme.
      type: int


    name:
      description: >-
        The name of the permission scheme. Must be unique.
      type: str


    permissions:
      description: >-
        The permission scheme to create or update. See About permission schemes and...
      type: list


    scope:
      description: >-
        The projects the item is associated with. Indicated for items associated with next-gen projects.
      type: dict


    self:
      description: >-
        The URL of the permission scheme.
      type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira permission scheme by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/permissionscheme")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List jira permission scheme resources with optional filtering and pagination."""

    params = {}


    name_filter = module.params.get("name")
    if name_filter is not None:
        params["name"] = name_filter


















    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/rest/api/3/permissionscheme", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/permissionscheme", params=params)



def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            name=dict(type="str", required=False),
















            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("id", "page"),
            ("id", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        jira_permission_schemes=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_permission_schemes"] = [item] if item else []
        else:
            result["jira_permission_schemes"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
