#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_project
short_description: Manage projects
version_added: "1.0.0"
description:
  - Create, update, and delete jira project resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the jira project resource.
    type: str
    choices: ['present', 'absent']
    default: present
  assigneeType:
    description:
      - >-
        The default assignee when creating issues for this project.
    type: str
    choices: ["PROJECT_LEAD", "UNASSIGNED"]
  avatarId:
    description:
      - >-
        An integer value for the project's avatar.
    type: int
  categoryId:
    description:
      - >-
        The ID of the project's category. A complete list of category IDs is found using the Get all...
    type: int
  description:
    description:
      - >-
        A brief description of the project.
    type: str
  fieldConfigurationScheme:
    description:
      - >-
        Deprecated use fieldScheme instead. The ID of the field configuration scheme for the project....
    type: int
  fieldScheme:
    description:
      - >-
        The ID of the field scheme for the project. Use the Get field...
    type: int
  issueSecurityScheme:
    description:
      - >-
        The ID of the issue security scheme for the project, which enables you to control who can and...
    type: int
  issueTypeScheme:
    description:
      - >-
        The ID of the issue type scheme for the project. Use the Get all issue type...
    type: int
  issueTypeScreenScheme:
    description:
      - >-
        The ID of the issue type screen scheme for the project. Use the Get all issue type screen...
    type: int
  key:
    description:
      - >-
        Project keys must be unique and start with an uppercase letter followed by one or more uppercase...
    type: str
  lead:
    description:
      - >-
        This parameter is deprecated because of privacy changes. Use leadAccountId instead. See the...
    type: str
  leadAccountId:
    description:
      - >-
        The account ID of the project lead. Cannot be provided with lead.
    type: str
  name:
    description:
      - >-
        The name of the project.
    type: str
  notificationScheme:
    description:
      - >-
        The ID of the notification scheme for the project. Use the Get notification...
    type: int
  permissionScheme:
    description:
      - >-
        The ID of the permission scheme for the project. Use the Get all permission...
    type: int
  projectTemplateKey:
    description:
      - >-
        A predefined configuration for a project. The type of the projectTemplateKey must match with the...
    type: str
    choices:
      - "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban"
      - "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum"
      - "com.pyxis.greenhopper.jira:gh-simplified-basic"
      - "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic"
      - "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic"
      - "com.pyxis.greenhopper.jira:gh-cross-team-template"
      - "com.pyxis.greenhopper.jira:gh-cross-team-planning-template"
      - "com.atlassian.servicedesk:simplified-it-service-management"
      - "com.atlassian.servicedesk:simplified-it-service-management-basic"
      - "com.atlassian.servicedesk:simplified-it-service-management-operations"
      - "com.atlassian.servicedesk:simplified-internal-service-desk"
      - "com.atlassian.servicedesk:simplified-external-service-desk"
      - "com.atlassian.servicedesk:simplified-hr-service-desk"
      - "com.atlassian.servicedesk:simplified-facilities-service-desk"
      - "com.atlassian.servicedesk:simplified-legal-service-desk"
      - "com.atlassian.servicedesk:simplified-marketing-service-desk"
      - "com.atlassian.servicedesk:simplified-finance-service-desk"
      - "com.atlassian.servicedesk:simplified-analytics-service-desk"
      - "com.atlassian.servicedesk:simplified-design-service-desk"
      - "com.atlassian.servicedesk:simplified-sales-service-desk"
      - "com.atlassian.servicedesk:simplified-halp-service-desk"
      - "com.atlassian.servicedesk:next-gen-it-service-desk"
      - "com.atlassian.servicedesk:next-gen-hr-service-desk"
      - "com.atlassian.servicedesk:next-gen-legal-service-desk"
      - "com.atlassian.servicedesk:next-gen-marketing-service-desk"
      - "com.atlassian.servicedesk:next-gen-facilities-service-desk"
      - "com.atlassian.servicedesk:next-gen-general-service-desk"
      - "com.atlassian.servicedesk:next-gen-analytics-service-desk"
      - "com.atlassian.servicedesk:next-gen-finance-service-desk"
      - "com.atlassian.servicedesk:next-gen-design-service-desk"
      - "com.atlassian.servicedesk:next-gen-sales-service-desk"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-content-management"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-document-approval"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-lead-tracking"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-procurement"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-project-management"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-recruitment"
      - "com.atlassian.jira-core-project-templates:jira-core-simplified-task-"
      - "com.atlassian.jcs:customer-service-management"
  projectTypeKey:
    description:
      - >-
        The project type, which defines the application-specific feature set. If you don't specify the...
    type: str
    choices: ["software", "service_desk", "business"]
  releasedProjectKeys:
    description:
      - >-
        Previous project keys to be released from the current project. Released keys must belong to the...
    type: list
    elements: dict
  url:
    description:
      - >-
        A link to information about this project, such as project documentation
    type: str
  workflowScheme:
    description:
      - >-
        The ID of the workflow scheme for the project. Use the Get all workflow...
    type: int
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a jira project
  stevefulme1.atlassian.jira_project:
    state: present
  # API: POST /rest/api/3/project
