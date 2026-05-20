#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_user_info
short_description: Retrieve information about user resources
version_added: "1.0.0"
description:
  - Retrieve a single user by its identifier, or list all user resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  key:
    description:
      - The unique identifier of the user to retrieve.
      - When omitted, all user resources are listed.
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
- name: Get a specific user
  stevefulme1.atlassian.jira_user_info:
    key: "example_id"
  register: result


- name: List all user resources
  stevefulme1.atlassian.jira_user_info:
  register: result


- name: List user resources filtered by name
  stevefulme1.atlassian.jira_user_info:
    name: "my_user"
  register: result


- name: List user resources with pagination
  stevefulme1.atlassian.jira_user_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
users:
  description: List of user resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    accountId:
      description: >-
        The account ID of the user, which uniquely identifies the user across all Atlassian products....
      type: str

    accountType:
      description: >-
        The user account type. Can take the following values: atlassian regular Atlassian user account...
      type: str

    active:
      description: >-
        Whether the user is active.
      type: bool

    appType:
      description: >-
        The app type of the user account when accountType is 'app'. Can take the following values:...
      type: str

    applicationRoles:
      description: >-

      type: dict

    avatarUrls:
      description: >-

      type: dict

    displayName:
      description: >-
        The display name of the user. Depending on the user's privacy setting, this may return an...
      type: str

    emailAddress:
      description: >-
        The email address of the user. Depending on the user's privacy setting, this may be returned as null.
      type: str

    expand:
      description: >-
        Expand options that include additional user details in the response.
      type: str

    groups:
      description: >-

      type: dict

    guest:
      description: >-
        Whether the user is a guest.
      type: bool

    key:
      description: >-
        This property is no longer available and will be removed from the documentation soon. See the...
      type: str

    locale:
      description: >-
        The locale of the user. Depending on the user's privacy setting, this may be returned as null.
      type: str

    name:
      description: >-
        This property is no longer available and will be removed from the documentation soon. See the...
      type: str

    self:
      description: >-
        The URL of the user.
      type: str

    timeZone:
      description: >-
        The time zone specified in the user's profile. If the user's time zone is not visible to the...
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single user by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/users")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("key")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List user resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/users", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/users", params=params)


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            key=dict(type="str", required=False),

            name=dict(type="str", required=False),

            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("key", "page"),
            ("key", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        users=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("key")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["users"] = [item] if item else []
        else:
            result["users"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
