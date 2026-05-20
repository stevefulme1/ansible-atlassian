#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_component_info
short_description: >-
  Retrieve information about jira component resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira component by its identifier,
    or list all jira component resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira component to retrieve.
      - When omitted, all jira component resources are listed.
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
- name: Get a specific jira component
  stevefulme1.atlassian.jira_component_info:
    id: "example_id"
  register: result

- name: List all jira component resources
  stevefulme1.atlassian.jira_component_info:
  register: result


- name: List jira component resources filtered by name
  stevefulme1.atlassian.jira_component_info:
    name: "my_jira component"
  register: result


- name: List jira component resources with pagination
  stevefulme1.atlassian.jira_component_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_components:
  description: List of jira component resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    ari:
      description: >-
        Compass component's ID. Can't be updated. Not required for creating a Project Component.
      type: str


    assignee:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    assigneeType:
      description: >-
        The nominal user type used to determine the assignee for issues created with this component. See...
      type: str


    description:
      description: >-
        The description for the component. Optional when creating or updating a component.
      type: str


    id:
      description: >-
        The unique identifier for the component.
      type: str


    isAssigneeTypeValid:
      description: >-
        Whether a user is associated with assigneeType. For example, if the assigneeType is set to...
      type: bool


    lead:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    leadAccountId:
      description: >-
        The accountId of the component's lead user. The accountId uniquely identifies the user across...
      type: str


    leadUserName:
      description: >-
        This property is no longer available and will be removed from the documentation soon. See the...
      type: str


    metadata:
      description: >-
        Compass component's metadata. Can't be updated. Not required for creating a Project Component.
      type: dict


    name:
      description: >-
        The unique name for the component in the project. Required when creating a component. Optional...
      type: str


    project:
      description: >-
        The key of the project the component is assigned to. Required when creating a component. Can't...
      type: str


    projectId:
      description: >-
        The ID of the project the component is assigned to.
      type: int


    realAssignee:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    realAssigneeType:
      description: >-
        The type of the assignee that is assigned to issues created with this component, when an...
      type: str


    self:
      description: >-
        The URL of the component.
      type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira component by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/component")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List jira component resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/component", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/component", params=params)


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
        jira_components=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_components"] = [item] if item else []
        else:
            result["jira_components"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
