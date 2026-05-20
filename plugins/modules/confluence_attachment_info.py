#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_attachment_info
short_description: >-
  Retrieve information about confluence attachment resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single confluence attachment by its identifier,
    or list all confluence attachment resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the confluence attachment to retrieve.
      - When omitted, all confluence attachment resources are listed.
    type: str
    required: false

  title:
    description:
      - Filter results by title.
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
- name: Get a specific confluence attachment
  stevefulme1.atlassian.confluence_attachment_info:
    id: "example_id"
  register: result

- name: List all confluence attachment resources
  stevefulme1.atlassian.confluence_attachment_info:
  register: result


- name: List confluence attachment resources filtered by title
  stevefulme1.atlassian.confluence_attachment_info:
    title: "my_confluence attachment"
  register: result


- name: List confluence attachment resources with pagination
  stevefulme1.atlassian.confluence_attachment_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
confluence_attachments:
  description: List of confluence attachment resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-

      type: str


    type:
      description: >-
        Can be "page", "blogpost", "attachment" or "content"
      type: str


    status:
      description: >-

      type: str


    title:
      description: >-

      type: str


    space:
      description: >-

      type: dict


    history:
      description: >-

      type: dict


    version:
      description: >-

      type: dict


    ancestors:
      description: >-

      type: list


    operations:
      description: >-

      type: list


    children:
      description: >-

      type: dict


    childTypes:
      description: >-
        Shows whether a piece of content has attachments, comments, or child pages/whiteboards. Note,...
      type: dict


    descendants:
      description: >-

      type: dict


    container:
      description: >-
        Container for content. This can be either a space (containing a page or blogpost) or a page/blog...
      type: dict


    body:
      description: >-

      type: dict


    restrictions:
      description: >-

      type: dict


    metadata:
      description: >-
        Metadata object for page, blogpost, comment content
      type: dict


    macroRenderedOutput:
      description: >-

      type: dict


    extensions:
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
    """Retrieve a single confluence attachment by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List confluence attachment resources with optional filtering and pagination."""

    raise ClientError("List operation is not supported for this resource")


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            title=dict(type="str", required=False),


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
        confluence_attachments=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["confluence_attachments"] = [item] if item else []
        else:
            result["confluence_attachments"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
