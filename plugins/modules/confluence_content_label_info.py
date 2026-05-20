#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_content_label_info
short_description: Retrieve information about content_label resources
version_added: "1.0.0"
description:
  - Retrieve a single content_label by its identifier, or list all content_label resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the content_label to retrieve.
      - When omitted, all content_label resources are listed.
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
- name: Get a specific content_label
  stevefulme1.atlassian.confluence_content_label_info:
    id: "example_id"
  register: result


- name: List all content_label resources
  stevefulme1.atlassian.confluence_content_label_info:
  register: result


- name: List content_label resources filtered by name
  stevefulme1.atlassian.confluence_content_label_info:
    name: "my_content_label"
  register: result


- name: List content_label resources with pagination
  stevefulme1.atlassian.confluence_content_label_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
content_labels:
  description: List of content_label resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    prefix:
      description: >-

      type: str

    name:
      description: >-

      type: str

    id:
      description: >-

      type: str

    label:
      description: >-

      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single content_label by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List content_label resources with optional filtering and pagination."""

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
        content_labels=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["content_labels"] = [item] if item else []
        else:
            result["content_labels"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
