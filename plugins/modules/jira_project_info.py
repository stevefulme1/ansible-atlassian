#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_project_info
short_description: >-
  Retrieve information about jira project resources
version_added: "1.0.0"
description:
  - >-
    Retrieve a single jira project by its identifier,
    or list all jira project resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the jira project to retrieve.
      - When omitted, all jira project resources are listed.
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
- name: Get a specific jira project
  stevefulme1.atlassian.jira_project_info:
    id: "example_id"
  register: result

- name: List all jira project resources
  stevefulme1.atlassian.jira_project_info:
  register: result


- name: List jira project resources filtered by name
  stevefulme1.atlassian.jira_project_info:
    name: "my_jira project"
  register: result


- name: List jira project resources with pagination
  stevefulme1.atlassian.jira_project_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
jira_projects:
  description: List of jira project resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    archived:
      description: >-
        Whether the project is archived.
      type: bool


    archivedBy:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    archivedDate:
      description: >-
        The date when the project was archived.
      type: str


    assigneeType:
      description: >-
        The default assignee when creating issues for this project.
      type: str


    avatarUrls:
      description: >-
        
      type: dict


    components:
      description: >-
        List of the components contained in the project.
      type: list


    deleted:
      description: >-
        Whether the project is marked as deleted.
      type: bool


    deletedBy:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    deletedDate:
      description: >-
        The date when the project was marked as deleted.
      type: str


    description:
      description: >-
        A brief description of the project.
      type: str


    email:
      description: >-
        An email address associated with the project.
      type: str


    expand:
      description: >-
        Expand options that include additional project details in the response.
      type: str


    favourite:
      description: >-
        Whether the project is selected as a favorite.
      type: bool


    id:
      description: >-
        The ID of the project.
      type: str


    insight:
      description: >-
        Additional details about a project.
      type: dict


    isPrivate:
      description: >-
        Whether the project is private from the user's perspective. This means the user can't see the...
      type: bool


    issueTypeHierarchy:
      description: >-
        The project issue type hierarchy.
      type: dict


    issueTypes:
      description: >-
        List of the issue types available in the project.
      type: list


    key:
      description: >-
        The key of the project.
      type: str


    landingPageInfo:
      description: >-
        
      type: dict


    lead:
      description: >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
      type: dict


    name:
      description: >-
        The name of the project.
      type: str


    permissions:
      description: >-
        Permissions which a user has on a project.
      type: dict


    projectCategory:
      description: >-
        A project category.
      type: dict


    projectTypeKey:
      description: >-
        The project type of the project.
      type: str


    properties:
      description: >-
        Map of project properties
      type: dict


    retentionTillDate:
      description: >-
        The date when the project is deleted permanently.
      type: str


    roles:
      description: >-
        The name and self URL for each role defined in the project. For more information, see Create...
      type: dict


    self:
      description: >-
        The URL of the project details.
      type: str


    simplified:
      description: >-
        Whether the project is simplified.
      type: bool


    style:
      description: >-
        The type of the project.
      type: str


    url:
      description: >-
        A link to information about this project, such as project documentation.
      type: str


    uuid:
      description: >-
        Unique ID for next-gen projects.
      type: str


    versions:
      description: >-
        The versions defined in the project. For more information, see Create...
      type: list


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single jira project by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/rest/api/3/project")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List jira project resources with optional filtering and pagination."""

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
        response = client.get("/rest/api/3/project", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/rest/api/3/project", params=params)



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
        jira_projects=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["jira_projects"] = [item] if item else []
        else:
            result["jira_projects"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
