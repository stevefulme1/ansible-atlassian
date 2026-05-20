#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_space_info
short_description: >-
  Retrieve information about confluence space resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single confluence space by its identifier,
    or list all confluence space resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the confluence space to retrieve.
      - When omitted, all confluence space resources are listed.
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
- name: Get a specific confluence space
  stevefulme1.atlassian.confluence_space_info:
    id: "example_id"
  register: result
- name: List all confluence space resources
  stevefulme1.atlassian.confluence_space_info:
  register: result
- name: List confluence space resources filtered by name
  stevefulme1.atlassian.confluence_space_info:
    name: "my_confluence space"
  register: result
- name: List confluence space resources with pagination
  stevefulme1.atlassian.confluence_space_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
confluence_spaces:
  description: List of confluence space resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:
    id:
      description: >-
      type: int
    key:
      description: >-
      type: str
    alias:
      description: >-
      type: str
    name:
      description: >-
      type: str
    icon:
      description: >-
        This object represents an icon. If used as a profilePicture, this may be returned as null,...
      type: dict
    description:
      description: >-
      type: dict
    homepage:
      description: >-
        Base object for all content types.
      type: dict
    type:
      description: >-
      type: str
    metadata:
      description: >-
      type: dict
    operations:
      description: >-
      type: list
    permissions:
      description: >-
      type: list
    status:
      description: >-
      type: str
    settings:
      description: >-
      type: dict
    theme:
      description: >-
      type: dict
    lookAndFeel:
      description: >-
      type: dict
    history:
      description: >-
      type: dict
    _expandable:
      description: >-
      type: dict
    _links:
      description: >-
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single confluence space by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List confluence space resources with optional filtering and pagination."""

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
        confluence_spaces=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["confluence_spaces"] = [item] if item else []
        else:
            result["confluence_spaces"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
