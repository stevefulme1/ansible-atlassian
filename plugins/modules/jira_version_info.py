#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_version_info
short_description: >-
  Retrieve information about jira version resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira version by its identifier,
    or list all jira version resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira version to retrieve.
      - When omitted, all jira version resources are listed.
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
- name: Get a specific jira version
  stevefulme1.atlassian.jira_version_info:
    id: "example_id"
  register: result
- name: List all jira version resources
  stevefulme1.atlassian.jira_version_info:
  register: result
- name: List jira version resources filtered by name
  stevefulme1.atlassian.jira_version_info:
    name: "my_jira version"
  register: result
- name: List jira version resources with pagination
  stevefulme1.atlassian.jira_version_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_versions:
  description: List of jira version resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:
    approvers:
      description: >-
        If the expand option approvers is used, returns a list containing the approvers for this version.
      type: list
    archived:
      description: >-
        Indicates that the version is archived. Optional when creating or updating a version.
      type: bool
    description:
      description: >-
        The description of the version. Optional when creating or updating a version. The maximum size...
      type: str
    driver:
      description: >-
        The Atlassian account ID of the version driver. Optional when creating or updating a version. If...
      type: str
    expand:
      description: >-
        Use expand(em>expansion) to include additional information about version in the response. This...
      type: str
    id:
      description: >-
        The ID of the version.
      type: str
    issuesStatusForFixVersion:
      description: >-
        Counts of the number of issues in various statuses.
      type: dict
    moveUnfixedIssuesTo:
      description: >-
        The URL of the self link to the version to which all unfixed issues are moved when a version is...
      type: str
    name:
      description: >-
        The unique name of the version. Required when creating a version. Optional when updating a...
      type: str
    operations:
      description: >-
        If the expand option operations is used, returns the list of operations available for this version.
      type: list
    overdue:
      description: >-
        Indicates that the version is overdue.
      type: bool
    project:
      description: >-
        Deprecated. Use projectId.
      type: str
    projectId:
      description: >-
        The ID of the project to which this version is attached. Required when creating a version. Not...
      type: int
    releaseDate:
      description: >-
        The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when...
      type: str
    released:
      description: >-
        Indicates that the version is released. If the version is released a request to release again is...
      type: bool
    self:
      description: >-
        The URL of the version.
      type: str
    startDate:
      description: >-
        The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating...
      type: str
    userReleaseDate:
      description: >-
        The date on which work on this version is expected to finish, expressed in the instance's...
      type: str
    userStartDate:
      description: >-
        The date on which work on this version is expected to start, expressed in the instance's...
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira version by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List jira version resources with optional filtering and pagination."""

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
        jira_versions=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_versions"] = [item] if item else []
        else:
            result["jira_versions"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
