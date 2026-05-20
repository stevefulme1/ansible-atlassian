#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_issue_info
short_description: >-
  Retrieve information about jira issue resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira issue by its identifier,
    or list all jira issue resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira issue to retrieve.
      - When omitted, all jira issue resources are listed.
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
- name: Get a specific jira issue
  stevefulme1.atlassian.jira_issue_info:
    id: "example_id"
  register: result

- name: List all jira issue resources
  stevefulme1.atlassian.jira_issue_info:
  register: result


- name: List jira issue resources with pagination
  stevefulme1.atlassian.jira_issue_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_issues:
  description: List of jira issue resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    changelog:
      description: >-
        A page of changelogs.
      type: dict


    editmeta:
      description: >-
        A list of editable field details.
      type: dict


    expand:
      description: >-
        Expand options that include additional issue details in the response.
      type: str


    fields:
      description: >-

      type: dict


    fieldsToInclude:
      description: >-

      type: dict


    id:
      description: >-
        The ID of the issue.
      type: str


    key:
      description: >-
        The key of the issue.
      type: str


    names:
      description: >-
        The ID and name of each field present on the issue.
      type: dict


    operations:
      description: >-
        Details of the operations that can be performed on the issue.
      type: dict


    properties:
      description: >-
        Details of the issue properties identified in the request.
      type: dict


    renderedFields:
      description: >-
        The rendered value of each field present on the issue.
      type: dict


    schema:
      description: >-
        The schema describing each field present on the issue.
      type: dict


    self:
      description: >-
        The URL of the issue details.
      type: str


    transitions:
      description: >-
        The transitions that can be performed on the issue.
      type: list


    versionedRepresentations:
      description: >-
        The versions of each field on the issue.
      type: dict


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira issue by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List jira issue resources with optional filtering and pagination."""

    raise ClientError("List operation is not supported for this resource")


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
        jira_issues=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_issues"] = [item] if item else []
        else:
            result["jira_issues"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