- name: Update a jira project
  stevefulme1.atlassian.jira_project:
    id: "existing_id"
    assigneeType: "updated_assigneeType"
    avatarId: "updated_avatarId"
    categoryId: "updated_categoryId"
    description: "updated_description"
    fieldConfigurationScheme: "updated_fieldConfigurationScheme"
    fieldScheme: "updated_fieldScheme"
    issueSecurityScheme: "updated_issueSecurityScheme"
    issueTypeScheme: "updated_issueTypeScheme"
    issueTypeScreenScheme: "updated_issueTypeScreenScheme"
    key: "updated_key"
    lead: "updated_lead"
    leadAccountId: "updated_leadAccountId"
    name: "updated_name"
    notificationScheme: "updated_notificationScheme"
    permissionScheme: "updated_permissionScheme"
    projectTemplateKey: "updated_projectTemplateKey"
    projectTypeKey: "updated_projectTypeKey"
    releasedProjectKeys: "updated_releasedProjectKeys"
    url: "updated_url"
    workflowScheme: "updated_workflowScheme"
    state: present
  # API:
- name: Delete a jira project
  stevefulme1.atlassian.jira_project:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/project/{projectIdOrKey}
"""

RETURN = r"""
archived:
  description: >-
    Whether the project is archived.
  returned: success
  type: bool
archivedBy:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
archivedDate:
  description: >-
    The date when the project was archived.
  returned: success
  type: str
assigneeType:
  description: >-
    The default assignee when creating issues for this project.
  returned: success
  type: str
avatarUrls:
  description: >-
  returned: success
  type: dict
components:
  description: >-
    List of the components contained in the project.
  returned: success
  type: list
deleted:
  description: >-
    Whether the project is marked as deleted.
  returned: success
  type: bool
deletedBy:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
deletedDate:
  description: >-
    The date when the project was marked as deleted.
  returned: success
  type: str
description:
  description: >-
    A brief description of the project.
  returned: success
  type: str
email:
  description: >-
    An email address associated with the project.
  returned: success
  type: str
expand:
  description: >-
    Expand options that include additional project details in the response.
  returned: success
  type: str
favourite:
  description: >-
    Whether the project is selected as a favorite.
  returned: success
  type: bool
id:
  description: >-
    The ID of the project.
  returned: success
  type: str
insight:
  description: >-
    Additional details about a project.
  returned: success
  type: dict
isPrivate:
  description: >-
    Whether the project is private from the user's perspective. This means the user can't see the...
  returned: success
  type: bool
issueTypeHierarchy:
  description: >-
    The project issue type hierarchy.
  returned: success
  type: dict
issueTypes:
  description: >-
    List of the issue types available in the project.
  returned: success
  type: list
key:
  description: >-
    The key of the project.
  returned: success
  type: str
landingPageInfo:
  description: >-
  returned: success
  type: dict
lead:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
name:
  description: >-
    The name of the project.
  returned: success
  type: str
permissions:
  description: >-
    Permissions which a user has on a project.
  returned: success
  type: dict
projectCategory:
  description: >-
    A project category.
  returned: success
  type: dict
projectTypeKey:
  description: >-
    The project type of the project.
  returned: success
  type: str
