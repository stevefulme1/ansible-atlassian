#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_filter_info
short_description: Retrieve information about filter resources
version_added: "1.0.0"
description:
  - Retrieve a single filter by its identifier, or list all filter resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the filter to retrieve.
      - When omitted, all filter resources are listed.
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
- name: Get a specific filter
  stevefulme1.atlassian.jira_filter_info:
    id: "example_id"
  register: result


- name: List all filter resources
  stevefulme1.atlassian.jira_filter_info:
  register: result


- name: List filter resources filtered by name
  stevefulme1.atlassian.jira_filter_info:
    name: "my_filter"
  register: result


- name: List filter resources with pagination
  stevefulme1.atlassian.jira_filter_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
filters:
  description: List of filter resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    approximateLastUsed:
      description: >-
        \Experimental\ Approximate last used time. Returns the date and time when the filter was last...
      type: str

    description:
      description: >-
        A description of the filter.
      type: str

    editPermissions:
      description: >-
        The groups and projects that can edit the filter.
      type: list

    favourite:
      description: >-
        Whether the filter is selected as a favorite.
      type: bool

    favouritedCount:
      description: >-
        The count of how many users have selected this filter as a favorite, including the filter owner.
      type: int

    id:
      description: >-
        The unique identifier for the filter.
      type: str

    jql:
      description: >-
        The JQL query for the filter. For example, project = SSP AND issuetype = Bug.
      type: str

    name:
      description: >-
        The name of the filter. Must be unique.
      type: str

    owner:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict

    searchUrl:
      description: >-
        A URL to view the filter results in Jira, using the Search for issues using...
      type: str

    self:
      description: >-
        The URL of the filter.
      type: str

    sharePermissions:
      description: >-
        The groups and projects that the filter is shared with.
      type: list

    sharedUsers:
      description: >-
        A paginated list of users sharing the filter. This includes users that are members of the groups...
      type: dict

    subscriptions:
      description: >-
        A paginated list of subscriptions to a filter.
      type: dict

    viewUrl:
      description: >-
        A URL to view the filter results in Jira, using the ID of the filter. For example,...
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single filter by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List filter resources with optional filtering and pagination."""

    raise ClientError("List operation is not supported for this resource")


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
        filters=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["filters"] = [item] if item else []
        else:
            result["filters"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
