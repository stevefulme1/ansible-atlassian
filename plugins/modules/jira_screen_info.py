#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_screen_info
short_description: >-
  Retrieve information about jira screen resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira screen by its identifier,
    or list all jira screen resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira screen to retrieve.
      - When omitted, all jira screen resources are listed.
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
- name: Get a specific jira screen
  stevefulme1.atlassian.jira_screen_info:
    id: "example_id"
  register: result

- name: List all jira screen resources
  stevefulme1.atlassian.jira_screen_info:
  register: result



- name: List jira screen resources with pagination
  stevefulme1.atlassian.jira_screen_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_screens:
  description: List of jira screen resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    isLast:
      description: >-
        Whether this is the last page.
      type: bool


    maxResults:
      description: >-
        The maximum number of items that could be returned.
      type: int


    nextPage:
      description: >-
        If there is another page of results, the URL of the next page.
      type: str


    self:
      description: >-
        The URL of the page.
      type: str


    startAt:
      description: >-
        The index of the first item returned.
      type: int


    total:
      description: >-
        The number of items returned.
      type: int


    values:
      description: >-
        The list of items.
      type: list


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira screen by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/screens")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List jira screen resources with optional filtering and pagination."""

    params = {}









    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/rest/api/3/screens", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/screens", params=params)



def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),






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
        jira_screens=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_screens"] = [item] if item else []
        else:
            result["jira_screens"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