properties:
  description: >-
    Map of project properties
  returned: success
  type: dict
retentionTillDate:
  description: >-
    The date when the project is deleted permanently.
  returned: success
  type: str
roles:
  description: >-
    The name and self URL for each role defined in the project. For more information, see Create...
  returned: success
  type: dict
self:
  description: >-
    The URL of the project details.
  returned: success
  type: str
simplified:
  description: >-
    Whether the project is simplified.
  returned: success
  type: bool
style:
  description: >-
    The type of the project.
  returned: success
  type: str
url:
  description: >-
    A link to information about this project, such as project documentation.
  returned: success
  type: str
uuid:
  description: >-
    Unique ID for next-gen projects.
  returned: success
  type: str
versions:
  description: >-
    The versions defined in the project. For more information, see Create...
  returned: success
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the jira project via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/project")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("id")) == str(search_value):
                return item
        return None
    except ClientError:
        return None


def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("assigneeType") is not None:
        payload["assigneeType"] = module.params["assigneeType"]

    if module.params.get("avatarId") is not None:
        payload["avatarId"] = module.params["avatarId"]

    if module.params.get("categoryId") is not None:
        payload["categoryId"] = module.params["categoryId"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("fieldConfigurationScheme") is not None:
        payload["fieldConfigurationScheme"] = module.params["fieldConfigurationScheme"]

    if module.params.get("fieldScheme") is not None:
        payload["fieldScheme"] = module.params["fieldScheme"]

    if module.params.get("issueSecurityScheme") is not None:
        payload["issueSecurityScheme"] = module.params["issueSecurityScheme"]

    if module.params.get("issueTypeScheme") is not None:
        payload["issueTypeScheme"] = module.params["issueTypeScheme"]

    if module.params.get("issueTypeScreenScheme") is not None:
        payload["issueTypeScreenScheme"] = module.params["issueTypeScreenScheme"]

    if module.params.get("key") is not None:
        payload["key"] = module.params["key"]

    if module.params.get("lead") is not None:
        payload["lead"] = module.params["lead"]

    if module.params.get("leadAccountId") is not None:
        payload["leadAccountId"] = module.params["leadAccountId"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("notificationScheme") is not None:
        payload["notificationScheme"] = module.params["notificationScheme"]

    if module.params.get("permissionScheme") is not None:
        payload["permissionScheme"] = module.params["permissionScheme"]

    if module.params.get("projectTemplateKey") is not None:
        payload["projectTemplateKey"] = module.params["projectTemplateKey"]

    if module.params.get("projectTypeKey") is not None:
        payload["projectTypeKey"] = module.params["projectTypeKey"]

    if module.params.get("releasedProjectKeys") is not None:
        payload["releasedProjectKeys"] = module.params["releasedProjectKeys"]

    if module.params.get("url") is not None:
        payload["url"] = module.params["url"]

    if module.params.get("workflowScheme") is not None:
        payload["workflowScheme"] = module.params["workflowScheme"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            assigneeType=dict(
                type="str",





                choices=['PROJECT_LEAD', 'UNASSIGNED'],




            ),

            avatarId=dict(
                type="int",








            ),

            categoryId=dict(
                type="int",








            ),

            description=dict(
                type="str",








            ),

            fieldConfigurationScheme=dict(
                type="int",








            ),

            fieldScheme=dict(
                type="int",








            ),

            issueSecurityScheme=dict(
                type="int",








            ),

            issueTypeScheme=dict(
                type="int",








            ),

            issueTypeScreenScheme=dict(
                type="int",








            ),

            key=dict(
                type="str",



                no_log=False,






            ),

            lead=dict(
                type="str",








            ),

            leadAccountId=dict(
                type="str",








            ),

            name=dict(
                type="str",








            ),

            notificationScheme=dict(
                type="int",








            ),

            permissionScheme=dict(
                type="int",








            ),

            projectTemplateKey=dict(
                type="str",



                no_log=False,



                choices=[

                    "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban",

                    "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",

                    "com.pyxis.greenhopper.jira:gh-simplified-basic",

                    "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic",

                    "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic",

                    "com.pyxis.greenhopper.jira:gh-cross-team-template",

                    "com.pyxis.greenhopper.jira:gh-cross-team-planning-template",

                    "com.atlassian.servicedesk:simplified-it-service-management",

                    "com.atlassian.servicedesk:simplified-it-service-management-basic",

                    "com.atlassian.servicedesk:simplified-it-service-management-operations",

                    "com.atlassian.servicedesk:simplified-internal-service-desk",

                    "com.atlassian.servicedesk:simplified-external-service-desk",

                    "com.atlassian.servicedesk:simplified-hr-service-desk",

                    "com.atlassian.servicedesk:simplified-facilities-service-desk",

                    "com.atlassian.servicedesk:simplified-legal-service-desk",

                    "com.atlassian.servicedesk:simplified-marketing-service-desk",

                    "com.atlassian.servicedesk:simplified-finance-service-desk",

                    "com.atlassian.servicedesk:simplified-analytics-service-desk",

                    "com.atlassian.servicedesk:simplified-design-service-desk",

                    "com.atlassian.servicedesk:simplified-sales-service-desk",

                    "com.atlassian.servicedesk:simplified-halp-service-desk",

                    "com.atlassian.servicedesk:next-gen-it-service-desk",

                    "com.atlassian.servicedesk:next-gen-hr-service-desk",

                    "com.atlassian.servicedesk:next-gen-legal-service-desk",

                    "com.atlassian.servicedesk:next-gen-marketing-service-desk",

                    "com.atlassian.servicedesk:next-gen-facilities-service-desk",

                    "com.atlassian.servicedesk:next-gen-general-service-desk",

                    "com.atlassian.servicedesk:next-gen-analytics-service-desk",

                    "com.atlassian.servicedesk:next-gen-finance-service-desk",

                    "com.atlassian.servicedesk:next-gen-design-service-desk",

                    "com.atlassian.servicedesk:next-gen-sales-service-desk",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-content-management",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-document-approval",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-lead-tracking",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-procurement",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-project-management",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-recruitment",

                    "com.atlassian.jira-core-project-templates:jira-core-simplified-task-",

                    "com.atlassian.jcs:customer-service-management",

                ],




            ),

            projectTypeKey=dict(
                type="str",



                no_log=False,



                choices=['software', 'service_desk', 'business'],




            ),

            releasedProjectKeys=dict(
                type="list",

                elements="dict",








            , no_log=False),

            url=dict(
                type="str",








            ),

            workflowScheme=dict(
                type="int",








            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.POST(
                        "/rest/api/3/project",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["archived"] = current.get("archived")

                result["archivedBy"] = current.get("archivedBy")

                result["archivedDate"] = current.get("archivedDate")

                result["assigneeType"] = current.get("assigneeType")

                result["avatarUrls"] = current.get("avatarUrls")

                result["components"] = current.get("components")

                result["deleted"] = current.get("deleted")

                result["deletedBy"] = current.get("deletedBy")

                result["deletedDate"] = current.get("deletedDate")

                result["description"] = current.get("description")

                result["email"] = current.get("email")

                result["expand"] = current.get("expand")

                result["favourite"] = current.get("favourite")

                result["id"] = current.get("id")

                result["insight"] = current.get("insight")

                result["isPrivate"] = current.get("isPrivate")

                result["issueTypeHierarchy"] = current.get("issueTypeHierarchy")

                result["issueTypes"] = current.get("issueTypes")

                result["key"] = current.get("key")

                result["landingPageInfo"] = current.get("landingPageInfo")

                result["lead"] = current.get("lead")

                result["name"] = current.get("name")

                result["permissions"] = current.get("permissions")

                result["projectCategory"] = current.get("projectCategory")

                result["projectTypeKey"] = current.get("projectTypeKey")

                result["properties"] = current.get("properties")

                result["retentionTillDate"] = current.get("retentionTillDate")

                result["roles"] = current.get("roles")

                result["self"] = current.get("self")

                result["simplified"] = current.get("simplified")

                result["style"] = current.get("style")

                result["url"] = current.get("url")

                result["uuid"] = current.get("uuid")

                result["versions"] = current.get("versions")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/project/{projectIdOrKey}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
