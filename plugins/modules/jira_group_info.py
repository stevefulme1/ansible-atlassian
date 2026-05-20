#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_group_info
short_description: Retrieve information about group resources
version_added: "1.0.0"
description:
  - Retrieve a single group by its identifier, or list all group resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer"
options:
  id:
    description:
      - The unique identifier of the group to retrieve.
      - When omitted, all group resources are listed.
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
- name: Get a specific group
  stevefulme1.atlassian.jira_group_info:
    id: "example_id"
  register: result

- name: List all group resources
  stevefulme1.atlassian.jira_group_info:
  register: result

- name: List group resources filtered by name
  stevefulme1.atlassian.jira_group_info:
    name: "my_group"
  register: result

- name: List group resources with pagination
  stevefulme1.atlassian.jira_group_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
groups:
  description: List of group resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    groupId:
      description: >-
        The ID of the group, which uniquely identifies the group across all Atlassian products. For...
      type: str

    name:
      description: >-
        The name of group.
      type: str

    self:
      description: >-
        The URL for these group details.
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single group by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/user/groups")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List group resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/user/groups", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/user/groups", params=params)



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
        groups=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["groups"] = [item] if item else []
        else:
            result["groups"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
