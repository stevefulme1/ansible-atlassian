#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_priority_info
short_description: Retrieve information about priority resources
version_added: "1.0.0"
description:
  - Retrieve a single priority by its identifier, or list all priority resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the priority to retrieve.
      - When omitted, all priority resources are listed.
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
- name: Get a specific priority
  stevefulme1.atlassian.jira_priority_info:
    id: "example_id"
  register: result


- name: List all priority resources
  stevefulme1.atlassian.jira_priority_info:
  register: result


- name: List priority resources filtered by name
  stevefulme1.atlassian.jira_priority_info:
    name: "my_priority"
  register: result


- name: List priority resources with pagination
  stevefulme1.atlassian.jira_priority_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
prioritys:
  description: List of priority resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    avatarId:
      description: >-
        The avatarId of the avatar for the issue priority. This parameter is nullable and when set, this...
      type: int

    description:
      description: >-
        The description of the issue priority.
      type: str

    iconUrl:
      description: >-
        The URL of the icon for the issue priority.
      type: str

    id:
      description: >-
        The ID of the issue priority.
      type: str

    isDefault:
      description: >-
        Whether this priority is the default.
      type: bool

    name:
      description: >-
        The name of the issue priority.
      type: str

    schemes:
      description: >-

      type: dict

    self:
      description: >-
        The URL of the issue priority.
      type: str

    statusColor:
      description: >-
        The color used to indicate the issue priority.
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single priority by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/priority")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List priority resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/priority", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/priority", params=params)


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
        prioritys=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["prioritys"] = [item] if item else []
        else:
            result["prioritys"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
