#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_dashboard_info
short_description: >-
  Retrieve information about jira dashboard resources

version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira dashboard by its identifier,
    or list all jira dashboard resources.
  - This module always reports C(changed=False).

author:
  - "Steve Fulmer (@stevefulme1)"

options:
  id:
    description:
      - The unique identifier of the jira dashboard to retrieve.
      - When omitted, all jira dashboard resources are listed.
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
- name: Get a specific jira dashboard
  stevefulme1.atlassian.jira_dashboard_info:
    id: "example_id"
  register: result

- name: List all jira dashboard resources
  stevefulme1.atlassian.jira_dashboard_info:
  register: result

- name: List jira dashboard resources filtered by name
  stevefulme1.atlassian.jira_dashboard_info:
    name: "my_jira dashboard"
  register: result

- name: List jira dashboard resources with pagination
  stevefulme1.atlassian.jira_dashboard_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_dashboards:
  description: List of jira dashboard resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:
    automaticRefreshMs:
      description: >-
        The automatic refresh interval for the dashboard in milliseconds.
      type: int
    description:
      description: >-
      type: str
    editPermissions:
      description: >-
        The details of any edit share permissions for the dashboard.
      type: list
    id:
      description: >-
        The ID of the dashboard.
      type: str
    isFavourite:
      description: >-
        Whether the dashboard is selected as a favorite by the user.
      type: bool
    isWritable:
      description: >-
        Whether the current user has permission to edit the dashboard.
      type: bool
    name:
      description: >-
        The name of the dashboard.
      type: str
    owner:
      description: >-
      type: dict
    popularity:
      description: >-
        The number of users who have this dashboard as a favorite.
      type: int
    rank:
      description: >-
        The rank of this dashboard.
      type: int
    self:
      description: >-
        The URL of these dashboard details.
      type: str
    sharePermissions:
      description: >-
        The details of any view share permissions for the dashboard.
      type: list
    systemDashboard:
      description: >-
        Whether the current dashboard is system dashboard.
      type: bool
    view:
      description: >-
        The URL of the dashboard.
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,

)


def fetch_single(client, identifier):
    """Retrieve a single jira dashboard by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/dashboard")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List jira dashboard resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/dashboard", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/dashboard", params=params)


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
        jira_dashboards=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_dashboards"] = [item] if item else []
        else:
            result["jira_dashboards"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
