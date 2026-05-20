#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_label_info
short_description: Retrieve information about label resources
version_added: "1.0.0"
description:
  - Retrieve a single label by its identifier, or list all label resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the label to retrieve.
      - When omitted, all label resources are listed.
    type: str
    required: false

  label:
    description:
      - Filter results by label.
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
- name: Get a specific label
  stevefulme1.atlassian.confluence_label_info:
    id: "example_id"
  register: result

- name: List all label resources
  stevefulme1.atlassian.confluence_label_info:
  register: result

- name: List label resources filtered by label
  stevefulme1.atlassian.confluence_label_info:
    label: "my_label"
  register: result

- name: List label resources with pagination
  stevefulme1.atlassian.confluence_label_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
labels:
  description: List of label resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    label:
      description: >-

      type: dict

    associatedContents:
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
    """Retrieve a single label by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/wiki/rest/api/label")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None

def fetch_list(client, module):
    """List label resources with optional filtering and pagination."""

    params = {}

    name_filter = module.params.get("label")
    if name_filter is not None:
        params["label"] = name_filter

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/wiki/rest/api/label", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/wiki/rest/api/label", params=params)

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            label=dict(type="str", required=False),

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
        labels=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["labels"] = [item] if item else []
        else:
            result["labels"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
