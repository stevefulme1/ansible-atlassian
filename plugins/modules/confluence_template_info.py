#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_template_info
short_description: >-
  Retrieve information about confluence template resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single confluence template by its identifier,
    or list all confluence template resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the confluence template to retrieve.
      - When omitted, all confluence template resources are listed.
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
- name: Get a specific confluence template
  stevefulme1.atlassian.confluence_template_info:
    id: "example_id"
  register: result
- name: List all confluence template resources
  stevefulme1.atlassian.confluence_template_info:
  register: result
- name: List confluence template resources filtered by name
  stevefulme1.atlassian.confluence_template_info:
    name: "my_confluence template"
  register: result
- name: List confluence template resources with pagination
  stevefulme1.atlassian.confluence_template_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
confluence_templates:
  description: List of confluence template resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:
    templateId:
      description: >-
      type: str
    originalTemplate:
      description: >-
      type: dict
    referencingBlueprint:
      description: >-
      type: str
    name:
      description: >-
      type: str
    description:
      description: >-
      type: str
    space:
      description: >-
      type: dict
    labels:
      description: >-
      type: list
    templateType:
      description: >-
      type: str
    editorVersion:
      description: >-
      type: str
    body:
      description: >-
        The body of the new content. Does not apply to attachments. Only one body format should be...
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
    """Retrieve a single confluence template by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List confluence template resources with optional filtering and pagination."""

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
        confluence_templates=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["confluence_templates"] = [item] if item else []
        else:
            result["confluence_templates"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
