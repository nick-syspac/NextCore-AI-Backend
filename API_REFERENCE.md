# RTOComply AI Cloud - Control Plane API
Version: 1.0.0

REST API for RTO Comply AI Backend - Comprehensive compliance and education management platform

## Endpoints
### api-keys
#### GET /api/api-keys/
`GET /api/api-keys/`

ViewSet for managing tenant API keys.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTenantAPIKeyList |

---

#### POST /api/api-keys/
`POST /api/api-keys/`

ViewSet for managing tenant API keys.


#### Request Body
Type: `TenantAPIKeyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TenantAPIKey |

---

#### GET /api/api-keys/{id}/
`GET /api/api-keys/{id}/`

ViewSet for managing tenant API keys.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant api key. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantAPIKey |

---

#### PUT /api/api-keys/{id}/
`PUT /api/api-keys/{id}/`

ViewSet for managing tenant API keys.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant api key. |

#### Request Body
Type: `TenantAPIKeyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantAPIKey |

---

#### PATCH /api/api-keys/{id}/
`PATCH /api/api-keys/{id}/`

ViewSet for managing tenant API keys.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant api key. |

#### Request Body
Type: `PatchedTenantAPIKeyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantAPIKey |

---

#### DELETE /api/api-keys/{id}/
`DELETE /api/api-keys/{id}/`

ViewSet for managing tenant API keys.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant api key. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/api-keys/{id}/revoke/
`POST /api/api-keys/{id}/revoke/`

Revoke an API key.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant api key. |

#### Request Body
Type: `TenantAPIKeyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantAPIKey |

---

### audit
#### GET /api/audit/events/
`GET /api/audit/events/`

List audit events with optional filtering.

Query parameters:
- tenant_id: Filter by tenant ID
- event_type: Filter by event type
- since: Filter events after this timestamp (ISO format)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| event_type | query | string | No |  |
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_id | query | string | No |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAuditList |

---

#### GET /api/audit/verify/
`GET /api/audit/verify/`

Verify the audit chain integrity.

Query parameters:
- tenant_id: Verify chain for specific tenant (optional)

Returns:
    Response with verification status and details



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

### auth
#### POST /api/auth/token/
`POST /api/auth/token/`

#### Request Body
Type: `AuthTokenRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthToken |

---

### competency-gap
#### GET /api/competency-gap/assignments/
`GET /api/competency-gap/assignments/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTrainerAssignmentList |

---

#### POST /api/competency-gap/assignments/
`POST /api/competency-gap/assignments/`

#### Request Body
Type: `TrainerAssignmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TrainerAssignment |

---

#### GET /api/competency-gap/assignments/{id}/
`GET /api/competency-gap/assignments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer assignment. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerAssignment |

---

#### PUT /api/competency-gap/assignments/{id}/
`PUT /api/competency-gap/assignments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer assignment. |

#### Request Body
Type: `TrainerAssignmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerAssignment |

---

#### PATCH /api/competency-gap/assignments/{id}/
`PATCH /api/competency-gap/assignments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer assignment. |

#### Request Body
Type: `PatchedTrainerAssignmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerAssignment |

---

#### DELETE /api/competency-gap/assignments/{id}/
`DELETE /api/competency-gap/assignments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer assignment. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/competency-gap/compliance-checks/
`GET /api/competency-gap/compliance-checks/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedComplianceCheckList |

---

#### POST /api/competency-gap/compliance-checks/
`POST /api/competency-gap/compliance-checks/`

#### Request Body
Type: `ComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ComplianceCheck |

---

#### GET /api/competency-gap/compliance-checks/{id}/
`GET /api/competency-gap/compliance-checks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### PUT /api/competency-gap/compliance-checks/{id}/
`PUT /api/competency-gap/compliance-checks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |

#### Request Body
Type: `ComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### PATCH /api/competency-gap/compliance-checks/{id}/
`PATCH /api/competency-gap/compliance-checks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |

#### Request Body
Type: `PatchedComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### DELETE /api/competency-gap/compliance-checks/{id}/
`DELETE /api/competency-gap/compliance-checks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/competency-gap/gaps/
`GET /api/competency-gap/gaps/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCompetencyGapList |

---

#### POST /api/competency-gap/gaps/
`POST /api/competency-gap/gaps/`

#### Request Body
Type: `CompetencyGapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CompetencyGap |

---

#### GET /api/competency-gap/gaps/{id}/
`GET /api/competency-gap/gaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this competency gap. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CompetencyGap |

---

#### PUT /api/competency-gap/gaps/{id}/
`PUT /api/competency-gap/gaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this competency gap. |

#### Request Body
Type: `CompetencyGapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CompetencyGap |

---

#### PATCH /api/competency-gap/gaps/{id}/
`PATCH /api/competency-gap/gaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this competency gap. |

#### Request Body
Type: `PatchedCompetencyGapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CompetencyGap |

---

#### DELETE /api/competency-gap/gaps/{id}/
`DELETE /api/competency-gap/gaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this competency gap. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/competency-gap/mappings/
`GET /api/competency-gap/mappings/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedQualificationMappingList |

---

#### POST /api/competency-gap/mappings/
`POST /api/competency-gap/mappings/`

#### Request Body
Type: `QualificationMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | QualificationMapping |

---

#### GET /api/competency-gap/mappings/{id}/
`GET /api/competency-gap/mappings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this qualification mapping. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | QualificationMapping |

---

#### PUT /api/competency-gap/mappings/{id}/
`PUT /api/competency-gap/mappings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this qualification mapping. |

#### Request Body
Type: `QualificationMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | QualificationMapping |

---

#### PATCH /api/competency-gap/mappings/{id}/
`PATCH /api/competency-gap/mappings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this qualification mapping. |

#### Request Body
Type: `PatchedQualificationMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | QualificationMapping |

---

#### DELETE /api/competency-gap/mappings/{id}/
`DELETE /api/competency-gap/mappings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this qualification mapping. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/competency-gap/qualifications/
`GET /api/competency-gap/qualifications/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTrainerQualificationList |

---

#### POST /api/competency-gap/qualifications/
`POST /api/competency-gap/qualifications/`

#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TrainerQualification |

---

#### GET /api/competency-gap/qualifications/{id}/
`GET /api/competency-gap/qualifications/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer qualification. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### PUT /api/competency-gap/qualifications/{id}/
`PUT /api/competency-gap/qualifications/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer qualification. |

#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### PATCH /api/competency-gap/qualifications/{id}/
`PATCH /api/competency-gap/qualifications/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer qualification. |

#### Request Body
Type: `PatchedTrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### DELETE /api/competency-gap/qualifications/{id}/
`DELETE /api/competency-gap/qualifications/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer qualification. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/competency-gap/qualifications/assign_trainer/
`POST /api/competency-gap/qualifications/assign_trainer/`

Assign a trainer to a unit with compliance checking


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### POST /api/competency-gap/qualifications/bulk_assign/
`POST /api/competency-gap/qualifications/bulk_assign/`

Bulk assign a trainer to multiple units


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### POST /api/competency-gap/qualifications/check_gaps/
`POST /api/competency-gap/qualifications/check_gaps/`

Check for competency gaps for a trainer-unit pair


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### GET /api/competency-gap/qualifications/dashboard/
`GET /api/competency-gap/qualifications/dashboard/`

Get dashboard statistics



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### POST /api/competency-gap/qualifications/generate_compliance_report/
`POST /api/competency-gap/qualifications/generate_compliance_report/`

Generate detailed compliance report


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### POST /api/competency-gap/qualifications/graph_analysis/
`POST /api/competency-gap/qualifications/graph_analysis/`

Perform graph-based analysis of qualifications and competencies


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### POST /api/competency-gap/qualifications/validate_matrix/
`POST /api/competency-gap/qualifications/validate_matrix/`

Validate the entire trainer matrix for compliance


#### Request Body
Type: `TrainerQualificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerQualification |

---

#### GET /api/competency-gap/units/
`GET /api/competency-gap/units/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedUnitOfCompetencyList |

---

#### POST /api/competency-gap/units/
`POST /api/competency-gap/units/`

#### Request Body
Type: `UnitOfCompetencyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | UnitOfCompetency |

---

#### GET /api/competency-gap/units/{id}/
`GET /api/competency-gap/units/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this unit of competency. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UnitOfCompetency |

---

#### PUT /api/competency-gap/units/{id}/
`PUT /api/competency-gap/units/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this unit of competency. |

#### Request Body
Type: `UnitOfCompetencyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UnitOfCompetency |

---

#### PATCH /api/competency-gap/units/{id}/
`PATCH /api/competency-gap/units/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this unit of competency. |

#### Request Body
Type: `PatchedUnitOfCompetencyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UnitOfCompetency |

---

#### DELETE /api/competency-gap/units/{id}/
`DELETE /api/competency-gap/units/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this unit of competency. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

### email-assistant
#### GET /api/email-assistant/drafts/
`GET /api/email-assistant/drafts/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedDraftReplyList |

---

#### POST /api/email-assistant/drafts/
`POST /api/email-assistant/drafts/`

#### Request Body
Type: `DraftReplyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | DraftReply |

---

#### GET /api/email-assistant/drafts/{id}/
`GET /api/email-assistant/drafts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this draft reply. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DraftReply |

---

#### PUT /api/email-assistant/drafts/{id}/
`PUT /api/email-assistant/drafts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this draft reply. |

#### Request Body
Type: `DraftReplyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DraftReply |

---

#### PATCH /api/email-assistant/drafts/{id}/
`PATCH /api/email-assistant/drafts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this draft reply. |

#### Request Body
Type: `PatchedDraftReplyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DraftReply |

---

#### DELETE /api/email-assistant/drafts/{id}/
`DELETE /api/email-assistant/drafts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this draft reply. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/email-assistant/history/
`GET /api/email-assistant/history/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedReplyHistoryList |

---

#### POST /api/email-assistant/history/
`POST /api/email-assistant/history/`

#### Request Body
Type: `ReplyHistoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ReplyHistory |

---

#### GET /api/email-assistant/history/{id}/
`GET /api/email-assistant/history/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reply history. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReplyHistory |

---

#### PUT /api/email-assistant/history/{id}/
`PUT /api/email-assistant/history/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reply history. |

#### Request Body
Type: `ReplyHistoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReplyHistory |

---

#### PATCH /api/email-assistant/history/{id}/
`PATCH /api/email-assistant/history/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reply history. |

#### Request Body
Type: `PatchedReplyHistoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReplyHistory |

---

#### DELETE /api/email-assistant/history/{id}/
`DELETE /api/email-assistant/history/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reply history. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/email-assistant/messages/
`GET /api/email-assistant/messages/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedStudentMessageList |

---

#### POST /api/email-assistant/messages/
`POST /api/email-assistant/messages/`

#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | StudentMessage |

---

#### GET /api/email-assistant/messages/{id}/
`GET /api/email-assistant/messages/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student message. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### PUT /api/email-assistant/messages/{id}/
`PUT /api/email-assistant/messages/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student message. |

#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### PATCH /api/email-assistant/messages/{id}/
`PATCH /api/email-assistant/messages/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student message. |

#### Request Body
Type: `PatchedStudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### DELETE /api/email-assistant/messages/{id}/
`DELETE /api/email-assistant/messages/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student message. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/email-assistant/messages/analyze_sentiment/
`POST /api/email-assistant/messages/analyze_sentiment/`

Analyze sentiment and urgency of a message


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### GET /api/email-assistant/messages/dashboard/
`GET /api/email-assistant/messages/dashboard/`

Get dashboard statistics and metrics



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### POST /api/email-assistant/messages/generate_reply/
`POST /api/email-assistant/messages/generate_reply/`

Generate AI draft reply to a student message


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### POST /api/email-assistant/messages/refine_tone/
`POST /api/email-assistant/messages/refine_tone/`

Refine the tone of an existing draft


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### POST /api/email-assistant/messages/save_template/
`POST /api/email-assistant/messages/save_template/`

Save a draft or custom text as a reusable template


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### POST /api/email-assistant/messages/send_reply/
`POST /api/email-assistant/messages/send_reply/`

Mark a draft as sent and record metrics


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### POST /api/email-assistant/messages/suggest_replies/
`POST /api/email-assistant/messages/suggest_replies/`

Generate multiple reply suggestions with different tones


#### Request Body
Type: `StudentMessageRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentMessage |

---

#### GET /api/email-assistant/templates/
`GET /api/email-assistant/templates/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMessageTemplateList |

---

#### POST /api/email-assistant/templates/
`POST /api/email-assistant/templates/`

#### Request Body
Type: `MessageTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MessageTemplate |

---

#### GET /api/email-assistant/templates/{id}/
`GET /api/email-assistant/templates/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this message template. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MessageTemplate |

---

#### PUT /api/email-assistant/templates/{id}/
`PUT /api/email-assistant/templates/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this message template. |

#### Request Body
Type: `MessageTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MessageTemplate |

---

#### PATCH /api/email-assistant/templates/{id}/
`PATCH /api/email-assistant/templates/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this message template. |

#### Request Body
Type: `PatchedMessageTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MessageTemplate |

---

#### DELETE /api/email-assistant/templates/{id}/
`DELETE /api/email-assistant/templates/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this message template. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/email-assistant/threads/
`GET /api/email-assistant/threads/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedConversationThreadList |

---

#### POST /api/email-assistant/threads/
`POST /api/email-assistant/threads/`

#### Request Body
Type: `ConversationThreadRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ConversationThread |

---

#### GET /api/email-assistant/threads/{id}/
`GET /api/email-assistant/threads/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this conversation thread. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ConversationThread |

---

#### PUT /api/email-assistant/threads/{id}/
`PUT /api/email-assistant/threads/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this conversation thread. |

#### Request Body
Type: `ConversationThreadRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ConversationThread |

---

#### PATCH /api/email-assistant/threads/{id}/
`PATCH /api/email-assistant/threads/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this conversation thread. |

#### Request Body
Type: `PatchedConversationThreadRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ConversationThread |

---

#### DELETE /api/email-assistant/threads/{id}/
`DELETE /api/email-assistant/threads/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this conversation thread. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/email-assistant/tone-profiles/
`GET /api/email-assistant/tone-profiles/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedToneProfileList |

---

#### POST /api/email-assistant/tone-profiles/
`POST /api/email-assistant/tone-profiles/`

#### Request Body
Type: `ToneProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ToneProfile |

---

#### GET /api/email-assistant/tone-profiles/{id}/
`GET /api/email-assistant/tone-profiles/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this tone profile. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ToneProfile |

---

#### PUT /api/email-assistant/tone-profiles/{id}/
`PUT /api/email-assistant/tone-profiles/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this tone profile. |

#### Request Body
Type: `ToneProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ToneProfile |

---

#### PATCH /api/email-assistant/tone-profiles/{id}/
`PATCH /api/email-assistant/tone-profiles/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this tone profile. |

#### Request Body
Type: `PatchedToneProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ToneProfile |

---

#### DELETE /api/email-assistant/tone-profiles/{id}/
`DELETE /api/email-assistant/tone-profiles/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this tone profile. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

### industry-currency
#### GET /api/industry-currency/entity-extractions/
`GET /api/industry-currency/entity-extractions/`

ViewSet for entity extractions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEntityExtractionList |

---

#### POST /api/industry-currency/entity-extractions/
`POST /api/industry-currency/entity-extractions/`

ViewSet for entity extractions


#### Request Body
Type: `EntityExtractionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EntityExtraction |

---

#### GET /api/industry-currency/entity-extractions/{id}/
`GET /api/industry-currency/entity-extractions/{id}/`

ViewSet for entity extractions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this entity extraction. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EntityExtraction |

---

#### PUT /api/industry-currency/entity-extractions/{id}/
`PUT /api/industry-currency/entity-extractions/{id}/`

ViewSet for entity extractions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this entity extraction. |

#### Request Body
Type: `EntityExtractionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EntityExtraction |

---

#### PATCH /api/industry-currency/entity-extractions/{id}/
`PATCH /api/industry-currency/entity-extractions/{id}/`

ViewSet for entity extractions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this entity extraction. |

#### Request Body
Type: `PatchedEntityExtractionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EntityExtraction |

---

#### DELETE /api/industry-currency/entity-extractions/{id}/
`DELETE /api/industry-currency/entity-extractions/{id}/`

ViewSet for entity extractions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this entity extraction. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/industry-currency/evidence/
`GET /api/industry-currency/evidence/`

ViewSet for currency evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCurrencyEvidenceList |

---

#### POST /api/industry-currency/evidence/
`POST /api/industry-currency/evidence/`

ViewSet for currency evidence documents


#### Request Body
Type: `CurrencyEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CurrencyEvidence |

---

#### GET /api/industry-currency/evidence/{id}/
`GET /api/industry-currency/evidence/{id}/`

ViewSet for currency evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this currency evidence. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CurrencyEvidence |

---

#### PUT /api/industry-currency/evidence/{id}/
`PUT /api/industry-currency/evidence/{id}/`

ViewSet for currency evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this currency evidence. |

#### Request Body
Type: `CurrencyEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CurrencyEvidence |

---

#### PATCH /api/industry-currency/evidence/{id}/
`PATCH /api/industry-currency/evidence/{id}/`

ViewSet for currency evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this currency evidence. |

#### Request Body
Type: `PatchedCurrencyEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CurrencyEvidence |

---

#### DELETE /api/industry-currency/evidence/{id}/
`DELETE /api/industry-currency/evidence/{id}/`

ViewSet for currency evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this currency evidence. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/industry-currency/github-activities/
`GET /api/industry-currency/github-activities/`

ViewSet for GitHub activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedGitHubActivityList |

---

#### POST /api/industry-currency/github-activities/
`POST /api/industry-currency/github-activities/`

ViewSet for GitHub activities


#### Request Body
Type: `GitHubActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | GitHubActivity |

---

#### GET /api/industry-currency/github-activities/{id}/
`GET /api/industry-currency/github-activities/{id}/`

ViewSet for GitHub activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this git hub activity. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GitHubActivity |

---

#### PUT /api/industry-currency/github-activities/{id}/
`PUT /api/industry-currency/github-activities/{id}/`

ViewSet for GitHub activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this git hub activity. |

#### Request Body
Type: `GitHubActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GitHubActivity |

---

#### PATCH /api/industry-currency/github-activities/{id}/
`PATCH /api/industry-currency/github-activities/{id}/`

ViewSet for GitHub activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this git hub activity. |

#### Request Body
Type: `PatchedGitHubActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GitHubActivity |

---

#### DELETE /api/industry-currency/github-activities/{id}/
`DELETE /api/industry-currency/github-activities/{id}/`

ViewSet for GitHub activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this git hub activity. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/industry-currency/linkedin-activities/
`GET /api/industry-currency/linkedin-activities/`

ViewSet for LinkedIn activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedLinkedInActivityList |

---

#### POST /api/industry-currency/linkedin-activities/
`POST /api/industry-currency/linkedin-activities/`

ViewSet for LinkedIn activities


#### Request Body
Type: `LinkedInActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | LinkedInActivity |

---

#### GET /api/industry-currency/linkedin-activities/{id}/
`GET /api/industry-currency/linkedin-activities/{id}/`

ViewSet for LinkedIn activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this linked in activity. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LinkedInActivity |

---

#### PUT /api/industry-currency/linkedin-activities/{id}/
`PUT /api/industry-currency/linkedin-activities/{id}/`

ViewSet for LinkedIn activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this linked in activity. |

#### Request Body
Type: `LinkedInActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LinkedInActivity |

---

#### PATCH /api/industry-currency/linkedin-activities/{id}/
`PATCH /api/industry-currency/linkedin-activities/{id}/`

ViewSet for LinkedIn activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this linked in activity. |

#### Request Body
Type: `PatchedLinkedInActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LinkedInActivity |

---

#### DELETE /api/industry-currency/linkedin-activities/{id}/
`DELETE /api/industry-currency/linkedin-activities/{id}/`

ViewSet for LinkedIn activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this linked in activity. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/industry-currency/profiles/
`GET /api/industry-currency/profiles/`

ViewSet for trainer profiles with industry currency verification

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTrainerProfileListList |

---

#### POST /api/industry-currency/profiles/
`POST /api/industry-currency/profiles/`

ViewSet for trainer profiles with industry currency verification


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TrainerProfile |

---

#### GET /api/industry-currency/profiles/{id}/
`GET /api/industry-currency/profiles/{id}/`

ViewSet for trainer profiles with industry currency verification

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### PUT /api/industry-currency/profiles/{id}/
`PUT /api/industry-currency/profiles/{id}/`

ViewSet for trainer profiles with industry currency verification

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |

#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### PATCH /api/industry-currency/profiles/{id}/
`PATCH /api/industry-currency/profiles/{id}/`

ViewSet for trainer profiles with industry currency verification

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |

#### Request Body
Type: `PatchedTrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### DELETE /api/industry-currency/profiles/{id}/
`DELETE /api/industry-currency/profiles/{id}/`

ViewSet for trainer profiles with industry currency verification

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/industry-currency/profiles/analyze-currency/
`POST /api/industry-currency/profiles/analyze-currency/`

Analyze industry currency based on scan results
POST /api/industry-currency/profiles/analyze-currency/
Body: {scan_id, industry, specializations, recency_weight, relevance_weight, frequency_weight}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### GET /api/industry-currency/profiles/dashboard/
`GET /api/industry-currency/profiles/dashboard/`

Get dashboard statistics
GET /api/industry-currency/profiles/dashboard/?tenant=X



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/extract-entities/
`POST /api/industry-currency/profiles/extract-entities/`

Extract entities from text using NLP
POST /api/industry-currency/profiles/extract-entities/
Body: {scan_id, source_type, source_text, source_url, nlp_model}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/generate-evidence/
`POST /api/industry-currency/profiles/generate-evidence/`

Generate currency evidence document
POST /api/industry-currency/profiles/generate-evidence/
Body: {scan_id, evidence_type, file_format, include_raw_data, start_date, end_date}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/scan-github/
`POST /api/industry-currency/profiles/scan-github/`

Scan GitHub profile for industry currency evidence
POST /api/industry-currency/profiles/scan-github/
Body: {scan_id, github_username, extract_repos, extract_commits, max_items}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/scan-linkedin/
`POST /api/industry-currency/profiles/scan-linkedin/`

Scan LinkedIn profile for industry currency evidence
POST /api/industry-currency/profiles/scan-linkedin/
Body: {scan_id, linkedin_url, extract_posts, extract_certifications, max_items}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/start-scan/
`POST /api/industry-currency/profiles/start-scan/`

Start a verification scan for a trainer profile
POST /api/industry-currency/profiles/start-scan/
Body: {profile_id, scan_type, sources_to_scan, linkedin_url, github_url}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### POST /api/industry-currency/profiles/verify-profile/
`POST /api/industry-currency/profiles/verify-profile/`

Complete profile verification workflow
POST /api/industry-currency/profiles/verify-profile/
Body: {profile_id, scan_linkedin, scan_github, analyze_currency, generate_evidence}


#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### GET /api/industry-currency/scans/
`GET /api/industry-currency/scans/`

ViewSet for verification scans

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedVerificationScanListList |

---

#### POST /api/industry-currency/scans/
`POST /api/industry-currency/scans/`

ViewSet for verification scans


#### Request Body
Type: `VerificationScanRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | VerificationScan |

---

#### GET /api/industry-currency/scans/{id}/
`GET /api/industry-currency/scans/{id}/`

ViewSet for verification scans

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this verification scan. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | VerificationScan |

---

#### PUT /api/industry-currency/scans/{id}/
`PUT /api/industry-currency/scans/{id}/`

ViewSet for verification scans

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this verification scan. |

#### Request Body
Type: `VerificationScanRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | VerificationScan |

---

#### PATCH /api/industry-currency/scans/{id}/
`PATCH /api/industry-currency/scans/{id}/`

ViewSet for verification scans

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this verification scan. |

#### Request Body
Type: `PatchedVerificationScanRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | VerificationScan |

---

#### DELETE /api/industry-currency/scans/{id}/
`DELETE /api/industry-currency/scans/{id}/`

ViewSet for verification scans

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this verification scan. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

### tenant-users
#### GET /api/tenant-users/
`GET /api/tenant-users/`

ViewSet for managing tenant user relationships.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTenantUserList |

---

#### POST /api/tenant-users/
`POST /api/tenant-users/`

ViewSet for managing tenant user relationships.


#### Request Body
Type: `TenantUserRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TenantUser |

---

#### GET /api/tenant-users/{id}/
`GET /api/tenant-users/{id}/`

ViewSet for managing tenant user relationships.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant user. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantUser |

---

#### PUT /api/tenant-users/{id}/
`PUT /api/tenant-users/{id}/`

ViewSet for managing tenant user relationships.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant user. |

#### Request Body
Type: `TenantUserRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantUser |

---

#### PATCH /api/tenant-users/{id}/
`PATCH /api/tenant-users/{id}/`

ViewSet for managing tenant user relationships.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant user. |

#### Request Body
Type: `PatchedTenantUserRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TenantUser |

---

#### DELETE /api/tenant-users/{id}/
`DELETE /api/tenant-users/{id}/`

ViewSet for managing tenant user relationships.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes | A UUID string identifying this tenant user. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

### tenants
#### GET /api/tenants/
`GET /api/tenants/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTenantList |

---

#### POST /api/tenants/
`POST /api/tenants/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.


#### Request Body
Type: `TenantCreateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TenantCreate |

---

#### GET /api/tenants/{slug}/
`GET /api/tenants/{slug}/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### PUT /api/tenants/{slug}/
`PUT /api/tenants/{slug}/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `TenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### PATCH /api/tenants/{slug}/
`PATCH /api/tenants/{slug}/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### DELETE /api/tenants/{slug}/
`DELETE /api/tenants/{slug}/`

ViewSet for managing tenants.

Provides CRUD operations and additional actions for tenant lifecycle management.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{slug}/activate/
`POST /api/tenants/{slug}/activate/`

Activate a tenant.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `TenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### GET /api/tenants/{slug}/quota/
`GET /api/tenants/{slug}/quota/`

Get quota information for a tenant.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### POST /api/tenants/{slug}/reset_quota/
`POST /api/tenants/{slug}/reset_quota/`

Reset monthly quotas for a tenant.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `TenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### POST /api/tenants/{slug}/restore/
`POST /api/tenants/{slug}/restore/`

Restore a suspended tenant.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `TenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### POST /api/tenants/{slug}/suspend/
`POST /api/tenants/{slug}/suspend/`

Suspend a tenant.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| slug | path | string | Yes |  |

#### Request Body
Type: `TenantRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Tenant |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedContentEmbeddingList |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ContentEmbeddingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ContentEmbedding |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Content Embedding. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ContentEmbedding |

---

#### PUT /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/
`PUT /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Content Embedding. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ContentEmbeddingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ContentEmbedding |

---

#### PATCH /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/
`PATCH /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Content Embedding. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedContentEmbeddingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ContentEmbedding |

---

#### DELETE /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/
`DELETE /api/tenants/{tenant_slug}/adaptive-pathway/embeddings/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Content Embedding. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedLearningPathwayList |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/pathways/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/pathways/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LearningPathwayRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | LearningPathway |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Pathway. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningPathway |

---

#### PUT /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/
`PUT /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Pathway. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LearningPathwayRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningPathway |

---

#### PATCH /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/
`PATCH /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Pathway. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedLearningPathwayRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningPathway |

---

#### DELETE /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/
`DELETE /api/tenants/{tenant_slug}/adaptive-pathway/pathways/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Pathway. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/completion_analytics/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/pathways/completion_analytics/`

Get completion rate analytics for pathways

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningPathway |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/pathways/recommend_pathway/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/pathways/recommend_pathway/`

Generate personalized learning pathway recommendations using
collaborative filtering + content embeddings (hybrid approach).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LearningPathwayRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningPathway |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/progress/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/progress/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedStudentProgressList |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/progress/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/progress/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `StudentProgressRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | StudentProgress |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Student Progress. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentProgress |

---

#### PUT /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/
`PUT /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Student Progress. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `StudentProgressRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentProgress |

---

#### PATCH /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/
`PATCH /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Student Progress. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedStudentProgressRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentProgress |

---

#### DELETE /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/
`DELETE /api/tenants/{tenant_slug}/adaptive-pathway/progress/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Student Progress. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedPathwayRecommendationList |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PathwayRecommendationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | PathwayRecommendation |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Pathway Recommendation. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PathwayRecommendation |

---

#### PUT /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/
`PUT /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Pathway Recommendation. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PathwayRecommendationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PathwayRecommendation |

---

#### PATCH /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/
`PATCH /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Pathway Recommendation. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedPathwayRecommendationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PathwayRecommendation |

---

#### DELETE /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/
`DELETE /api/tenants/{tenant_slug}/adaptive-pathway/recommendations/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Pathway Recommendation. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/steps/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/steps/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedLearningStepList |

---

#### POST /api/tenants/{tenant_slug}/adaptive-pathway/steps/
`POST /api/tenants/{tenant_slug}/adaptive-pathway/steps/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LearningStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | LearningStep |

---

#### GET /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/
`GET /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Step. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningStep |

---

#### PUT /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/
`PUT /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Step. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LearningStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningStep |

---

#### PATCH /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/
`PATCH /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Step. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedLearningStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LearningStep |

---

#### DELETE /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/
`DELETE /api/tenants/{tenant_slug}/adaptive-pathway/steps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Learning Step. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/assessments/
`GET /api/tenants/{tenant_slug}/assessment-builder/assessments/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAssessmentList |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/assessments/
`POST /api/tenants/{tenant_slug}/assessment-builder/assessments/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Assessment |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/
`GET /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentDetail |

---

#### PUT /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/
`PUT /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### PATCH /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/
`PATCH /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### DELETE /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/
`DELETE /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/analyze_blooms/
`POST /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/analyze_blooms/`

Analyze Bloom's taxonomy distribution in assessment

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/approve/
`POST /api/tenants/{tenant_slug}/assessment-builder/assessments/{id}/approve/`

Approve assessment for publishing

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/assessments/dashboard_stats/
`GET /api/tenants/{tenant_slug}/assessment-builder/assessments/dashboard_stats/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/assessments/generate_assessment/
`POST /api/tenants/{tenant_slug}/assessment-builder/assessments/generate_assessment/`

Generate assessment using GPT-4 from unit code

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Assessment |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/criteria/
`GET /api/tenants/{tenant_slug}/assessment-builder/criteria/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAssessmentCriteriaList |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/criteria/
`POST /api/tenants/{tenant_slug}/assessment-builder/criteria/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentCriteriaRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AssessmentCriteria |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/
`GET /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentCriteria |

---

#### PUT /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/
`PUT /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentCriteriaRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentCriteria |

---

#### PATCH /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/
`PATCH /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAssessmentCriteriaRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentCriteria |

---

#### DELETE /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/
`DELETE /api/tenants/{tenant_slug}/assessment-builder/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/tasks/
`GET /api/tenants/{tenant_slug}/assessment-builder/tasks/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAssessmentTaskList |

---

#### POST /api/tenants/{tenant_slug}/assessment-builder/tasks/
`POST /api/tenants/{tenant_slug}/assessment-builder/tasks/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentTaskRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AssessmentTask |

---

#### GET /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/
`GET /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentTask |

---

#### PUT /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/
`PUT /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessmentTaskRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentTask |

---

#### PATCH /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/
`PATCH /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAssessmentTaskRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessmentTask |

---

#### DELETE /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/
`DELETE /api/tenants/{tenant_slug}/assessment-builder/tasks/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/audit-reports/
`GET /api/tenants/{tenant_slug}/audit-assistant/audit-reports/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAuditReportList |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/
`POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuditReportRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AuditReport |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/
`GET /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditReportDetail |

---

#### PUT /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/
`PUT /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuditReportRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditReport |

---

#### PATCH /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/
`PATCH /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAuditReportRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditReport |

---

#### DELETE /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/
`DELETE /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/`

ViewSet for audit report management

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/generate_report/
`POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/generate_report/`

Generate clause-by-clause audit report with evidence mapping

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuditReportRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditReport |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/submit/
`POST /api/tenants/{tenant_slug}/audit-assistant/audit-reports/{id}/submit/`

Submit audit report (mark as submitted to ASQA)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuditReportRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditReport |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/
`GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedClauseEvidenceList |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/
`POST /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ClauseEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ClauseEvidence |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/
`GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseEvidence |

---

#### PUT /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/
`PUT /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ClauseEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseEvidence |

---

#### PATCH /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/
`PATCH /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedClauseEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseEvidence |

---

#### DELETE /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/
`DELETE /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/{id}/`

ViewSet for managing clause-evidence mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/gaps/
`GET /api/tenants/{tenant_slug}/audit-assistant/clause-evidence/gaps/`

Identify clauses with insufficient evidence (gap analysis)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseEvidence |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/evidence/
`GET /api/tenants/{tenant_slug}/audit-assistant/evidence/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEvidenceList |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/evidence/
`POST /api/tenants/{tenant_slug}/audit-assistant/evidence/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Evidence |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/
`GET /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### PUT /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/
`PUT /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### PATCH /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/
`PATCH /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### DELETE /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/
`DELETE /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/`

ViewSet for evidence document management with NER auto-tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/process_ner/
`POST /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/process_ner/`

Manually trigger NER processing and auto-tagging for an evidence document.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### GET /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/tagged_clauses/
`GET /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/tagged_clauses/`

Get all clauses tagged to this evidence with mapping details

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/verify_tagging/
`POST /api/tenants/{tenant_slug}/audit-assistant/evidence/{id}/verify_tagging/`

Verify/approve auto-tagged clauses for evidence

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### POST /api/tenants/{tenant_slug}/audit-assistant/evidence/upload/
`POST /api/tenants/{tenant_slug}/audit-assistant/evidence/upload/`

Upload evidence file and queue background processing.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Evidence |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/analyses/
`GET /api/tenants/{tenant_slug}/authenticity-check/analyses/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedSubmissionAnalysisListList |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/analyses/
`POST /api/tenants/{tenant_slug}/authenticity-check/analyses/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionAnalysisRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | SubmissionAnalysis |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/
`GET /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Submission Analysis. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionAnalysis |

---

#### PUT /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/
`PUT /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Submission Analysis. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionAnalysisRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionAnalysis |

---

#### PATCH /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/
`PATCH /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Submission Analysis. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedSubmissionAnalysisRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionAnalysis |

---

#### DELETE /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/
`DELETE /api/tenants/{tenant_slug}/authenticity-check/analyses/{id}/`

ViewSet for managing submission analyses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Submission Analysis. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/
`GET /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAnomalyDetectionList |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/
`POST /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AnomalyDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AnomalyDetection |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/
`GET /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Anomaly Detection. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AnomalyDetection |

---

#### PUT /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/
`PUT /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Anomaly Detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AnomalyDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AnomalyDetection |

---

#### PATCH /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/
`PATCH /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Anomaly Detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAnomalyDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AnomalyDetection |

---

#### DELETE /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/
`DELETE /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/`

ViewSet for managing anomaly detections

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Anomaly Detection. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/acknowledge/
`POST /api/tenants/{tenant_slug}/authenticity-check/anomaly-detections/{id}/acknowledge/`

Acknowledge anomaly with notes

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Anomaly Detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AnomalyDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AnomalyDetection |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/checks/
`GET /api/tenants/{tenant_slug}/authenticity-check/checks/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAuthenticityCheckListList |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/checks/
`POST /api/tenants/{tenant_slug}/authenticity-check/checks/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuthenticityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AuthenticityCheck |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/
`GET /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthenticityCheck |

---

#### PUT /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/
`PUT /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuthenticityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthenticityCheck |

---

#### PATCH /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/
`PATCH /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAuthenticityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthenticityCheck |

---

#### DELETE /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/
`DELETE /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/`

ViewSet for managing authenticity checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/check_authenticity/
`POST /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/check_authenticity/`

Run authenticity check on submission with plagiarism detection

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AuthenticityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthenticityCheck |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/integrity_report/
`GET /api/tenants/{tenant_slug}/authenticity-check/checks/{id}/integrity_report/`

Generate comprehensive integrity report

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Authenticity Check. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuthenticityCheck |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/
`GET /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMetadataVerificationList |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/
`POST /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MetadataVerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MetadataVerification |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/
`GET /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Metadata Verification. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MetadataVerification |

---

#### PUT /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/
`PUT /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Metadata Verification. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MetadataVerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MetadataVerification |

---

#### PATCH /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/
`PATCH /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Metadata Verification. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedMetadataVerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MetadataVerification |

---

#### DELETE /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/
`DELETE /api/tenants/{tenant_slug}/authenticity-check/metadata-verifications/{id}/`

ViewSet for managing metadata verifications

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Metadata Verification. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/
`GET /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedPlagiarismMatchList |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/
`POST /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PlagiarismMatchRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | PlagiarismMatch |

---

#### GET /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/
`GET /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Plagiarism Match. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PlagiarismMatch |

---

#### PUT /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/
`PUT /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Plagiarism Match. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PlagiarismMatchRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PlagiarismMatch |

---

#### PATCH /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/
`PATCH /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Plagiarism Match. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedPlagiarismMatchRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PlagiarismMatch |

---

#### DELETE /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/
`DELETE /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/`

ViewSet for managing plagiarism matches

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Plagiarism Match. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/mark_reviewed/
`POST /api/tenants/{tenant_slug}/authenticity-check/plagiarism-matches/{id}/mark_reviewed/`

Mark plagiarism match as reviewed

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Plagiarism Match. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PlagiarismMatchRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PlagiarismMatch |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/criteria/
`GET /api/tenants/{tenant_slug}/auto-marker/criteria/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMarkingCriterionList |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/criteria/
`POST /api/tenants/{tenant_slug}/auto-marker/criteria/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MarkingCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MarkingCriterion |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/
`GET /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marking criterion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkingCriterion |

---

#### PUT /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/
`PUT /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marking criterion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MarkingCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkingCriterion |

---

#### PATCH /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/
`PATCH /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marking criterion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedMarkingCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkingCriterion |

---

#### DELETE /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/
`DELETE /api/tenants/{tenant_slug}/auto-marker/criteria/{id}/`

ViewSet for managing marking criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marking criterion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/logs/
`GET /api/tenants/{tenant_slug}/auto-marker/logs/`

ViewSet for viewing marking logs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMarkingLogList |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/logs/{id}/
`GET /api/tenants/{tenant_slug}/auto-marker/logs/{id}/`

ViewSet for viewing marking logs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marking log. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkingLog |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/markers/
`GET /api/tenants/{tenant_slug}/auto-marker/markers/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAutoMarkerListList |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/markers/
`POST /api/tenants/{tenant_slug}/auto-marker/markers/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AutoMarkerDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AutoMarkerDetail |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/markers/{id}/
`GET /api/tenants/{tenant_slug}/auto-marker/markers/{id}/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### PUT /api/tenants/{tenant_slug}/auto-marker/markers/{id}/
`PUT /api/tenants/{tenant_slug}/auto-marker/markers/{id}/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AutoMarkerDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### PATCH /api/tenants/{tenant_slug}/auto-marker/markers/{id}/
`PATCH /api/tenants/{tenant_slug}/auto-marker/markers/{id}/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAutoMarkerDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### DELETE /api/tenants/{tenant_slug}/auto-marker/markers/{id}/
`DELETE /api/tenants/{tenant_slug}/auto-marker/markers/{id}/`

ViewSet for AutoMarker management and marking operations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/markers/{id}/mark_responses/
`POST /api/tenants/{tenant_slug}/auto-marker/markers/{id}/mark_responses/`

Mark multiple responses in batch with semantic similarity

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AutoMarkerDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/markers/{id}/mark_single/
`POST /api/tenants/{tenant_slug}/auto-marker/markers/{id}/mark_single/`

Mark a single response

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AutoMarkerDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/markers/{id}/statistics/
`GET /api/tenants/{tenant_slug}/auto-marker/markers/{id}/statistics/`

Get detailed statistics for this auto-marker

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this auto marker. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AutoMarkerDetail |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/responses/
`GET /api/tenants/{tenant_slug}/auto-marker/responses/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMarkedResponseListList |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/responses/
`POST /api/tenants/{tenant_slug}/auto-marker/responses/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MarkedResponseDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MarkedResponseDetail |

---

#### GET /api/tenants/{tenant_slug}/auto-marker/responses/{id}/
`GET /api/tenants/{tenant_slug}/auto-marker/responses/{id}/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marked response. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkedResponseDetail |

---

#### PUT /api/tenants/{tenant_slug}/auto-marker/responses/{id}/
`PUT /api/tenants/{tenant_slug}/auto-marker/responses/{id}/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marked response. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MarkedResponseDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkedResponseDetail |

---

#### PATCH /api/tenants/{tenant_slug}/auto-marker/responses/{id}/
`PATCH /api/tenants/{tenant_slug}/auto-marker/responses/{id}/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marked response. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedMarkedResponseDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkedResponseDetail |

---

#### DELETE /api/tenants/{tenant_slug}/auto-marker/responses/{id}/
`DELETE /api/tenants/{tenant_slug}/auto-marker/responses/{id}/`

ViewSet for viewing and managing marked responses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marked response. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/auto-marker/responses/{id}/review/
`POST /api/tenants/{tenant_slug}/auto-marker/responses/{id}/review/`

Review and potentially adjust a marked response

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this marked response. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MarkedResponseDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MarkedResponseDetail |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/actions/
`GET /api/tenants/{tenant_slug}/continuous-improvement/actions/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedImprovementActionList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ImprovementAction |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/{id}/ai_classify/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/{id}/ai_classify/`

Trigger AI classification for an action

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/{id}/ai_summarize/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/{id}/ai_summarize/`

Generate AI summary for an action

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/compliance_dashboard/
`GET /api/tenants/{tenant_slug}/continuous-improvement/actions-cir/compliance_dashboard/`

Get comprehensive compliance dashboard data

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementActionDetail |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/`

ViewSet for improvement actions with AI classification and tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/add_tracking/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/add_tracking/`

Add a tracking update to an improvement action

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/approve/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/approve/`

Approve an improvement action

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/classify/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions/{id}/classify/`

Trigger AI classification and summarization for an action

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/actions/classify_text/
`POST /api/tenants/{tenant_slug}/continuous-improvement/actions/classify_text/`

Classify text without creating an action (for preview)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/actions/compliance_overview/
`GET /api/tenants/{tenant_slug}/continuous-improvement/actions/compliance_overview/`

Get compliance overview with trend analysis

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/actions/dashboard_stats/
`GET /api/tenants/{tenant_slug}/continuous-improvement/actions/dashboard_stats/`

Get dashboard statistics for real-time compliance tracking

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementAction |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/ai-runs/
`GET /api/tenants/{tenant_slug}/continuous-improvement/ai-runs/`

ViewSet for AI run logs (read-only audit trail)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAIRunList |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/ai-runs/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/ai-runs/{id}/`

ViewSet for AI run logs (read-only audit trail)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AIRun |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/attachments/
`GET /api/tenants/{tenant_slug}/continuous-improvement/attachments/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAttachmentList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/attachments/
`POST /api/tenants/{tenant_slug}/continuous-improvement/attachments/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Attachment |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Attachment |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Attachment |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Attachment |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/attachments/{id}/`

ViewSet for file attachments

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/categories/
`GET /api/tenants/{tenant_slug}/continuous-improvement/categories/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedImprovementCategoryList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/categories/
`POST /api/tenants/{tenant_slug}/continuous-improvement/categories/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementCategoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ImprovementCategory |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Category. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementCategory |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Category. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementCategoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementCategory |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Category. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedImprovementCategoryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementCategory |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/categories/{id}/`

ViewSet for managing improvement categories

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Category. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/
`GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedClauseLinkList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/clause-links/
`POST /api/tenants/{tenant_slug}/continuous-improvement/clause-links/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ClauseLinkRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ClauseLink |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseLink |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ClauseLinkRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseLink |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedClauseLinkRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseLink |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/`

ViewSet for clause-action links

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/review/
`POST /api/tenants/{tenant_slug}/continuous-improvement/clause-links/{id}/review/`

Review and approve a clause link

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ClauseLinkRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseLink |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/by_clause/
`GET /api/tenants/{tenant_slug}/continuous-improvement/clause-links/by_clause/`

Get all actions linked to a specific clause

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ClauseLink |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/comments/
`GET /api/tenants/{tenant_slug}/continuous-improvement/comments/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCommentList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/comments/
`POST /api/tenants/{tenant_slug}/continuous-improvement/comments/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CommentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Comment |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CommentDetail |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CommentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Comment |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedCommentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Comment |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/comments/{id}/`

ViewSet for comments on improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/
`GET /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/`

ViewSet for KPI snapshots (read-only, computed via tasks)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedKPISnapshotList |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/{id}/`

ViewSet for KPI snapshots (read-only, computed via tasks)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | KPISnapshot |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/compute/
`POST /api/tenants/{tenant_slug}/continuous-improvement/kpi-snapshots/compute/`

Trigger KPI snapshot computation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `KPISnapshotRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | KPISnapshot |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/reviews/
`GET /api/tenants/{tenant_slug}/continuous-improvement/reviews/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedImprovementReviewList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/
`POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementReviewRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ImprovementReview |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementReview |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementReviewRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementReview |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedImprovementReviewRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementReview |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/`

ViewSet for improvement reviews

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/calculate_stats/
`POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/calculate_stats/`

Calculate review statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementReviewRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementReview |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/generate_ai_insights/
`POST /api/tenants/{tenant_slug}/continuous-improvement/reviews/{id}/generate_ai_insights/`

Generate AI insights for a review

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Improvement Review. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ImprovementReviewRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ImprovementReview |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/
`GET /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedSLAPolicyList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/
`POST /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SLAPolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | SLAPolicy |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SLAPolicy |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SLAPolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SLAPolicy |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedSLAPolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SLAPolicy |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/sla-policies/{id}/`

ViewSet for SLA policies

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/steps/
`GET /api/tenants/{tenant_slug}/continuous-improvement/steps/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedActionStepList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/steps/
`POST /api/tenants/{tenant_slug}/continuous-improvement/steps/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ActionStep |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionStep |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionStep |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedActionStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionStep |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/`

ViewSet for action steps within improvement actions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/block/
`POST /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/block/`

Mark a step as blocked

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionStep |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/complete/
`POST /api/tenants/{tenant_slug}/continuous-improvement/steps/{id}/complete/`

Mark a step as completed

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionStepRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionStep |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/
`GET /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTaxonomyLabelList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/
`POST /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TaxonomyLabelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TaxonomyLabel |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TaxonomyLabel |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TaxonomyLabelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TaxonomyLabel |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTaxonomyLabelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TaxonomyLabel |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/taxonomy-labels/{id}/`

ViewSet for taxonomy labels

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/tracking/
`GET /api/tenants/{tenant_slug}/continuous-improvement/tracking/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedActionTrackingList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/tracking/
`POST /api/tenants/{tenant_slug}/continuous-improvement/tracking/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionTrackingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ActionTracking |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Action Tracking Update. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionTracking |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Action Tracking Update. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ActionTrackingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionTracking |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Action Tracking Update. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedActionTrackingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ActionTracking |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/tracking/{id}/`

ViewSet for action tracking updates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Action Tracking Update. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/verifications/
`GET /api/tenants/{tenant_slug}/continuous-improvement/verifications/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedVerificationList |

---

#### POST /api/tenants/{tenant_slug}/continuous-improvement/verifications/
`POST /api/tenants/{tenant_slug}/continuous-improvement/verifications/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `VerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Verification |

---

#### GET /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/
`GET /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Verification |

---

#### PUT /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/
`PUT /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `VerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Verification |

---

#### PATCH /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/
`PATCH /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedVerificationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Verification |

---

#### DELETE /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/
`DELETE /api/tenants/{tenant_slug}/continuous-improvement/verifications/{id}/`

ViewSet for verification records

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/alerts/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/alerts/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEngagementAlertList |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/alerts/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/alerts/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementAlertRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EngagementAlert |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Alert. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementAlert |

---

#### PUT /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/
`PUT /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Alert. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementAlertRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementAlert |

---

#### PATCH /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/
`PATCH /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Alert. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEngagementAlertRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementAlert |

---

#### DELETE /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/
`DELETE /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Alert. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/acknowledge/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/alerts/{id}/acknowledge/`

Acknowledge an alert

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Alert. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementAlertRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementAlert |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/attendance/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/attendance/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAttendanceRecordList |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/attendance/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/attendance/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AttendanceRecordRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AttendanceRecord |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Attendance Record. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AttendanceRecord |

---

#### PUT /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/
`PUT /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Attendance Record. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AttendanceRecordRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AttendanceRecord |

---

#### PATCH /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/
`PATCH /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Attendance Record. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAttendanceRecordRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AttendanceRecord |

---

#### DELETE /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/
`DELETE /api/tenants/{tenant_slug}/engagement-heatmap/attendance/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Attendance Record. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEngagementHeatmapList |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementHeatmapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EngagementHeatmap |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Heatmap. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementHeatmap |

---

#### PUT /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/
`PUT /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Heatmap. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementHeatmapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementHeatmap |

---

#### PATCH /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/
`PATCH /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Heatmap. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEngagementHeatmapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementHeatmap |

---

#### DELETE /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/
`DELETE /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Engagement Heatmap. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/generate_heatmap/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/generate_heatmap/`

Generate engagement heatmap with attendance tracking, LMS activity analysis,
and sentiment analysis of discussions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EngagementHeatmapRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementHeatmap |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/risk_dashboard/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/heatmaps/risk_dashboard/`

Visual risk dashboard with aggregated metrics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EngagementHeatmap |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedLMSActivityList |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LMSActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | LMSActivity |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this LMS Activity. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LMSActivity |

---

#### PUT /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/
`PUT /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this LMS Activity. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `LMSActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LMSActivity |

---

#### PATCH /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/
`PATCH /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this LMS Activity. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedLMSActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | LMSActivity |

---

#### DELETE /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/
`DELETE /api/tenants/{tenant_slug}/engagement-heatmap/lms-activity/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this LMS Activity. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedDiscussionSentimentList |

---

#### POST /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/
`POST /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `DiscussionSentimentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | DiscussionSentiment |

---

#### GET /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/
`GET /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Discussion Sentiment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiscussionSentiment |

---

#### PUT /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/
`PUT /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Discussion Sentiment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `DiscussionSentimentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiscussionSentiment |

---

#### PATCH /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/
`PATCH /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Discussion Sentiment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedDiscussionSentimentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiscussionSentiment |

---

#### DELETE /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/
`DELETE /api/tenants/{tenant_slug}/engagement-heatmap/sentiment/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this Discussion Sentiment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/audit/
`GET /api/tenants/{tenant_slug}/evidence-mapper/audit/`

ViewSet for viewing evidence audit logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEvidenceAuditList |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/audit/{id}/
`GET /api/tenants/{tenant_slug}/evidence-mapper/audit/{id}/`

ViewSet for viewing evidence audit logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence audit. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceAudit |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/
`GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEvidenceMappingList |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/mappings/
`POST /api/tenants/{tenant_slug}/evidence-mapper/mappings/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EvidenceMapping |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/
`GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence mapping. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceMapping |

---

#### PUT /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/
`PUT /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence mapping. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceMapping |

---

#### PATCH /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/
`PATCH /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence mapping. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEvidenceMappingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceMapping |

---

#### DELETE /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/
`DELETE /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/`

ViewSet for managing evidence mappings with coverage tracking.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence mapping. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/coverage_report/
`GET /api/tenants/{tenant_slug}/evidence-mapper/mappings/{id}/coverage_report/`

Generate coverage report showing criteria with/without evidence.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence mapping. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceMapping |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/searches/
`GET /api/tenants/{tenant_slug}/evidence-mapper/searches/`

ViewSet for viewing embedding search logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEmbeddingSearchList |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/searches/{id}/
`GET /api/tenants/{tenant_slug}/evidence-mapper/searches/{id}/`

ViewSet for viewing embedding search logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this embedding search. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EmbeddingSearch |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/submissions/
`GET /api/tenants/{tenant_slug}/evidence-mapper/submissions/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedSubmissionEvidenceList |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/
`POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | SubmissionEvidence |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/
`GET /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidenceDetail |

---

#### PUT /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/
`PUT /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidence |

---

#### PATCH /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/
`PATCH /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedSubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidence |

---

#### DELETE /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/
`DELETE /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/`

ViewSet for managing submission evidence with text extraction and embedding generation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/extract_text/
`POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/extract_text/`

Extract text from submission and optionally generate embeddings.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidence |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/tag_evidence/
`POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/{id}/tag_evidence/`

Tag specific text excerpt to a criterion.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this submission evidence. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidence |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/search_embeddings/
`POST /api/tenants/{tenant_slug}/evidence-mapper/submissions/search_embeddings/`

Search submissions using embedding similarity.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `SubmissionEvidenceRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SubmissionEvidence |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/tags/
`GET /api/tenants/{tenant_slug}/evidence-mapper/tags/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCriteriaTagList |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/tags/
`POST /api/tenants/{tenant_slug}/evidence-mapper/tags/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CriteriaTagRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CriteriaTag |

---

#### GET /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/
`GET /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this criteria tag. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CriteriaTag |

---

#### PUT /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/
`PUT /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this criteria tag. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CriteriaTagRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CriteriaTag |

---

#### PATCH /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/
`PATCH /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this criteria tag. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedCriteriaTagRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CriteriaTag |

---

#### DELETE /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/
`DELETE /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/`

ViewSet for managing criteria tags.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this criteria tag. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/validate_tag/
`POST /api/tenants/{tenant_slug}/evidence-mapper/tags/{id}/validate_tag/`

Validate a criteria tag.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this criteria tag. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CriteriaTagRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CriteriaTag |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/criteria/
`GET /api/tenants/{tenant_slug}/feedback-assistant/criteria/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedFeedbackCriterionList |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/criteria/
`POST /api/tenants/{tenant_slug}/feedback-assistant/criteria/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | FeedbackCriterion |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/
`GET /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback criterion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackCriterion |

---

#### PUT /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/
`PUT /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback criterion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackCriterion |

---

#### PATCH /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/
`PATCH /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback criterion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedFeedbackCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackCriterion |

---

#### DELETE /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/
`DELETE /api/tenants/{tenant_slug}/feedback-assistant/criteria/{id}/`

ViewSet for managing feedback criteria

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback criterion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/generated/
`GET /api/tenants/{tenant_slug}/feedback-assistant/generated/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedGeneratedFeedbackListList |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/generated/
`POST /api/tenants/{tenant_slug}/feedback-assistant/generated/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `GeneratedFeedbackDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | GeneratedFeedbackDetail |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/
`GET /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GeneratedFeedbackDetail |

---

#### PUT /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/
`PUT /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `GeneratedFeedbackDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GeneratedFeedbackDetail |

---

#### PATCH /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/
`PATCH /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedGeneratedFeedbackDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GeneratedFeedbackDetail |

---

#### DELETE /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/
`DELETE /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/`

ViewSet for viewing and managing generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/deliver/
`POST /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/deliver/`

Mark feedback as delivered

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `GeneratedFeedbackDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GeneratedFeedbackDetail |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/review/
`POST /api/tenants/{tenant_slug}/feedback-assistant/generated/{id}/review/`

Review and potentially revise generated feedback

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this generated feedback. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `GeneratedFeedbackDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | GeneratedFeedbackDetail |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/logs/
`GET /api/tenants/{tenant_slug}/feedback-assistant/logs/`

ViewSet for viewing feedback logs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedFeedbackLogList |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/logs/{id}/
`GET /api/tenants/{tenant_slug}/feedback-assistant/logs/{id}/`

ViewSet for viewing feedback logs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback log. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackLog |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/templates/
`GET /api/tenants/{tenant_slug}/feedback-assistant/templates/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedFeedbackTemplateListList |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/templates/
`POST /api/tenants/{tenant_slug}/feedback-assistant/templates/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackTemplateDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | FeedbackTemplateDetail |

---

#### GET /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/
`GET /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackTemplateDetail |

---

#### PUT /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/
`PUT /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackTemplateDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackTemplateDetail |

---

#### PATCH /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/
`PATCH /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedFeedbackTemplateDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackTemplateDetail |

---

#### DELETE /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/
`DELETE /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/`

ViewSet for FeedbackTemplate management and feedback generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/generate_batch/
`POST /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/generate_batch/`

Generate feedback for multiple students in batch

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackTemplateDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackTemplateDetail |

---

#### POST /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/generate_feedback/
`POST /api/tenants/{tenant_slug}/feedback-assistant/templates/{id}/generate_feedback/`

Generate personalized feedback for a single student

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this feedback template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `FeedbackTemplateDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | FeedbackTemplateDetail |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/attachments/
`GET /api/tenants/{tenant_slug}/funding-eligibility/attachments/`

Evidence attachment viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEvidenceAttachmentList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/attachments/
`POST /api/tenants/{tenant_slug}/funding-eligibility/attachments/`

Upload evidence file

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceAttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EvidenceAttachment |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/`

Evidence attachment viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence attachment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceAttachment |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/`

Evidence attachment viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence attachment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceAttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceAttachment |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/`

Evidence attachment viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence attachment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEvidenceAttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceAttachment |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/`

Evidence attachment viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence attachment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/verify/
`POST /api/tenants/{tenant_slug}/funding-eligibility/attachments/{id}/verify/`

Mark evidence as verified

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence attachment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EvidenceAttachmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceAttachment |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/
`GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEligibilityCheckList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/
`POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EligibilityCheck |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheckDetail |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheck |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEligibilityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheck |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/approve_override/
`POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/{id}/approve_override/`

Approve eligibility override

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheck |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/check_eligibility/
`POST /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/check_eligibility/`

Perform eligibility check with rules engine validation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheck |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/dashboard_stats/
`GET /api/tenants/{tenant_slug}/funding-eligibility/checks-legacy/dashboard_stats/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityCheck |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions/`

Jurisdiction viewset - read-only, public access for browsing available jurisdictions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedJurisdictionList |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedJurisdictionRequirementList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/
`POST /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `JurisdictionRequirementRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | JurisdictionRequirement |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | JurisdictionRequirement |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `JurisdictionRequirementRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | JurisdictionRequirement |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedJurisdictionRequirementRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | JurisdictionRequirement |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/requirements_summary/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/{id}/requirements_summary/`

Get human-readable summary of requirements

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | JurisdictionRequirement |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/active/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions-legacy/active/`

Get currently active jurisdiction requirements

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | JurisdictionRequirement |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions/{code}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/jurisdictions/{code}/`

Jurisdiction viewset - read-only, public access for browsing available jurisdictions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| code | path | string | Yes | A unique value identifying this Jurisdiction. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Jurisdiction |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/overrides/
`GET /api/tenants/{tenant_slug}/funding-eligibility/overrides/`

Decision override viewset.
Allows authorized users to override automated decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedDecisionOverrideList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/overrides/
`POST /api/tenants/{tenant_slug}/funding-eligibility/overrides/`

Create decision override

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `DecisionOverrideRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | DecisionOverride |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/`

Decision override viewset.
Allows authorized users to override automated decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this decision override. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DecisionOverride |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/`

Decision override viewset.
Allows authorized users to override automated decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this decision override. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `DecisionOverrideRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DecisionOverride |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/`

Decision override viewset.
Allows authorized users to override automated decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this decision override. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedDecisionOverrideRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DecisionOverride |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/overrides/{id}/`

Decision override viewset.
Allows authorized users to override automated decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this decision override. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/
`GET /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedReferenceTableList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/
`POST /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ReferenceTableRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ReferenceTable |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reference table. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReferenceTable |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reference table. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ReferenceTableRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReferenceTable |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reference table. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedReferenceTableRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ReferenceTable |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/reference-tables/{id}/`

Reference table management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this reference table. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/requests/
`GET /api/tenants/{tenant_slug}/funding-eligibility/requests/`

Eligibility request viewset with hard-block enforcement.

CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEligibilityRequestListList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/requests/
`POST /api/tenants/{tenant_slug}/funding-eligibility/requests/`

Create eligibility request and enqueue evaluation.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CreateEligibilityRequestRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CreateEligibilityRequest |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/`

Eligibility request viewset with hard-block enforcement.

CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRequest |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/`

Eligibility request viewset with hard-block enforcement.

CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityRequestRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRequest |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/`

Eligibility request viewset with hard-block enforcement.

CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEligibilityRequestRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRequest |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/`

Eligibility request viewset with hard-block enforcement.

CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/check_eligibility/
`GET /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/check_eligibility/`

Check if request allows enrolment.

HARD-BLOCK ENFORCEMENT:
Returns 403 if decision is 'ineligible' and no override approved.
SMS/LMS should check this endpoint before allowing enrolment.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRequest |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/evaluate/
`POST /api/tenants/{tenant_slug}/funding-eligibility/requests/{id}/evaluate/`

Trigger eligibility evaluation.
Uses rules engine to produce deterministic decision.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this eligibility request. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityRequestRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRequest |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/
`GET /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEligibilityRuleList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/
`POST /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EligibilityRule |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRule |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `EligibilityRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRule |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedEligibilityRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EligibilityRule |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/rules-legacy/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/rulesets/
`GET /api/tenants/{tenant_slug}/funding-eligibility/rulesets/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRulesetList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/
`POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RulesetRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Ruleset |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Ruleset |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RulesetRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Ruleset |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedRulesetRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Ruleset |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/`

Ruleset management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/activate/
`POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/activate/`

Activate a ruleset.
Retires currently active rulesets for same jurisdiction.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RulesetRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Ruleset |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/add_artifact/
`POST /api/tenants/{tenant_slug}/funding-eligibility/rulesets/{id}/add_artifact/`

Add an artifact to a ruleset

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ruleset. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RulesetRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Ruleset |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/webhooks/
`GET /api/tenants/{tenant_slug}/funding-eligibility/webhooks/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedWebhookEndpointList |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/webhooks/
`POST /api/tenants/{tenant_slug}/funding-eligibility/webhooks/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `WebhookEndpointRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | WebhookEndpoint |

---

#### GET /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/
`GET /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this webhook endpoint. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | WebhookEndpoint |

---

#### PUT /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/
`PUT /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this webhook endpoint. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `WebhookEndpointRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | WebhookEndpoint |

---

#### PATCH /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/
`PATCH /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this webhook endpoint. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedWebhookEndpointRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | WebhookEndpoint |

---

#### DELETE /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/
`DELETE /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/`

Webhook endpoint management viewset.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this webhook endpoint. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/test/
`POST /api/tenants/{tenant_slug}/funding-eligibility/webhooks/{id}/test/`

Test webhook endpoint

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this webhook endpoint. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `WebhookEndpointRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | WebhookEndpoint |

---

#### GET /api/tenants/{tenant_slug}/integrations/
`GET /api/tenants/{tenant_slug}/integrations/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedIntegrationList |

---

#### POST /api/tenants/{tenant_slug}/integrations/
`POST /api/tenants/{tenant_slug}/integrations/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Integration |

---

#### GET /api/tenants/{tenant_slug}/integrations/{id}/
`GET /api/tenants/{tenant_slug}/integrations/{id}/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### PUT /api/tenants/{tenant_slug}/integrations/{id}/
`PUT /api/tenants/{tenant_slug}/integrations/{id}/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### PATCH /api/tenants/{tenant_slug}/integrations/{id}/
`PATCH /api/tenants/{tenant_slug}/integrations/{id}/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedIntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### DELETE /api/tenants/{tenant_slug}/integrations/{id}/
`DELETE /api/tenants/{tenant_slug}/integrations/{id}/`

API endpoint for managing integrations

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/integrations/{id}/connect/
`POST /api/tenants/{tenant_slug}/integrations/{id}/connect/`

Connect/activate an integration

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### POST /api/tenants/{tenant_slug}/integrations/{id}/disconnect/
`POST /api/tenants/{tenant_slug}/integrations/{id}/disconnect/`

Disconnect/deactivate an integration

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### GET /api/tenants/{tenant_slug}/integrations/{id}/logs/
`GET /api/tenants/{tenant_slug}/integrations/{id}/logs/`

Get integration logs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### GET /api/tenants/{tenant_slug}/integrations/{id}/mappings/
`GET /api/tenants/{tenant_slug}/integrations/{id}/mappings/`

Get or create field mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### POST /api/tenants/{tenant_slug}/integrations/{id}/mappings/
`POST /api/tenants/{tenant_slug}/integrations/{id}/mappings/`

Get or create field mappings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### POST /api/tenants/{tenant_slug}/integrations/{id}/sync/
`POST /api/tenants/{tenant_slug}/integrations/{id}/sync/`

Trigger manual synchronization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### POST /api/tenants/{tenant_slug}/integrations/{id}/test_connection/
`POST /api/tenants/{tenant_slug}/integrations/{id}/test_connection/`

Test integration connection using actual connector

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `IntegrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Integration |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/audit-logs/
`GET /api/tenants/{tenant_slug}/intervention-tracker/audit-logs/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAuditLogList |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/audit-logs/{id}/
`GET /api/tenants/{tenant_slug}/intervention-tracker/audit-logs/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this audit log. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AuditLog |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/
`GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedInterventionListList |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/
`POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Intervention |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/
`GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### PUT /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/
`PUT /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### PATCH /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/
`PATCH /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedInterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### DELETE /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/
`DELETE /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/record_outcome/
`POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/record_outcome/`

Record intervention outcome

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/update_status/
`POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/update_status/`

Update intervention status

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/update_step/
`POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/{id}/update_step/`

Update workflow step status

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/audit_report/
`GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/audit_report/`

Generate audit report

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/create_intervention/
`POST /api/tenants/{tenant_slug}/intervention-tracker/interventions/create_intervention/`

Create a new intervention with workflow initialization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/dashboard/
`GET /api/tenants/{tenant_slug}/intervention-tracker/interventions/dashboard/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Intervention |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/rules/
`GET /api/tenants/{tenant_slug}/intervention-tracker/rules/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedInterventionRuleList |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/rules/
`POST /api/tenants/{tenant_slug}/intervention-tracker/rules/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | InterventionRule |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/
`GET /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention rule. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionRule |

---

#### PUT /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/
`PUT /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention rule. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionRule |

---

#### PATCH /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/
`PATCH /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention rule. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedInterventionRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionRule |

---

#### DELETE /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/
`DELETE /api/tenants/{tenant_slug}/intervention-tracker/rules/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention rule. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/rules/evaluate_rules/
`POST /api/tenants/{tenant_slug}/intervention-tracker/rules/evaluate_rules/`

Evaluate rules against student metrics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionRule |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/workflows/
`GET /api/tenants/{tenant_slug}/intervention-tracker/workflows/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedInterventionWorkflowList |

---

#### POST /api/tenants/{tenant_slug}/intervention-tracker/workflows/
`POST /api/tenants/{tenant_slug}/intervention-tracker/workflows/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionWorkflowRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | InterventionWorkflow |

---

#### GET /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/
`GET /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention workflow. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionWorkflow |

---

#### PUT /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/
`PUT /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention workflow. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionWorkflowRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionWorkflow |

---

#### PATCH /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/
`PATCH /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention workflow. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedInterventionWorkflowRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionWorkflow |

---

#### DELETE /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/
`DELETE /api/tenants/{tenant_slug}/intervention-tracker/workflows/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention workflow. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/micro-credentials/
`GET /api/tenants/{tenant_slug}/micro-credentials/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMicroCredentialList |

---

#### POST /api/tenants/{tenant_slug}/micro-credentials/
`POST /api/tenants/{tenant_slug}/micro-credentials/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MicroCredential |

---

#### GET /api/tenants/{tenant_slug}/micro-credentials/{micro_credential_id}/versions/
`GET /api/tenants/{tenant_slug}/micro-credentials/{micro_credential_id}/versions/`

ViewSet for viewing micro-credential version history.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| micro_credential_id | path | integer | Yes |  |
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMicroCredentialVersionList |

---

#### GET /api/tenants/{tenant_slug}/micro-credentials/{id}/
`GET /api/tenants/{tenant_slug}/micro-credentials/{id}/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### PUT /api/tenants/{tenant_slug}/micro-credentials/{id}/
`PUT /api/tenants/{tenant_slug}/micro-credentials/{id}/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### PATCH /api/tenants/{tenant_slug}/micro-credentials/{id}/
`PATCH /api/tenants/{tenant_slug}/micro-credentials/{id}/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedMicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### DELETE /api/tenants/{tenant_slug}/micro-credentials/{id}/
`DELETE /api/tenants/{tenant_slug}/micro-credentials/{id}/`

ViewSet for managing micro-credentials (short courses).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/micro-credentials/{id}/duplicate/
`POST /api/tenants/{tenant_slug}/micro-credentials/{id}/duplicate/`

Duplicate a micro-credential.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### POST /api/tenants/{tenant_slug}/micro-credentials/{id}/publish/
`POST /api/tenants/{tenant_slug}/micro-credentials/{id}/publish/`

Publish a micro-credential.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### GET /api/tenants/{tenant_slug}/micro-credentials/enrollments/
`GET /api/tenants/{tenant_slug}/micro-credentials/enrollments/`

ViewSet for managing micro-credential enrollments.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedMicroCredentialEnrollmentList |

---

#### POST /api/tenants/{tenant_slug}/micro-credentials/enrollments/
`POST /api/tenants/{tenant_slug}/micro-credentials/enrollments/`

ViewSet for managing micro-credential enrollments.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialEnrollmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | MicroCredentialEnrollment |

---

#### POST /api/tenants/{tenant_slug}/micro-credentials/generate_from_units/
`POST /api/tenants/{tenant_slug}/micro-credentials/generate_from_units/`

Generate a micro-credential using AI from selected units.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `MicroCredentialRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | MicroCredential |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/bias-scores/
`GET /api/tenants/{tenant_slug}/moderation-tool/bias-scores/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedBiasScoreList |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/bias-scores/
`POST /api/tenants/{tenant_slug}/moderation-tool/bias-scores/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `BiasScoreRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | BiasScore |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/
`GET /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this bias score. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | BiasScore |

---

#### PUT /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/
`PUT /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this bias score. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `BiasScoreRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | BiasScore |

---

#### PATCH /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/
`PATCH /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this bias score. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedBiasScoreRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | BiasScore |

---

#### DELETE /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/
`DELETE /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/`

ViewSet for managing bias scores.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this bias score. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/validate/
`POST /api/tenants/{tenant_slug}/moderation-tool/bias-scores/{id}/validate/`

Validate a bias score.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this bias score. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `BiasScoreRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | BiasScore |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/decisions/
`GET /api/tenants/{tenant_slug}/moderation-tool/decisions/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAssessorDecisionList |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/decisions/
`POST /api/tenants/{tenant_slug}/moderation-tool/decisions/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessorDecisionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AssessorDecision |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/
`GET /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this assessor decision. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessorDecision |

---

#### PUT /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/
`PUT /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this assessor decision. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `AssessorDecisionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessorDecision |

---

#### PATCH /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/
`PATCH /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this assessor decision. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedAssessorDecisionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AssessorDecision |

---

#### DELETE /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/
`DELETE /api/tenants/{tenant_slug}/moderation-tool/decisions/{id}/`

ViewSet for managing individual assessor decisions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this assessor decision. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/logs/
`GET /api/tenants/{tenant_slug}/moderation-tool/logs/`

ViewSet for viewing moderation logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedModerationLogList |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/logs/{id}/
`GET /api/tenants/{tenant_slug}/moderation-tool/logs/{id}/`

ViewSet for viewing moderation logs (read-only).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation log. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationLog |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/outliers/
`GET /api/tenants/{tenant_slug}/moderation-tool/outliers/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedOutlierDetectionList |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/outliers/
`POST /api/tenants/{tenant_slug}/moderation-tool/outliers/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `OutlierDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | OutlierDetection |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/
`GET /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this outlier detection. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | OutlierDetection |

---

#### PUT /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/
`PUT /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this outlier detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `OutlierDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | OutlierDetection |

---

#### PATCH /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/
`PATCH /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this outlier detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedOutlierDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | OutlierDetection |

---

#### DELETE /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/
`DELETE /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/`

ViewSet for managing outlier detections.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this outlier detection. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/resolve/
`POST /api/tenants/{tenant_slug}/moderation-tool/outliers/{id}/resolve/`

Mark an outlier as resolved.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this outlier detection. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `OutlierDetectionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | OutlierDetection |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/sessions/
`GET /api/tenants/{tenant_slug}/moderation-tool/sessions/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedModerationSessionList |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/sessions/
`POST /api/tenants/{tenant_slug}/moderation-tool/sessions/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ModerationSession |

---

#### GET /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/
`GET /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### PUT /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/
`PUT /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### PATCH /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/
`PATCH /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### DELETE /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/
`DELETE /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/`

ViewSet for managing moderation sessions and running comparisons.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/calculate_bias/
`POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/calculate_bias/`

Calculate bias scores for assessors.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/compare_decisions/
`POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/compare_decisions/`

Compare assessor decisions for a specific student or across all submissions.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/detect_outliers/
`POST /api/tenants/{tenant_slug}/moderation-tool/sessions/{id}/detect_outliers/`

Detect outliers in assessor decisions using statistical analysis.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this moderation session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ModerationSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ModerationSession |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/activities/
`GET /api/tenants/{tenant_slug}/pd-tracker/activities/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedPDActivityList |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/activities/
`POST /api/tenants/{tenant_slug}/pd-tracker/activities/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | PDActivity |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/
`GET /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd activity. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDActivityDetail |

---

#### PUT /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/
`PUT /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd activity. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDActivity |

---

#### PATCH /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/
`PATCH /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd activity. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedPDActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDActivity |

---

#### DELETE /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/
`DELETE /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/`

ViewSet for managing PD activities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd activity. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/verify_activity/
`POST /api/tenants/{tenant_slug}/pd-tracker/activities/{id}/verify_activity/`

Verify a PD activity

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd activity. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDActivity |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/activities/log_activity/
`POST /api/tenants/{tenant_slug}/pd-tracker/activities/log_activity/`

Log a new PD activity and update trainer profile

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDActivityRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDActivity |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/checks/
`GET /api/tenants/{tenant_slug}/pd-tracker/checks/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedComplianceCheckList |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/checks/
`POST /api/tenants/{tenant_slug}/pd-tracker/checks/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ComplianceCheck |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/
`GET /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheckDetail |

---

#### PUT /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/
`PUT /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### PATCH /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/
`PATCH /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### DELETE /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/
`DELETE /api/tenants/{tenant_slug}/pd-tracker/checks/{id}/`

ViewSet for managing compliance checks

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance check. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/checks/compliance_report/
`POST /api/tenants/{tenant_slug}/pd-tracker/checks/compliance_report/`

Generate compliance report

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ComplianceCheckRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/checks/dashboard/
`GET /api/tenants/{tenant_slug}/pd-tracker/checks/dashboard/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceCheck |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/profiles/
`GET /api/tenants/{tenant_slug}/pd-tracker/profiles/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTrainerProfileList |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/profiles/
`POST /api/tenants/{tenant_slug}/pd-tracker/profiles/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TrainerProfile |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/
`GET /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfileDetail |

---

#### PUT /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/
`PUT /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### PATCH /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/
`PATCH /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTrainerProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfile |

---

#### DELETE /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/
`DELETE /api/tenants/{tenant_slug}/pd-tracker/profiles/{id}/`

ViewSet for managing trainer profiles

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this trainer profile. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/profiles/check_currency/
`POST /api/tenants/{tenant_slug}/pd-tracker/profiles/check_currency/`

Check trainer currency status

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TrainerProfileDetailRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TrainerProfileDetail |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/rules/
`GET /api/tenants/{tenant_slug}/pd-tracker/rules/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedComplianceRuleList |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/rules/
`POST /api/tenants/{tenant_slug}/pd-tracker/rules/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ComplianceRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ComplianceRule |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/
`GET /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance rule. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceRule |

---

#### PUT /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/
`PUT /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance rule. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ComplianceRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceRule |

---

#### PATCH /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/
`PATCH /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance rule. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedComplianceRuleRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComplianceRule |

---

#### DELETE /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/
`DELETE /api/tenants/{tenant_slug}/pd-tracker/rules/{id}/`

ViewSet for managing compliance rules

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this compliance rule. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/suggestions/
`GET /api/tenants/{tenant_slug}/pd-tracker/suggestions/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedPDSuggestionList |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/
`POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDSuggestionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | PDSuggestion |

---

#### GET /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/
`GET /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd suggestion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDSuggestionDetail |

---

#### PUT /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/
`PUT /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd suggestion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDSuggestionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDSuggestion |

---

#### PATCH /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/
`PATCH /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd suggestion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedPDSuggestionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDSuggestion |

---

#### DELETE /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/
`DELETE /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/`

ViewSet for managing PD suggestions

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd suggestion. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/accept_suggestion/
`POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/{id}/accept_suggestion/`

Accept a suggestion and optionally create linked activity

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this pd suggestion. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDSuggestionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDSuggestion |

---

#### POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/generate_suggestions/
`POST /api/tenants/{tenant_slug}/pd-tracker/suggestions/generate_suggestions/`

Generate LLM-powered PD suggestions for a trainer

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PDSuggestionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PDSuggestion |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/clauses/
`GET /api/tenants/{tenant_slug}/policy-comparator/clauses/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| compliance_level | query | string | No | * `critical` - Critical - Must comply * `essential` - Essential - Required * `recommended` - Recommended - Best practice |
| is_active | query | boolean | No |  |
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| standard | query | integer | No |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedASQAClauseList |

---

#### POST /api/tenants/{tenant_slug}/policy-comparator/clauses/
`POST /api/tenants/{tenant_slug}/policy-comparator/clauses/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ASQAClauseRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ASQAClause |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/
`GET /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Clause. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAClause |

---

#### PUT /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/
`PUT /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Clause. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ASQAClauseRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAClause |

---

#### PATCH /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/
`PATCH /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Clause. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedASQAClauseRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAClause |

---

#### DELETE /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/
`DELETE /api/tenants/{tenant_slug}/policy-comparator/clauses/{id}/`

ViewSet for ASQA clauses

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Clause. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedPolicyList |

---

#### POST /api/tenants/{tenant_slug}/policy-comparator/policies/
`POST /api/tenants/{tenant_slug}/policy-comparator/policies/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### PUT /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/
`PUT /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### PATCH /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/
`PATCH /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedPolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### DELETE /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/
`DELETE /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/`

ViewSet for policies with comparison capabilities

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/compare/
`POST /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/compare/`

Compare policy against ASQA standards using NLP-based text similarity
Instantly identifies compliance gaps

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/comparison_history/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/comparison_history/`

Get comparison history for a policy

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### POST /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/convert_to_2025_standards/
`POST /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/convert_to_2025_standards/`

Convert policy from 2015 to 2025 ASQA Standards using AI

Request Body:
{
    "session_name": "optional session name",
    "ai_model": "gpt-4o" | "claude-3-opus",
    "options": {
        "preserve_formatting": true,
        "update_terminology": true,
        "add_conversion_notes": true,
        "use_ai": true
    }
}

Returns conversion session details and summary

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PolicyRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/gap_analysis/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/gap_analysis/`

Get detailed gap analysis for a policy

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/results/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/{id}/results/`

Get detailed comparison results for a policy

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/conversion-sessions/{session_id}/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/conversion-sessions/{session_id}/`

Get detailed information about a specific conversion session

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| session_id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/policies/list_conversion_sessions/
`GET /api/tenants/{tenant_slug}/policy-comparator/policies/list_conversion_sessions/`

List all policy conversion sessions for this tenant

Query params:
- status: filter by status (pending, analyzing, converting, completed, failed)
- limit: max results (default 20)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Policy |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/sessions/
`GET /api/tenants/{tenant_slug}/policy-comparator/sessions/`

ViewSet for comparison sessions (read-only)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedComparisonSessionList |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/sessions/{id}/
`GET /api/tenants/{tenant_slug}/policy-comparator/sessions/{id}/`

ViewSet for comparison sessions (read-only)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ComparisonSession |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/standards/
`GET /api/tenants/{tenant_slug}/policy-comparator/standards/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| is_active | query | boolean | No |  |
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| standard_type | query | string | No | * `training_assessment` - Training and Assessment * `trainer_assessor` - Trainer and Assessor * `educational_support` - Educational and Support Services * `certification` - Certification * `engagement_employer` - Engagement with Employers * `complaints_appeals` - Complaints and Appeals * `governance` - Governance and Administration * `financial` - Financial Management * `qa1_training_assessment` - Quality Area 1 - Training and Assessment * `qa2_student_support` - Quality Area 2 - VET Student Support * `qa3_workforce` - Quality Area 3 - VET Workforce * `qa4_governance` - Quality Area 4 - Governance * `compliance_information` - Compliance - Information and Transparency * `compliance_integrity` - Compliance - Integrity of NRT Products * `compliance_accountability` - Compliance - Accountability * `compliance_fit_proper` - Compliance - Fit and Proper Person * `credential_policy` - Credential Policy |
| tenant_slug | path | string | Yes |  |
| version | query | string | No | * `2015` - Standards for RTOs 2015 * `2025` - Standards for RTOs 2025 |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedASQAStandardList |

---

#### POST /api/tenants/{tenant_slug}/policy-comparator/standards/
`POST /api/tenants/{tenant_slug}/policy-comparator/standards/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ASQAStandardRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ASQAStandard |

---

#### GET /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/
`GET /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Standard. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAStandard |

---

#### PUT /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/
`PUT /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Standard. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ASQAStandardRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAStandard |

---

#### PATCH /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/
`PATCH /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Standard. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedASQAStandardRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ASQAStandard |

---

#### DELETE /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/
`DELETE /api/tenants/{tenant_slug}/policy-comparator/standards/{id}/`

ViewSet for ASQA standards

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this ASQA Standard. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/
`GET /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedStudentEngagementMetricList |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/
`POST /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `StudentEngagementMetricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | StudentEngagementMetric |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/
`GET /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student engagement metric. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentEngagementMetric |

---

#### PUT /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/
`PUT /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student engagement metric. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `StudentEngagementMetricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentEngagementMetric |

---

#### PATCH /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/
`PATCH /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student engagement metric. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedStudentEngagementMetricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | StudentEngagementMetric |

---

#### DELETE /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/
`DELETE /api/tenants/{tenant_slug}/risk-engine/engagement-metrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this student engagement metric. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/interventions/
`GET /api/tenants/{tenant_slug}/risk-engine/interventions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedInterventionActionList |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/interventions/
`POST /api/tenants/{tenant_slug}/risk-engine/interventions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | InterventionAction |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/
`GET /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention action. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionAction |

---

#### PUT /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/
`PUT /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionAction |

---

#### PATCH /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/
`PATCH /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedInterventionActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionAction |

---

#### DELETE /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/
`DELETE /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention action. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/mark_completed/
`POST /api/tenants/{tenant_slug}/risk-engine/interventions/{id}/mark_completed/`

Mark intervention as completed

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this intervention action. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `InterventionActionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | InterventionAction |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/
`GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRiskAssessmentListList |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/
`POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RiskAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | RiskAssessment |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/
`GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk assessment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### PUT /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/
`PUT /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk assessment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RiskAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### PATCH /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/
`PATCH /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk assessment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedRiskAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### DELETE /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/
`DELETE /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk assessment. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/acknowledge_alert/
`POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/{id}/acknowledge_alert/`

Acknowledge a risk alert

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk assessment. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RiskAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/alerts_dashboard/
`GET /api/tenants/{tenant_slug}/risk-engine/risk-assessments/alerts_dashboard/`

Get dashboard data for risk alerts

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/predict_risk/
`POST /api/tenants/{tenant_slug}/risk-engine/risk-assessments/predict_risk/`

Predict dropout risk using logistic regression + sentiment fusion

Expected payload:
{
    "student_id": "STU001",
    "student_name": "John Doe",
    "engagement_data": {...},
    "performance_data": {...},
    "attendance_data": {...},
    "sentiment_data": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RiskAssessmentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskAssessment |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/risk-factors/
`GET /api/tenants/{tenant_slug}/risk-engine/risk-factors/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRiskFactorList |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/risk-factors/{id}/
`GET /api/tenants/{tenant_slug}/risk-engine/risk-factors/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this risk factor. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RiskFactor |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/sentiment-analyses/
`GET /api/tenants/{tenant_slug}/risk-engine/sentiment-analyses/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedSentimentAnalysisList |

---

#### GET /api/tenants/{tenant_slug}/risk-engine/sentiment-analyses/{id}/
`GET /api/tenants/{tenant_slug}/risk-engine/sentiment-analyses/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this sentiment analysis. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | SentimentAnalysis |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/criteria/
`GET /api/tenants/{tenant_slug}/rubric-generator/criteria/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRubricCriterionList |

---

#### POST /api/tenants/{tenant_slug}/rubric-generator/criteria/
`POST /api/tenants/{tenant_slug}/rubric-generator/criteria/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | RubricCriterion |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/
`GET /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricCriterion |

---

#### PUT /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/
`PUT /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricCriterion |

---

#### PATCH /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/
`PATCH /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedRubricCriterionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricCriterion |

---

#### DELETE /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/
`DELETE /api/tenants/{tenant_slug}/rubric-generator/criteria/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/levels/
`GET /api/tenants/{tenant_slug}/rubric-generator/levels/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRubricLevelList |

---

#### POST /api/tenants/{tenant_slug}/rubric-generator/levels/
`POST /api/tenants/{tenant_slug}/rubric-generator/levels/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricLevelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | RubricLevel |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/
`GET /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricLevel |

---

#### PUT /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/
`PUT /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricLevelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricLevel |

---

#### PATCH /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/
`PATCH /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedRubricLevelRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricLevel |

---

#### DELETE /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/
`DELETE /api/tenants/{tenant_slug}/rubric-generator/levels/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/
`GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedRubricList |

---

#### POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/
`POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | Rubric |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/
`GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | RubricDetail |

---

#### PUT /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/
`PUT /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Rubric |

---

#### PATCH /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/
`PATCH /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedRubricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Rubric |

---

#### DELETE /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/
`DELETE /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/approve/
`POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/{id}/approve/`

Approve rubric for publishing

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Rubric |

---

#### GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/dashboard_stats/
`GET /api/tenants/{tenant_slug}/rubric-generator/rubrics/dashboard_stats/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Rubric |

---

#### POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/generate_rubric/
`POST /api/tenants/{tenant_slug}/rubric-generator/rubrics/generate_rubric/`

Generate rubric using NLP summarization and taxonomy tagging

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `RubricRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | Rubric |

---

#### GET /api/tenants/{tenant_slug}/study-coach/config/
`GET /api/tenants/{tenant_slug}/study-coach/config/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCoachConfigurationList |

---

#### POST /api/tenants/{tenant_slug}/study-coach/config/
`POST /api/tenants/{tenant_slug}/study-coach/config/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CoachConfigurationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CoachConfiguration |

---

#### GET /api/tenants/{tenant_slug}/study-coach/config/{id}/
`GET /api/tenants/{tenant_slug}/study-coach/config/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coach configuration. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachConfiguration |

---

#### PUT /api/tenants/{tenant_slug}/study-coach/config/{id}/
`PUT /api/tenants/{tenant_slug}/study-coach/config/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coach configuration. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CoachConfigurationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachConfiguration |

---

#### PATCH /api/tenants/{tenant_slug}/study-coach/config/{id}/
`PATCH /api/tenants/{tenant_slug}/study-coach/config/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coach configuration. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedCoachConfigurationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachConfiguration |

---

#### DELETE /api/tenants/{tenant_slug}/study-coach/config/{id}/
`DELETE /api/tenants/{tenant_slug}/study-coach/config/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coach configuration. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/study-coach/documents/
`GET /api/tenants/{tenant_slug}/study-coach/documents/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedKnowledgeDocumentList |

---

#### POST /api/tenants/{tenant_slug}/study-coach/documents/
`POST /api/tenants/{tenant_slug}/study-coach/documents/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `KnowledgeDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | KnowledgeDocument |

---

#### GET /api/tenants/{tenant_slug}/study-coach/documents/{id}/
`GET /api/tenants/{tenant_slug}/study-coach/documents/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this knowledge document. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | KnowledgeDocument |

---

#### PUT /api/tenants/{tenant_slug}/study-coach/documents/{id}/
`PUT /api/tenants/{tenant_slug}/study-coach/documents/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this knowledge document. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `KnowledgeDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | KnowledgeDocument |

---

#### PATCH /api/tenants/{tenant_slug}/study-coach/documents/{id}/
`PATCH /api/tenants/{tenant_slug}/study-coach/documents/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this knowledge document. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedKnowledgeDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | KnowledgeDocument |

---

#### DELETE /api/tenants/{tenant_slug}/study-coach/documents/{id}/
`DELETE /api/tenants/{tenant_slug}/study-coach/documents/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this knowledge document. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/study-coach/insights/
`GET /api/tenants/{tenant_slug}/study-coach/insights/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedCoachingInsightList |

---

#### POST /api/tenants/{tenant_slug}/study-coach/insights/
`POST /api/tenants/{tenant_slug}/study-coach/insights/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CoachingInsightRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | CoachingInsight |

---

#### GET /api/tenants/{tenant_slug}/study-coach/insights/{id}/
`GET /api/tenants/{tenant_slug}/study-coach/insights/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coaching insight. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachingInsight |

---

#### PUT /api/tenants/{tenant_slug}/study-coach/insights/{id}/
`PUT /api/tenants/{tenant_slug}/study-coach/insights/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coaching insight. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CoachingInsightRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachingInsight |

---

#### PATCH /api/tenants/{tenant_slug}/study-coach/insights/{id}/
`PATCH /api/tenants/{tenant_slug}/study-coach/insights/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coaching insight. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedCoachingInsightRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachingInsight |

---

#### DELETE /api/tenants/{tenant_slug}/study-coach/insights/{id}/
`DELETE /api/tenants/{tenant_slug}/study-coach/insights/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this coaching insight. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/study-coach/insights/generate_insights/
`POST /api/tenants/{tenant_slug}/study-coach/insights/generate_insights/`

Generate insights for a student

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `CoachingInsightRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | CoachingInsight |

---

#### GET /api/tenants/{tenant_slug}/study-coach/messages/
`GET /api/tenants/{tenant_slug}/study-coach/messages/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedChatMessageList |

---

#### GET /api/tenants/{tenant_slug}/study-coach/messages/{id}/
`GET /api/tenants/{tenant_slug}/study-coach/messages/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat message. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatMessage |

---

#### GET /api/tenants/{tenant_slug}/study-coach/sessions/
`GET /api/tenants/{tenant_slug}/study-coach/sessions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedChatSessionListList |

---

#### POST /api/tenants/{tenant_slug}/study-coach/sessions/
`POST /api/tenants/{tenant_slug}/study-coach/sessions/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ChatSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | ChatSession |

---

#### GET /api/tenants/{tenant_slug}/study-coach/sessions/{id}/
`GET /api/tenants/{tenant_slug}/study-coach/sessions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat session. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### PUT /api/tenants/{tenant_slug}/study-coach/sessions/{id}/
`PUT /api/tenants/{tenant_slug}/study-coach/sessions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ChatSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### PATCH /api/tenants/{tenant_slug}/study-coach/sessions/{id}/
`PATCH /api/tenants/{tenant_slug}/study-coach/sessions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedChatSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### DELETE /api/tenants/{tenant_slug}/study-coach/sessions/{id}/
`DELETE /api/tenants/{tenant_slug}/study-coach/sessions/{id}/`
#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat session. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/study-coach/sessions/{id}/rate_session/
`POST /api/tenants/{tenant_slug}/study-coach/sessions/{id}/rate_session/`

Rate a completed session

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this chat session. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ChatSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### GET /api/tenants/{tenant_slug}/study-coach/sessions/dashboard/
`GET /api/tenants/{tenant_slug}/study-coach/sessions/dashboard/`

Get dashboard statistics

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### POST /api/tenants/{tenant_slug}/study-coach/sessions/send_message/
`POST /api/tenants/{tenant_slug}/study-coach/sessions/send_message/`

Send a message and get AI coach response

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `ChatSessionRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChatSession |

---

#### GET /api/tenants/{tenant_slug}/tas/
`GET /api/tenants/{tenant_slug}/tas/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTASList |

---

#### POST /api/tenants/{tenant_slug}/tas/
`POST /api/tenants/{tenant_slug}/tas/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/{id}/
`GET /api/tenants/{tenant_slug}/tas/{id}/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### PUT /api/tenants/{tenant_slug}/tas/{id}/
`PUT /api/tenants/{tenant_slug}/tas/{id}/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### PATCH /api/tenants/{tenant_slug}/tas/{id}/
`PATCH /api/tenants/{tenant_slug}/tas/{id}/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### DELETE /api/tenants/{tenant_slug}/tas/{id}/
`DELETE /api/tenants/{tenant_slug}/tas/{id}/`

ViewSet for TAS documents with GPT-4 generation

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/ask/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/ask/`

Conversational AI co-pilot - answer inline questions

POST /api/tenants/{tenant_slug}/tas/{id}/ai/ask/
Body: {
    "question": "Why is this cluster non-compliant?",
    "context": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/assess-facility/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/assess-facility/`

Assess facility adequacy

POST /api/tenants/{tenant_slug}/tas/{id}/ai/assess-facility/
Body: {
    "facility_inventory": [...],
    "unit_requirements": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/assessment-blueprint/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/assessment-blueprint/`

Generate assessment blueprint for a unit

POST /api/tenants/{tenant_slug}/tas/{id}/ai/assessment-blueprint/
Body: {
    "unit_code": "BSBWHS411",
    "elements": [...],
    "delivery_mode": "classroom",
    "industry_context": "office administration"
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-compliance/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-compliance/`

Check ASQA clause coverage

POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-compliance/
Body: {
    "tas_content": {...},
    "target_clauses": ["1.1", "1.2", "1.3"]
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-consistency/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-consistency/`

Check consistency across TAS, LMS, assessment tools

POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-consistency/
Body: {
    "tas_data": {...},
    "lms_data": {...},
    "assessment_tools": [...]
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/cluster-units/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/cluster-units/`

Suggest unit clusters based on semantic similarity

POST /api/tenants/{tenant_slug}/tas/{id}/ai/cluster-units/
Body: {
    "units": [...],
    "max_cluster_size": 4
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/completion-risk/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/completion-risk/`

Analyze completion/withdrawal risk

POST /api/tenants/{tenant_slug}/tas/{id}/ai/completion-risk/
Body: {
    "clusters": [...],
    "delivery_schedule": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/detect-policy-drift/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/detect-policy-drift/`

Detect policy changes since TAS approval

POST /api/tenants/{tenant_slug}/tas/{id}/ai/detect-policy-drift/
Body: {
    "tas_policy_references": [...],
    "current_policies": [...]
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/draft-section/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/draft-section/`

Draft TAS content section (cohort needs, delivery model, etc.)

POST /api/tenants/{tenant_slug}/tas/{id}/ai/draft-section/
Body: {
    "section_type": "cohort_needs",
    "cohort_data": {...},
    "qualification": "...",
    "delivery_context": "..."
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/enrich-tga/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/enrich-tga/`

Enrich TGA unit data with learning outcomes and assessment hints

POST /api/tenants/{tenant_slug}/tas/{id}/ai/enrich-tga/
Body: {
    "unit_code": "BSBWHS411",
    "tga_data": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/explain-changes/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/explain-changes/`

Explain differences between TAS versions

POST /api/tenants/{tenant_slug}/tas/{id}/ai/explain-changes/
Body: {
    "old_version": {...},
    "new_version": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/map-resources/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/map-resources/`

Map unit resource requirements to inventory

POST /api/tenants/{tenant_slug}/tas/{id}/ai/map-resources/
Body: {
    "unit_requirements": {...},
    "available_inventory": [...],
    "budget_constraints": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/optimize-timetable/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/optimize-timetable/`

Optimize timetable allocation

POST /api/tenants/{tenant_slug}/tas/{id}/ai/optimize-timetable/
Body: {
    "clusters": [...],
    "total_weeks": 52,
    "resources": {...},
    "constraints": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/predict-lln-risk/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/predict-lln-risk/`

Predict LLN support requirements

POST /api/tenants/{tenant_slug}/tas/{id}/ai/predict-lln-risk/
Body: {
    "cohort_data": {...},
    "historical_cohorts": [...]
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/recommend-electives/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/recommend-electives/`

Recommend elective units based on job outcomes

POST /api/tenants/{tenant_slug}/tas/{id}/ai/recommend-electives/
Body: {
    "qualification_code": "BSB50120",
    "job_outcomes": ["Business Manager", "Operations Coordinator"],
    "available_electives": [...],
    "packaging_rules": "..."
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/score-trainer/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/score-trainer/`

Score trainer suitability for a unit

POST /api/tenants/{tenant_slug}/tas/{id}/ai/score-trainer/
Body: {
    "trainer_profile": {...},
    "unit_requirements": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/suggest-cohort/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/suggest-cohort/`

Suggest cohort archetype and support requirements

POST /api/tenants/{tenant_slug}/tas/{id}/ai/suggest-cohort/
Body: {
    "cohort_history": [...],
    "demographics": {...}
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/summarize-minutes/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/summarize-minutes/`

Summarize industry engagement minutes

POST /api/tenants/{tenant_slug}/tas/{id}/ai/summarize-minutes/
Body: {
    "minutes_text": "...",
    "meeting_date": "2024-01-15",
    "attendees": [...]
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/ai/validation-plan/
`POST /api/tenants/{tenant_slug}/tas/{id}/ai/validation-plan/`

Generate validation/moderation plan

POST /api/tenants/{tenant_slug}/tas/{id}/ai/validation-plan/
Body: {
    "assessment_tasks": [...],
    "cohort_size": 25,
    "last_validation_date": "2024-01-01"
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/approve/
`POST /api/tenants/{tenant_slug}/tas/{id}/approve/`

Approve TAS document

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/convert-to-2025/
`POST /api/tenants/{tenant_slug}/tas/{id}/convert-to-2025/`

Convert TAS from Standards for RTOs 2015 to Standards for RTOs 2025

POST /api/tenants/{tenant_slug}/tas/{id}/convert-to-2025/
Body: {
    "session_name": "Optional session name",
    "ai_model": "gpt-4o",  // optional, defaults to gpt-4o
    "options": {
        "preserve_formatting": true,
        "update_terminology": true,
        "add_conversion_notes": true,
        "use_ai": true
    }
}

Returns: {
    "session_id": 123,
    "status": "pending",
    "message": "Conversion session created successfully"
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/create_version/
`POST /api/tenants/{tenant_slug}/tas/{id}/create_version/`

Create a new version of an existing TAS

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/{id}/generation_logs/
`GET /api/tenants/{tenant_slug}/tas/{id}/generation_logs/`

Get GPT-4 generation logs for a TAS document

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/publish/
`POST /api/tenants/{tenant_slug}/tas/{id}/publish/`

Publish TAS document

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/regenerate_section/
`POST /api/tenants/{tenant_slug}/tas/{id}/regenerate_section/`

Regenerate a specific section using GPT-4

Request body:
{
    "section_name": "qualification_overview",  // Required
    "custom_prompt": "Additional context...",  // Optional
    "ai_model": "gpt-4o"                      // Optional, defaults to gpt-4
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/{id}/submit_for_review/
`POST /api/tenants/{tenant_slug}/tas/{id}/submit_for_review/`

Submit TAS for review

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### PUT /api/tenants/{tenant_slug}/tas/{id}/update-content/
`PUT /api/tenants/{tenant_slug}/tas/{id}/update-content/`

Update TAS document content with optional version control

PATCH /api/tenants/{slug}/tas/{id}/update-content/

Body:
{
    "title": "Updated title",
    "sections": [...],
    "content": {...},
    "create_version": false,
    "change_summary": "Updated assessment section"
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### PATCH /api/tenants/{tenant_slug}/tas/{id}/update-content/
`PATCH /api/tenants/{tenant_slug}/tas/{id}/update-content/`

Update TAS document content with optional version control

PATCH /api/tenants/{slug}/tas/{id}/update-content/

Body:
{
    "title": "Updated title",
    "sections": [...],
    "content": {...},
    "create_version": false,
    "change_summary": "Updated assessment section"
}

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/{id}/version_history/
`GET /api/tenants/{tenant_slug}/tas/{id}/version_history/`

Get version history for a TAS document

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/{id}/versions/
`GET /api/tenants/{tenant_slug}/tas/{id}/versions/`

Get all versions of a TAS document

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/conversion-sessions/
`GET /api/tenants/{tenant_slug}/tas/conversion-sessions/`

List all TAS conversion sessions for the tenant

GET /api/tenants/{tenant_slug}/tas/conversion-sessions/

Query params:
- status: Filter by status (pending, analyzing, completed, failed, etc.)
- limit: Number of results (default 20)

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/conversion-sessions/{session_id}/
`GET /api/tenants/{tenant_slug}/tas/conversion-sessions/{session_id}/`

Get detailed information about a specific conversion session

GET /api/tenants/{tenant_slug}/tas/conversion-sessions/{session_id}/

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| session_id | path | string | Yes |  |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### POST /api/tenants/{tenant_slug}/tas/generate/
`POST /api/tenants/{tenant_slug}/tas/generate/`

Generate a new TAS document using GPT-4
Reduces TAS creation time by 90%

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/qualifications/
`GET /api/tenants/{tenant_slug}/tas/qualifications/`

Fetch qualifications from training.gov.au
Returns a list of qualifications with code, title, AQF level, and training package

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

#### GET /api/tenants/{tenant_slug}/tas/templates/
`GET /api/tenants/{tenant_slug}/tas/templates/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| aqf_level | query | string | No | * `certificate_i` - Certificate I * `certificate_ii` - Certificate II * `certificate_iii` - Certificate III * `certificate_iv` - Certificate IV * `diploma` - Diploma * `advanced_diploma` - Advanced Diploma * `graduate_certificate` - Graduate Certificate * `graduate_diploma` - Graduate Diploma * `bachelor` - Bachelor Degree * `masters` - Masters Degree |
| is_active | query | boolean | No |  |
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |
| template_type | query | string | No | * `general` - General Template * `trade` - Trade/Technical * `business` - Business/Commerce * `health` - Health/Community Services * `creative` - Creative Industries * `hospitality` - Hospitality/Tourism * `technology` - Information Technology * `education` - Education/Training |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTASTemplateList |

---

#### POST /api/tenants/{tenant_slug}/tas/templates/
`POST /api/tenants/{tenant_slug}/tas/templates/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TASTemplate |

---

#### GET /api/tenants/{tenant_slug}/tas/templates/{id}/
`GET /api/tenants/{tenant_slug}/tas/templates/{id}/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this TAS Template. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TASTemplate |

---

#### PUT /api/tenants/{tenant_slug}/tas/templates/{id}/
`PUT /api/tenants/{tenant_slug}/tas/templates/{id}/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this TAS Template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `TASTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TASTemplate |

---

#### PATCH /api/tenants/{tenant_slug}/tas/templates/{id}/
`PATCH /api/tenants/{tenant_slug}/tas/templates/{id}/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this TAS Template. |
| tenant_slug | path | string | Yes |  |

#### Request Body
Type: `PatchedTASTemplateRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TASTemplate |

---

#### DELETE /api/tenants/{tenant_slug}/tas/templates/{id}/
`DELETE /api/tenants/{tenant_slug}/tas/templates/{id}/`

ViewSet for TAS templates

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this TAS Template. |
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/tenants/{tenant_slug}/tas/units/
`GET /api/tenants/{tenant_slug}/tas/units/`

Fetch units of competency for a specific qualification
Returns units organized by groupings/majors if available

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| tenant_slug | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TAS |

---

### trainer-diary
#### GET /api/trainer-diary/audio-recordings/
`GET /api/trainer-diary/audio-recordings/`

ViewSet for audio recordings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedAudioRecordingList |

---

#### POST /api/trainer-diary/audio-recordings/
`POST /api/trainer-diary/audio-recordings/`

ViewSet for audio recordings


#### Request Body
Type: `AudioRecordingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | AudioRecording |

---

#### GET /api/trainer-diary/audio-recordings/{id}/
`GET /api/trainer-diary/audio-recordings/{id}/`

ViewSet for audio recordings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this audio recording. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AudioRecording |

---

#### PUT /api/trainer-diary/audio-recordings/{id}/
`PUT /api/trainer-diary/audio-recordings/{id}/`

ViewSet for audio recordings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this audio recording. |

#### Request Body
Type: `AudioRecordingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AudioRecording |

---

#### PATCH /api/trainer-diary/audio-recordings/{id}/
`PATCH /api/trainer-diary/audio-recordings/{id}/`

ViewSet for audio recordings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this audio recording. |

#### Request Body
Type: `PatchedAudioRecordingRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | AudioRecording |

---

#### DELETE /api/trainer-diary/audio-recordings/{id}/
`DELETE /api/trainer-diary/audio-recordings/{id}/`

ViewSet for audio recordings

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this audio recording. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/trainer-diary/daily-summaries/
`GET /api/trainer-diary/daily-summaries/`

ViewSet for daily summaries

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedDailySummaryList |

---

#### POST /api/trainer-diary/daily-summaries/
`POST /api/trainer-diary/daily-summaries/`

ViewSet for daily summaries


#### Request Body
Type: `DailySummaryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | DailySummary |

---

#### GET /api/trainer-diary/daily-summaries/{id}/
`GET /api/trainer-diary/daily-summaries/{id}/`

ViewSet for daily summaries

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this daily summary. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DailySummary |

---

#### PUT /api/trainer-diary/daily-summaries/{id}/
`PUT /api/trainer-diary/daily-summaries/{id}/`

ViewSet for daily summaries

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this daily summary. |

#### Request Body
Type: `DailySummaryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DailySummary |

---

#### PATCH /api/trainer-diary/daily-summaries/{id}/
`PATCH /api/trainer-diary/daily-summaries/{id}/`

ViewSet for daily summaries

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this daily summary. |

#### Request Body
Type: `PatchedDailySummaryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DailySummary |

---

#### DELETE /api/trainer-diary/daily-summaries/{id}/
`DELETE /api/trainer-diary/daily-summaries/{id}/`

ViewSet for daily summaries

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this daily summary. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/trainer-diary/diary-entries/
`GET /api/trainer-diary/diary-entries/`

ViewSet for diary entries with speech-to-text and AI summarization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedDiaryEntryListList |

---

#### POST /api/trainer-diary/diary-entries/
`POST /api/trainer-diary/diary-entries/`

ViewSet for diary entries with speech-to-text and AI summarization


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | DiaryEntry |

---

#### GET /api/trainer-diary/diary-entries/{id}/
`GET /api/trainer-diary/diary-entries/{id}/`

ViewSet for diary entries with speech-to-text and AI summarization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this diary entry. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### PUT /api/trainer-diary/diary-entries/{id}/
`PUT /api/trainer-diary/diary-entries/{id}/`

ViewSet for diary entries with speech-to-text and AI summarization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this diary entry. |

#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### PATCH /api/trainer-diary/diary-entries/{id}/
`PATCH /api/trainer-diary/diary-entries/{id}/`

ViewSet for diary entries with speech-to-text and AI summarization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this diary entry. |

#### Request Body
Type: `PatchedDiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### DELETE /api/trainer-diary/diary-entries/{id}/
`DELETE /api/trainer-diary/diary-entries/{id}/`

ViewSet for diary entries with speech-to-text and AI summarization

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this diary entry. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### POST /api/trainer-diary/diary-entries/create-daily-summary/
`POST /api/trainer-diary/diary-entries/create-daily-summary/`

Create daily aggregated summary of teaching activities
POST /api/diary-entries/create-daily-summary/
Body: {trainer_id, summary_date, include_draft_entries}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### GET /api/trainer-diary/diary-entries/dashboard/
`GET /api/trainer-diary/diary-entries/dashboard/`

Get dashboard statistics for trainer diary
GET /api/diary-entries/dashboard/?trainer_id=X&tenant=Y



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### POST /api/trainer-diary/diary-entries/export-evidence/
`POST /api/trainer-diary/diary-entries/export-evidence/`

Export evidence documents for date range
POST /api/diary-entries/export-evidence/
Body: {trainer_id, start_date, end_date, export_format, include_transcripts, include_summaries, include_evidence_docs}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### POST /api/trainer-diary/diary-entries/generate-evidence/
`POST /api/trainer-diary/diary-entries/generate-evidence/`

Generate evidence document from diary entry
POST /api/diary-entries/generate-evidence/
Body: {diary_entry_id, document_type, document_format, include_attachments}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### POST /api/trainer-diary/diary-entries/generate-summary/
`POST /api/trainer-diary/diary-entries/generate-summary/`

Generate AI-powered summary of teaching session
POST /api/diary-entries/generate-summary/
Body: {diary_entry_id, include_transcript, include_manual_notes, summary_style}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### POST /api/trainer-diary/diary-entries/transcribe-audio/
`POST /api/trainer-diary/diary-entries/transcribe-audio/`

Transcribe audio recording to text using speech-to-text
POST /api/diary-entries/transcribe-audio/
Body: {recording_id, transcription_engine, language, enable_speaker_diarization}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### POST /api/trainer-diary/diary-entries/upload-audio/
`POST /api/trainer-diary/diary-entries/upload-audio/`

Upload audio recording for a diary entry
POST /api/diary-entries/upload-audio/
Body: {diary_entry_id, audio_file, recording_filename, language}


#### Request Body
Type: `DiaryEntryRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | DiaryEntry |

---

#### GET /api/trainer-diary/evidence-documents/
`GET /api/trainer-diary/evidence-documents/`

ViewSet for evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedEvidenceDocumentList |

---

#### POST /api/trainer-diary/evidence-documents/
`POST /api/trainer-diary/evidence-documents/`

ViewSet for evidence documents


#### Request Body
Type: `EvidenceDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | EvidenceDocument |

---

#### GET /api/trainer-diary/evidence-documents/{id}/
`GET /api/trainer-diary/evidence-documents/{id}/`

ViewSet for evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence document. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceDocument |

---

#### PUT /api/trainer-diary/evidence-documents/{id}/
`PUT /api/trainer-diary/evidence-documents/{id}/`

ViewSet for evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence document. |

#### Request Body
Type: `EvidenceDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceDocument |

---

#### PATCH /api/trainer-diary/evidence-documents/{id}/
`PATCH /api/trainer-diary/evidence-documents/{id}/`

ViewSet for evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence document. |

#### Request Body
Type: `PatchedEvidenceDocumentRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | EvidenceDocument |

---

#### DELETE /api/trainer-diary/evidence-documents/{id}/
`DELETE /api/trainer-diary/evidence-documents/{id}/`

ViewSet for evidence documents

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this evidence document. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

#### GET /api/trainer-diary/transcription-jobs/
`GET /api/trainer-diary/transcription-jobs/`

ViewSet for transcription jobs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedTranscriptionJobList |

---

#### POST /api/trainer-diary/transcription-jobs/
`POST /api/trainer-diary/transcription-jobs/`

ViewSet for transcription jobs


#### Request Body
Type: `TranscriptionJobRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | TranscriptionJob |

---

#### GET /api/trainer-diary/transcription-jobs/{id}/
`GET /api/trainer-diary/transcription-jobs/{id}/`

ViewSet for transcription jobs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this transcription job. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TranscriptionJob |

---

#### PUT /api/trainer-diary/transcription-jobs/{id}/
`PUT /api/trainer-diary/transcription-jobs/{id}/`

ViewSet for transcription jobs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this transcription job. |

#### Request Body
Type: `TranscriptionJobRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TranscriptionJob |

---

#### PATCH /api/trainer-diary/transcription-jobs/{id}/
`PATCH /api/trainer-diary/transcription-jobs/{id}/`

ViewSet for transcription jobs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this transcription job. |

#### Request Body
Type: `PatchedTranscriptionJobRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | TranscriptionJob |

---

#### DELETE /api/trainer-diary/transcription-jobs/{id}/
`DELETE /api/trainer-diary/transcription-jobs/{id}/`

ViewSet for transcription jobs

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | integer | Yes | A unique integer value identifying this transcription job. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 204 | No response body | any |

---

### users
#### POST /api/users/accept-invitation/
`POST /api/users/accept-invitation/`

Accept a tenant invitation.



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### PUT /api/users/change-password/
`PUT /api/users/change-password/`

Change user password.
Requires authentication.


#### Request Body
Type: `ChangePasswordRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChangePassword |

---

#### PATCH /api/users/change-password/
`PATCH /api/users/change-password/`

Change user password.
Requires authentication.


#### Request Body
Type: `PatchedChangePasswordRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | ChangePassword |

---

#### GET /api/users/invitations/
`GET /api/users/invitations/`

List and create invitations.
Only tenant admins/owners can create invitations.

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | No | Which field to use when ordering the results. |
| page | query | integer | No | A page number within the paginated result set. |
| search | query | string | No | A search term. |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | PaginatedUserInvitationList |

---

#### POST /api/users/invitations/
`POST /api/users/invitations/`

List and create invitations.
Only tenant admins/owners can create invitations.


#### Request Body
Type: `UserInvitationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | UserInvitation |

---

#### GET /api/users/invitations/{token}/
`GET /api/users/invitations/{token}/`

Get invitation details (public endpoint for preview before accepting).

#### Parameters
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| token | path | string | Yes |  |


#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### GET /api/users/my-tenants/
`GET /api/users/my-tenants/`

List all tenants the authenticated user belongs to.



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### GET /api/users/profile/
`GET /api/users/profile/`

View and update user profile.
Requires authentication.



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UserProfile |

---

#### PUT /api/users/profile/
`PUT /api/users/profile/`

View and update user profile.
Requires authentication.


#### Request Body
Type: `UserProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UserProfile |

---

#### PATCH /api/users/profile/
`PATCH /api/users/profile/`

View and update user profile.
Requires authentication.


#### Request Body
Type: `PatchedUserProfileRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 |  | UserProfile |

---

#### POST /api/users/register/
`POST /api/users/register/`

Public endpoint for user registration.
No authentication required.


#### Request Body
Type: `UserRegistrationRequest`

#### Responses
| Code | Description | Schema |
|---|---|---|
| 201 |  | UserRegistration |

---

#### POST /api/users/resend-verification/
`POST /api/users/resend-verification/`

Resend verification email.



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

#### POST /api/users/verify-email/
`POST /api/users/verify-email/`

Verify user email with token.



#### Responses
| Code | Description | Schema |
|---|---|---|
| 200 | No response body | any |

---

## Schemas
### AIRun
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| target_entity | string | Entity type (improvement_action, etc.) |
| target_id | integer | Entity primary key |
| task_type | AIRunTaskTypeEnum |  |
| task_type_display | string |  |
| input_ref | string | Reference to input data |
| output_json | object | AI output/predictions |
| success | boolean |  |
| error_message | string |  |
| tokens_used | integer |  |
| latency_ms | integer | Response time in ms |
| model_name | string |  |
| model_version | string |  |
| created_at | string |  |


### AIRunTaskTypeEnum
Type: `string`


### ASQAClause
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| standard | integer |  |
| clause_number | string | e.g., 1.1, 1.2, 1.3 |
| title | string |  |
| clause_text | string | Full text of the clause |
| evidence_required | object | Types of evidence needed |
| keywords | object | Key terms for text similarity |
| compliance_level | ComplianceLevelEnum |  |
| compliance_level_display | string |  |
| is_active | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### ASQAClauseRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| standard | integer |  |
| clause_number | string | e.g., 1.1, 1.2, 1.3 |
| title | string |  |
| clause_text | string | Full text of the clause |
| evidence_required | object | Types of evidence needed |
| keywords | object | Key terms for text similarity |
| compliance_level | ComplianceLevelEnum |  |
| is_active | boolean |  |


### ASQAStandard
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| standard_number | string | e.g., Standard 1.1 (2015) or QA1.1 (2025) |
| title | string |  |
| description | string |  |
| standard_type | StandardTypeEnum |  |
| standard_type_display | string |  |
| full_text | string | Complete text of the ASQA standard |
| requirements | object | List of specific requirements |
| is_active | boolean |  |
| effective_date | string |  |
| version | object |  |
| created_at | string |  |
| updated_at | string |  |
| clauses | [ASQAClause] |  |
| clause_count | string |  |


### ASQAStandardRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| standard_number | string | e.g., Standard 1.1 (2015) or QA1.1 (2025) |
| title | string |  |
| description | string |  |
| standard_type | StandardTypeEnum |  |
| full_text | string | Complete text of the ASQA standard |
| requirements | object | List of specific requirements |
| is_active | boolean |  |
| effective_date | string |  |
| version | object |  |


### ActionStep
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| title | string |  |
| description | string |  |
| sequence_order | integer | Order of execution |
| owner | integer |  |
| owner_name | string |  |
| status | ActionStepStatusEnum |  |
| status_display | string |  |
| due_date | string |  |
| started_at | string |  |
| completed_at | string |  |
| progress_notes | string |  |
| evidence_refs | object | References to evidence documents/files |
| is_blocked | boolean |  |
| blocker_description | string |  |
| blocker_resolved_at | string |  |
| is_overdue | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### ActionStepRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| title | string |  |
| description | string |  |
| sequence_order | integer | Order of execution |
| owner | integer |  |
| status | ActionStepStatusEnum |  |
| due_date | string |  |
| started_at | string |  |
| completed_at | string |  |
| progress_notes | string |  |
| evidence_refs | object | References to evidence documents/files |
| is_blocked | boolean |  |
| blocker_description | string |  |
| blocker_resolved_at | string |  |


### ActionStepStatusEnum
Type: `string`


### ActionTracking
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| update_type | UpdateTypeEnum |  |
| update_type_display | string |  |
| update_text | string | Description of the update |
| progress_percentage | integer | Overall progress (0-100) |
| old_status | string |  |
| new_status | string |  |
| is_blocker | boolean |  |
| blocker_resolved | boolean |  |
| blocker_resolution | string |  |
| evidence_provided | object | Evidence of progress (file URLs, references) |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |


### ActionTrackingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| update_type | UpdateTypeEnum |  |
| update_text | string | Description of the update |
| progress_percentage | integer | Overall progress (0-100) |
| old_status | string |  |
| new_status | string |  |
| is_blocker | boolean |  |
| blocker_resolved | boolean |  |
| blocker_resolution | string |  |
| evidence_provided | object | Evidence of progress (file URLs, references) |
| created_by | integer |  |


### ActivityType9adEnum
Type: `string`


### AddressesCurrencyGapEnum
Type: `string`


### AlertTypeEnum
Type: `string`


### AlgorithmUsedEnum
Type: `string`


### AnomalyDetection
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| anomaly_number | string |  |
| submission_analysis | integer |  |
| anomaly_type | AnomalyTypeEnum |  |
| anomaly_type_display | string |  |
| severity | SeverityE88Enum |  |
| severity_display | string |  |
| anomaly_data | object | Detailed anomaly data and evidence |
| description | string |  |
| confidence_score | number | Confidence in anomaly detection (0.0-1.0) |
| impact_score | number | Impact on integrity score (0-100) |
| acknowledged | boolean |  |
| false_positive | boolean |  |
| resolution_notes | string |  |
| detected_at | string |  |


### AnomalyDetectionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| submission_analysis | integer |  |
| anomaly_type | AnomalyTypeEnum |  |
| severity | SeverityE88Enum |  |
| anomaly_data | object | Detailed anomaly data and evidence |
| description | string |  |
| confidence_score | number | Confidence in anomaly detection (0.0-1.0) |
| acknowledged | boolean |  |
| false_positive | boolean |  |
| resolution_notes | string |  |


### AnomalyTypeEnum
Type: `string`


### AnswerTypeEnum
Type: `string`


### AqfLevelEnum
Type: `string`


### Assessment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| assessment_number | string |  |
| unit_code | string | Training package unit code (e.g., BSBWHS211) |
| unit_title | string |  |
| training_package | string | e.g., BSB - Business Services |
| unit_release | string | Release number |
| assessment_type | AssessmentType64bEnum |  |
| assessment_type_display | string |  |
| title | string |  |
| version | string |  |
| instructions | string | AI-generated assessment instructions |
| context | string | Assessment context and scenario |
| conditions | string | Assessment conditions (equipment, resources, etc.) |
| ai_generated | boolean |  |
| ai_model | string | e.g., GPT-4 |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| blooms_analysis | object | Bloom's taxonomy verb analysis: {level: count} |
| blooms_distribution | object | Distribution percentages across Bloom's levels |
| dominant_blooms_level | string | Most prominent Bloom's level |
| is_compliant | boolean |  |
| compliance_score | integer | Overall compliance score (0-100) |
| compliance_notes | string |  |
| elements_covered | object | List of unit elements covered |
| performance_criteria_covered | object | List of performance criteria covered |
| knowledge_evidence_covered | object | List of knowledge evidence items covered |
| performance_evidence_covered | object | List of performance evidence items covered |
| estimated_duration_hours | string | Estimated completion time in hours |
| status | Status304Enum |  |
| status_display | string |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| approved_by_name | string |  |
| approved_at | string |  |
| task_count | integer |  |
| total_questions | integer |  |
| created_at | string |  |
| updated_at | string |  |
| created_by_name | string |  |


### AssessmentCriteria
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| task | integer | Optional: Link to specific task |
| criterion_number | string |  |
| criterion_text | string | What the student must demonstrate |
| unit_element | string |  |
| performance_criterion | string |  |
| knowledge_evidence | string |  |
| satisfactory_evidence | string | What constitutes satisfactory performance |
| not_satisfactory_evidence | string | What would be unsatisfactory |
| ai_generated | boolean |  |
| display_order | integer |  |
| created_at | string |  |


### AssessmentCriteriaRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| task | integer | Optional: Link to specific task |
| criterion_number | string |  |
| criterion_text | string | What the student must demonstrate |
| unit_element | string |  |
| performance_criterion | string |  |
| knowledge_evidence | string |  |
| satisfactory_evidence | string | What constitutes satisfactory performance |
| not_satisfactory_evidence | string | What would be unsatisfactory |
| ai_generated | boolean |  |
| display_order | integer |  |


### AssessmentDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| assessment_number | string |  |
| unit_code | string | Training package unit code (e.g., BSBWHS211) |
| unit_title | string |  |
| training_package | string | e.g., BSB - Business Services |
| unit_release | string | Release number |
| assessment_type | AssessmentType64bEnum |  |
| assessment_type_display | string |  |
| title | string |  |
| version | string |  |
| instructions | string | AI-generated assessment instructions |
| context | string | Assessment context and scenario |
| conditions | string | Assessment conditions (equipment, resources, etc.) |
| ai_generated | boolean |  |
| ai_model | string | e.g., GPT-4 |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| blooms_analysis | object | Bloom's taxonomy verb analysis: {level: count} |
| blooms_distribution | object | Distribution percentages across Bloom's levels |
| dominant_blooms_level | string | Most prominent Bloom's level |
| is_compliant | boolean |  |
| compliance_score | integer | Overall compliance score (0-100) |
| compliance_notes | string |  |
| elements_covered | object | List of unit elements covered |
| performance_criteria_covered | object | List of performance criteria covered |
| knowledge_evidence_covered | object | List of knowledge evidence items covered |
| performance_evidence_covered | object | List of performance evidence items covered |
| estimated_duration_hours | string | Estimated completion time in hours |
| status | Status304Enum |  |
| status_display | string |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| approved_by_name | string |  |
| approved_at | string |  |
| task_count | integer |  |
| total_questions | integer |  |
| created_at | string |  |
| updated_at | string |  |
| created_by_name | string |  |
| tasks | [AssessmentTask] |  |
| criteria | [AssessmentCriteria] |  |


### AssessmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| unit_code | string | Training package unit code (e.g., BSBWHS211) |
| unit_title | string |  |
| training_package | string | e.g., BSB - Business Services |
| unit_release | string | Release number |
| assessment_type | AssessmentType64bEnum |  |
| title | string |  |
| version | string |  |
| instructions | string | AI-generated assessment instructions |
| context | string | Assessment context and scenario |
| conditions | string | Assessment conditions (equipment, resources, etc.) |
| ai_generated | boolean |  |
| ai_model | string | e.g., GPT-4 |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| blooms_analysis | object | Bloom's taxonomy verb analysis: {level: count} |
| blooms_distribution | object | Distribution percentages across Bloom's levels |
| dominant_blooms_level | string | Most prominent Bloom's level |
| is_compliant | boolean |  |
| compliance_score | integer | Overall compliance score (0-100) |
| compliance_notes | string |  |
| elements_covered | object | List of unit elements covered |
| performance_criteria_covered | object | List of performance criteria covered |
| knowledge_evidence_covered | object | List of knowledge evidence items covered |
| performance_evidence_covered | object | List of performance evidence items covered |
| estimated_duration_hours | string | Estimated completion time in hours |
| status | Status304Enum |  |
| reviewed_at | string |  |
| approved_at | string |  |


### AssessmentTask
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| task_number | string | e.g., '1', '1a', 'A.1' |
| task_type | AssessmentTaskTaskTypeEnum |  |
| task_type_display | string |  |
| question | string | The task question or instruction |
| context | string | Additional context, scenario, or information for the task |
| ai_generated | boolean |  |
| ai_rationale | string | AI explanation of why this task was generated |
| blooms_level | string | Primary Bloom's taxonomy level |
| blooms_level_display | string |  |
| blooms_verbs | object | Bloom's taxonomy verbs detected in this task |
| maps_to_elements | object | Unit elements this task addresses |
| maps_to_performance_criteria | object | Performance criteria this task addresses |
| maps_to_knowledge_evidence | object | Knowledge evidence this task addresses |
| question_count | integer | Number of sub-questions (for multi-part tasks) |
| estimated_time_minutes | integer | Estimated completion time in minutes |
| marks_available | integer | Total marks for this task |
| display_order | integer |  |
| created_at | string |  |
| updated_at | string |  |


### AssessmentTaskRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| task_number | string | e.g., '1', '1a', 'A.1' |
| task_type | AssessmentTaskTaskTypeEnum |  |
| question | string | The task question or instruction |
| context | string | Additional context, scenario, or information for the task |
| ai_generated | boolean |  |
| ai_rationale | string | AI explanation of why this task was generated |
| blooms_level | string | Primary Bloom's taxonomy level |
| blooms_verbs | object | Bloom's taxonomy verbs detected in this task |
| maps_to_elements | object | Unit elements this task addresses |
| maps_to_performance_criteria | object | Performance criteria this task addresses |
| maps_to_knowledge_evidence | object | Knowledge evidence this task addresses |
| question_count | integer | Number of sub-questions (for multi-part tasks) |
| estimated_time_minutes | integer | Estimated completion time in minutes |
| marks_available | integer | Total marks for this task |
| display_order | integer |  |


### AssessmentTaskTaskTypeEnum
Type: `string`


### AssessmentType64bEnum
Type: `string`


### AssessorDecision
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| percentage_score | string |  |
| decision_number | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| assessor_id | string |  |
| assessor_name | string |  |
| score | number |  |
| max_score | number |  |
| grade | GradeEnum |  |
| criterion_scores | object | Dictionary of criterion_id -> score |
| is_outlier | boolean |  |
| has_bias_flag | boolean |  |
| requires_review | boolean |  |
| comments | string |  |
| marking_time_minutes | integer |  |
| marked_at | string |  |
| created_at | string |  |
| session | integer |  |


### AssessorDecisionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| assessor_id | string |  |
| assessor_name | string |  |
| score | number |  |
| max_score | number |  |
| grade | GradeEnum |  |
| criterion_scores | object | Dictionary of criterion_id -> score |
| requires_review | boolean |  |
| comments | string |  |
| marking_time_minutes | integer |  |
| marked_at | string |  |
| session | integer |  |


### AssignmentStatusEnum
Type: `string`


### Attachment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| file_uri | string | S3 URI or file path |
| filename | string |  |
| file_size | integer | Size in bytes |
| file_size_mb | string |  |
| mime_type | string |  |
| kind | KindEnum |  |
| kind_display | string |  |
| sha256_hash | string | File integrity hash |
| description | string |  |
| uploaded_by | integer |  |
| uploaded_by_name | string |  |
| uploaded_at | string |  |


### AttachmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| file_uri | string | S3 URI or file path |
| filename | string |  |
| file_size | integer | Size in bytes |
| mime_type | string |  |
| kind | KindEnum |  |
| sha256_hash | string | File integrity hash |
| description | string |  |


### AttendanceRecord
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| record_number | string |  |
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| status | AttendanceRecordStatusEnum |  |
| session_name | string |  |
| scheduled_start | string |  |
| scheduled_end | string |  |
| actual_arrival | string |  |
| actual_departure | string |  |
| minutes_late | integer |  |
| minutes_attended | integer |  |
| participation_level | ParticipationLevelEnum |  |
| notes | string |  |
| created_at | string |  |


### AttendanceRecordRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| status | AttendanceRecordStatusEnum |  |
| session_name | string |  |
| scheduled_start | string |  |
| scheduled_end | string |  |
| actual_arrival | string |  |
| actual_departure | string |  |
| minutes_late | integer |  |
| minutes_attended | integer |  |
| participation_level | ParticipationLevelEnum |  |
| notes | string |  |


### AttendanceRecordStatusEnum
Type: `string`


### AudioRecording
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| recording_number | string |  |
| recording_filename | string |  |
| recording_file_path | string |  |
| recording_file_size_mb | number |  |
| recording_duration_seconds | number |  |
| recording_format | string |  |
| transcript_text | string |  |
| transcript_confidence | number |  |
| transcript_language | string |  |
| processing_status | ProcessingStatusEnum |  |
| error_message | string |  |
| uploaded_at | string |  |
| processed_at | string |  |
| diary_entry | integer |  |


### AudioRecordingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| recording_filename | string |  |
| recording_file_path | string |  |
| recording_file_size_mb | number |  |
| recording_duration_seconds | number |  |
| recording_format | string |  |
| transcript_text | string |  |
| transcript_confidence | number |  |
| transcript_language | string |  |
| processing_status | ProcessingStatusEnum |  |
| error_message | string |  |
| diary_entry | integer |  |


### Audit
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant_id | string |  |
| event_type | string |  |
| severity | string |  |
| actor_type | string |  |
| actor_id | string |  |
| actor_username | string |  |
| resource_type | string |  |
| resource_id | string |  |
| action | string |  |
| status | string |  |
| ip_address | string |  |
| user_agent | string |  |
| metadata | string |  |
| timestamp | string |  |
| hash | string |  |
| prev_hash | string |  |
| payload | any |  |


### AuditLog
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| log_number | string |  |
| tenant | string |  |
| action_type | AuditLogActionTypeEnum |  |
| action_description | string |  |
| performed_by | string |  |
| performed_by_role | string |  |
| changes | any |  |
| ip_address | string |  |
| user_agent | string |  |
| timestamp | string |  |
| intervention | integer |  |


### AuditLogActionTypeEnum
Type: `string`


### AuditLogRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| action_type | AuditLogActionTypeEnum |  |
| action_description | string |  |
| performed_by | string |  |
| performed_by_role | string |  |
| changes | any |  |
| ip_address | string |  |
| user_agent | string |  |
| intervention | integer |  |


### AuditReport
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| report_number | string |  |
| title | string |  |
| description | string |  |
| asqa_standards | [integer] | ASQA standards included in this audit |
| standards_count | string |  |
| standards_details | string |  |
| audit_period_start | string | Start date of audit period |
| audit_period_end | string | End date of audit period |
| status | Status9adEnum |  |
| status_display | string |  |
| total_clauses | integer |  |
| clauses_with_evidence | integer |  |
| clauses_without_evidence | integer |  |
| compliance_percentage | number | Percentage of clauses with evidence |
| critical_clauses_count | integer |  |
| critical_clauses_covered | integer |  |
| critical_compliance_percentage | number |  |
| total_evidence_count | integer |  |
| auto_tagged_count | integer | Evidence auto-tagged via NER |
| manually_tagged_count | integer |  |
| verified_evidence_count | integer |  |
| findings | object | List of findings: [{clause: str, finding: str, severity: str, recommendation: str}] |
| recommendations | object | Overall recommendations |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| updated_at | string |  |
| completed_at | string |  |
| submitted_at | string |  |
| submitted_by | integer |  |
| submitted_by_name | string |  |
| clause_entries_count | string |  |


### AuditReportClause
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| asqa_clause | integer |  |
| clause_number | string |  |
| clause_title | string |  |
| clause_text | string |  |
| clause_compliance_level | string |  |
| standard_name | string |  |
| compliance_status | AuditReportClauseComplianceStatusEnum |  |
| compliance_status_display | string |  |
| evidence_count | integer |  |
| verified_evidence_count | integer |  |
| evidence_details | string |  |
| finding | string | Audit finding for this clause |
| severity | object |  |
| recommendation | string |  |
| assessed_by | integer |  |
| assessed_by_name | string |  |
| assessed_at | string |  |
| notes | string |  |
| created_at | string |  |
| updated_at | string |  |


### AuditReportClauseComplianceStatusEnum
Type: `string`


### AuditReportClauseSeverityEnum
Type: `string`


### AuditReportDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| report_number | string |  |
| title | string |  |
| description | string |  |
| asqa_standards | [integer] | ASQA standards included in this audit |
| standards_count | string |  |
| standards_details | string |  |
| audit_period_start | string | Start date of audit period |
| audit_period_end | string | End date of audit period |
| status | Status9adEnum |  |
| status_display | string |  |
| total_clauses | integer |  |
| clauses_with_evidence | integer |  |
| clauses_without_evidence | integer |  |
| compliance_percentage | number | Percentage of clauses with evidence |
| critical_clauses_count | integer |  |
| critical_clauses_covered | integer |  |
| critical_compliance_percentage | number |  |
| total_evidence_count | integer |  |
| auto_tagged_count | integer | Evidence auto-tagged via NER |
| manually_tagged_count | integer |  |
| verified_evidence_count | integer |  |
| findings | object | List of findings: [{clause: str, finding: str, severity: str, recommendation: str}] |
| recommendations | object | Overall recommendations |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| updated_at | string |  |
| completed_at | string |  |
| submitted_at | string |  |
| submitted_by | integer |  |
| submitted_by_name | string |  |
| clause_entries_count | string |  |
| clause_entries | [AuditReportClause] |  |


### AuditReportRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| report_number | string |  |
| title | string |  |
| description | string |  |
| asqa_standards | [integer] | ASQA standards included in this audit |
| audit_period_start | string | Start date of audit period |
| audit_period_end | string | End date of audit period |
| status | Status9adEnum |  |
| findings | object | List of findings: [{clause: str, finding: str, severity: str, recommendation: str}] |
| recommendations | object | Overall recommendations |
| created_by | integer |  |
| completed_at | string |  |
| submitted_at | string |  |
| submitted_by | integer |  |


### AuthToken
Type: `object`

| Property | Type | Description |
|---|---|---|
| token | string |  |


### AuthTokenRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| username | string |  |
| password | string |  |


### AuthenticityCheck
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| check_number | string |  |
| assessment | integer |  |
| assessment_title | string |  |
| name | string |  |
| description | string |  |
| plagiarism_threshold | number | Similarity threshold for plagiarism detection (0.0-1.0) |
| metadata_verification_enabled | boolean |  |
| anomaly_detection_enabled | boolean |  |
| academic_integrity_mode | boolean | Enable strict academic integrity compliance |
| status | Status24eEnum |  |
| status_display | string |  |
| total_submissions_checked | integer |  |
| plagiarism_cases_detected | integer |  |
| metadata_issues_found | integer |  |
| anomalies_detected | integer |  |
| overall_integrity_score | number | Overall integrity score (0-100) |
| created_at | string |  |
| updated_at | string |  |
| created_by | integer |  |
| submission_analyses | [SubmissionAnalysisList] |  |


### AuthenticityCheckList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| check_number | string |  |
| assessment_title | string |  |
| name | string |  |
| status | Status24eEnum |  |
| status_display | string |  |
| total_submissions_checked | integer |  |
| plagiarism_cases_detected | integer |  |
| metadata_issues_found | integer |  |
| anomalies_detected | integer |  |
| overall_integrity_score | number | Overall integrity score (0-100) |
| created_at | string |  |


### AuthenticityCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| assessment | integer |  |
| name | string |  |
| description | string |  |
| plagiarism_threshold | number | Similarity threshold for plagiarism detection (0.0-1.0) |
| metadata_verification_enabled | boolean |  |
| anomaly_detection_enabled | boolean |  |
| academic_integrity_mode | boolean | Enable strict academic integrity compliance |
| status | Status24eEnum |  |
| created_by | integer |  |


### AutoMarkerDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| marker_number | string |  |
| title | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| answer_type | AnswerTypeEnum |  |
| question_text | string | The question being asked |
| model_answer | string | The ideal/model answer for comparison |
| max_marks | integer |  |
| similarity_model | SimilarityModelEnum |  |
| similarity_threshold | number | Minimum similarity score for full marks (0.0-1.0) |
| partial_credit_enabled | boolean |  |
| min_similarity_for_credit | number | Minimum similarity for partial credit |
| use_keywords | boolean | Enable keyword matching |
| keywords | object | Required keywords for full marks |
| keyword_weight | number | Weight of keyword matching in final score |
| total_responses_marked | integer |  |
| average_similarity_score | number |  |
| average_marking_time | number | Average time in seconds |
| status | Status86cEnum |  |
| criteria | [MarkingCriterion] |  |
| statistics | string |  |
| created_at | string |  |
| updated_at | string |  |


### AutoMarkerDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| answer_type | AnswerTypeEnum |  |
| question_text | string | The question being asked |
| model_answer | string | The ideal/model answer for comparison |
| max_marks | integer |  |
| similarity_model | SimilarityModelEnum |  |
| similarity_threshold | number | Minimum similarity score for full marks (0.0-1.0) |
| partial_credit_enabled | boolean |  |
| min_similarity_for_credit | number | Minimum similarity for partial credit |
| use_keywords | boolean | Enable keyword matching |
| keywords | object | Required keywords for full marks |
| keyword_weight | number | Weight of keyword matching in final score |
| status | Status86cEnum |  |


### AutoMarkerList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| marker_number | string |  |
| title | string |  |
| description | string |  |
| tenant | string |  |
| answer_type | AnswerTypeEnum |  |
| max_marks | integer |  |
| status | Status86cEnum |  |
| similarity_model | SimilarityModelEnum |  |
| similarity_threshold | number | Minimum similarity score for full marks (0.0-1.0) |
| total_responses_marked | integer |  |
| average_similarity_score | number |  |
| average_marking_time | number | Average time in seconds |
| total_responses | string |  |
| pending_review | string |  |
| created_at | string |  |
| updated_at | string |  |


### AutoMarkerListRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| tenant | string |  |
| answer_type | AnswerTypeEnum |  |
| max_marks | integer |  |
| status | Status86cEnum |  |
| similarity_model | SimilarityModelEnum |  |
| similarity_threshold | number | Minimum similarity score for full marks (0.0-1.0) |
| total_responses_marked | integer |  |
| average_similarity_score | number |  |
| average_marking_time | number | Average time in seconds |


### BiasScore
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| severity_label | string |  |
| bias_number | string |  |
| assessor_id | string |  |
| assessor_name | string |  |
| bias_type | BiasTypeEnum |  |
| bias_score | number | Bias score (0=no bias, 1=severe bias) |
| sample_size | integer | Number of decisions analyzed |
| mean_difference | number | Difference from cohort mean |
| std_dev_ratio | number | Ratio to cohort standard deviation |
| evidence | object | Statistical evidence and patterns detected |
| affected_students | object | List of student IDs affected by bias |
| is_validated | boolean |  |
| validation_notes | string |  |
| validated_by | string |  |
| validated_at | string |  |
| recommendation | string | Action recommended to address bias |
| severity_level | integer | Severity level (1=minor, 10=critical) |
| calculated_at | string |  |
| session | integer |  |


### BiasScoreRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| assessor_id | string |  |
| assessor_name | string |  |
| bias_type | BiasTypeEnum |  |
| bias_score | number | Bias score (0=no bias, 1=severe bias) |
| sample_size | integer | Number of decisions analyzed |
| mean_difference | number | Difference from cohort mean |
| std_dev_ratio | number | Ratio to cohort standard deviation |
| evidence | object | Statistical evidence and patterns detected |
| affected_students | object | List of student IDs affected by bias |
| is_validated | boolean |  |
| validation_notes | string |  |
| validated_by | string |  |
| validated_at | string |  |
| recommendation | string | Action recommended to address bias |
| severity_level | integer | Severity level (1=minor, 10=critical) |
| session | integer |  |


### BiasTypeEnum
Type: `string`


### BlankEnum
Type: `object`


### BusinessStructureEnum
Type: `string`


### CategoryTypeEnum
Type: `string`


### ChangePassword
Type: `object`

| Property | Type | Description |
|---|---|---|
| old_password | string |  |
| new_password | string |  |
| new_password_confirm | string |  |


### ChangePasswordRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| old_password | string |  |
| new_password | string |  |
| new_password_confirm | string |  |


### ChatMessage
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| message_number | string |  |
| role | ChatMessageRoleEnum |  |
| content | string |  |
| model_used | string |  |
| prompt_tokens | integer |  |
| completion_tokens | integer |  |
| total_tokens | integer |  |
| response_time_ms | integer |  |
| context_used | any |  |
| vector_search_results | any |  |
| relevance_scores | any |  |
| sentiment | object |  |
| intent_detected | string |  |
| created_at | string |  |
| session | integer |  |


### ChatMessageRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| role | ChatMessageRoleEnum |  |
| content | string |  |
| model_used | string |  |
| prompt_tokens | integer |  |
| completion_tokens | integer |  |
| total_tokens | integer |  |
| response_time_ms | integer |  |
| context_used | any |  |
| vector_search_results | any |  |
| relevance_scores | any |  |
| sentiment | object |  |
| intent_detected | string |  |
| session | integer |  |


### ChatMessageRoleEnum
Type: `string`


### ChatMessageSentimentEnum
Type: `string`


### ChatSession
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| messages | [ChatMessage] |  |
| session_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| subject | string |  |
| topic | string |  |
| session_type | SessionTypeEnum |  |
| status | StatusF84Enum |  |
| message_count | integer |  |
| total_duration_minutes | integer |  |
| satisfaction_rating | integer |  |
| student_feedback | string |  |
| referenced_materials | any |  |
| key_concepts_discussed | any |  |
| follow_up_needed | boolean |  |
| follow_up_reason | string |  |
| created_at | string |  |
| updated_at | string |  |
| completed_at | string |  |


### ChatSessionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| session_number | string |  |
| student_name | string |  |
| subject | string |  |
| topic | string |  |
| session_type | SessionTypeEnum |  |
| status | StatusF84Enum |  |
| message_count | integer |  |
| satisfaction_rating | integer |  |
| created_at | string |  |
| updated_at | string |  |


### ChatSessionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| subject | string |  |
| topic | string |  |
| session_type | SessionTypeEnum |  |
| status | StatusF84Enum |  |
| message_count | integer |  |
| total_duration_minutes | integer |  |
| satisfaction_rating | integer |  |
| student_feedback | string |  |
| referenced_materials | any |  |
| key_concepts_discussed | any |  |
| follow_up_needed | boolean |  |
| follow_up_reason | string |  |
| completed_at | string |  |


### CheckStatusEnum
Type: `string`


### ClauseEvidence
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| asqa_clause | integer |  |
| clause_number | string |  |
| clause_title | string |  |
| clause_compliance_level | string |  |
| evidence | integer |  |
| evidence_number | string |  |
| evidence_title | string |  |
| evidence_type | string |  |
| mapping_type | MappingTypeEnum |  |
| mapping_type_display | string |  |
| confidence_score | number | Confidence score (0.0-1.0) for auto-tagged matches |
| matched_entities | object | NER entities that triggered this mapping: [{entity: str, type: str}] |
| matched_keywords | object | Keywords that matched between clause and evidence |
| rule_name | string | Name of rule that triggered mapping |
| rule_metadata | object | Additional rule processing data |
| is_verified | boolean | Manually verified by reviewer |
| verified_by | integer |  |
| verified_by_name | string |  |
| verified_at | string |  |
| relevance_notes | string | Notes on evidence relevance to clause |
| created_at | string |  |
| updated_at | string |  |


### ClauseEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| asqa_clause | integer |  |
| evidence | integer |  |
| mapping_type | MappingTypeEnum |  |
| confidence_score | number | Confidence score (0.0-1.0) for auto-tagged matches |
| matched_entities | object | NER entities that triggered this mapping: [{entity: str, type: str}] |
| matched_keywords | object | Keywords that matched between clause and evidence |
| rule_name | string | Name of rule that triggered mapping |
| rule_metadata | object | Additional rule processing data |
| is_verified | boolean | Manually verified by reviewer |
| verified_by | integer |  |
| verified_at | string |  |
| relevance_notes | string | Notes on evidence relevance to clause |


### ClauseLink
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| clause | integer |  |
| clause_number | string |  |
| clause_title | string |  |
| standard_name | string |  |
| source | ClauseLinkSourceEnum |  |
| source_display | string |  |
| confidence | number | Confidence score for AI suggestions (0.0-1.0) |
| rationale | string | Explanation for the clause link |
| reviewed | boolean |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |


### ClauseLinkRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| clause | integer |  |
| source | ClauseLinkSourceEnum |  |
| confidence | number | Confidence score for AI suggestions (0.0-1.0) |
| rationale | string | Explanation for the clause link |
| reviewed | boolean |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |


### ClauseLinkSourceEnum
Type: `string`


### CoachConfiguration
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| primary_model | string |  |
| fallback_model | string |  |
| temperature | number |  |
| max_tokens | integer |  |
| coaching_style | CoachingStyleEnum |  |
| personality_traits | any |  |
| system_prompt | string |  |
| response_guidelines | any |  |
| prohibited_topics | any |  |
| vector_db_enabled | boolean |  |
| top_k_results | integer |  |
| similarity_threshold | number |  |
| content_filter_enabled | boolean |  |
| profanity_filter | boolean |  |
| escalation_keywords | any |  |
| available_24_7 | boolean |  |
| business_hours_only | boolean |  |
| timezone | string |  |
| created_at | string |  |
| updated_at | string |  |


### CoachConfigurationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| primary_model | string |  |
| fallback_model | string |  |
| temperature | number |  |
| max_tokens | integer |  |
| coaching_style | CoachingStyleEnum |  |
| personality_traits | any |  |
| system_prompt | string |  |
| response_guidelines | any |  |
| prohibited_topics | any |  |
| vector_db_enabled | boolean |  |
| top_k_results | integer |  |
| similarity_threshold | number |  |
| content_filter_enabled | boolean |  |
| profanity_filter | boolean |  |
| escalation_keywords | any |  |
| available_24_7 | boolean |  |
| business_hours_only | boolean |  |
| timezone | string |  |


### CoachingInsight
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| insight_number | string |  |
| tenant | string |  |
| student_id | string |  |
| time_period | string |  |
| total_sessions | integer |  |
| total_messages | integer |  |
| total_duration_minutes | integer |  |
| average_session_length | number |  |
| session_type_distribution | any |  |
| most_discussed_subjects | any |  |
| most_discussed_topics | any |  |
| knowledge_gaps_identified | any |  |
| average_sentiment_score | number |  |
| sentiment_trend | SentimentTrendEnum |  |
| average_satisfaction | number |  |
| sessions_with_feedback | integer |  |
| recommended_resources | any |  |
| follow_up_actions | any |  |
| at_risk_indicators | any |  |
| created_at | string |  |
| updated_at | string |  |


### CoachingInsightRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| time_period | string |  |
| total_sessions | integer |  |
| total_messages | integer |  |
| total_duration_minutes | integer |  |
| average_session_length | number |  |
| session_type_distribution | any |  |
| most_discussed_subjects | any |  |
| most_discussed_topics | any |  |
| knowledge_gaps_identified | any |  |
| average_sentiment_score | number |  |
| sentiment_trend | SentimentTrendEnum |  |
| average_satisfaction | number |  |
| sessions_with_feedback | integer |  |
| recommended_resources | any |  |
| follow_up_actions | any |  |
| at_risk_indicators | any |  |


### CoachingStyleEnum
Type: `string`


### Comment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| body | string |  |
| visibility | Visibility757Enum |  |
| visibility_display | string |  |
| parent | integer |  |
| mentioned_users | [integer] |  |
| author | integer |  |
| author_name | string |  |
| author_email | string |  |
| created_at | string |  |
| updated_at | string |  |
| edited | boolean |  |
| replies_count | string |  |


### CommentDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| body | string |  |
| visibility | Visibility757Enum |  |
| visibility_display | string |  |
| parent | integer |  |
| mentioned_users | [integer] |  |
| author | integer |  |
| author_name | string |  |
| author_email | string |  |
| created_at | string |  |
| updated_at | string |  |
| edited | boolean |  |
| replies_count | string |  |
| replies | string |  |


### CommentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| body | string |  |
| visibility | Visibility757Enum |  |
| parent | integer |  |
| mentioned_users | [integer] |  |


### CommunicationMethodEnum
Type: `string`


### ComparisonSession
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| policy | integer |  |
| policy_details | object |  |
| session_name | string |  |
| status | object |  |
| status_display | string |  |
| standards_compared | object | List of ASQA standard IDs compared |
| total_clauses_checked | integer |  |
| compliant_count | integer |  |
| partial_match_count | integer |  |
| gap_count | integer |  |
| overall_compliance_score | number |  |
| processing_time_seconds | number |  |
| error_message | string |  |
| created_by | integer |  |
| created_by_details | object |  |
| created_at | string |  |
| completed_at | string |  |


### CompetencyGap
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| unit_details | object |  |
| gap_id | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| gap_type | GapTypeEnum |  |
| gap_severity | GapSeverityEnum |  |
| gap_description | string |  |
| required_qualification | string |  |
| required_competency | string |  |
| required_experience_years | integer |  |
| current_qualifications | any |  |
| is_resolved | boolean |  |
| resolution_date | string |  |
| resolution_notes | string |  |
| recommended_action | string |  |
| estimated_resolution_time | string |  |
| created_at | string |  |
| updated_at | string |  |
| unit | integer |  |
| assignment | integer |  |


### CompetencyGapRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| gap_type | GapTypeEnum |  |
| gap_severity | GapSeverityEnum |  |
| gap_description | string |  |
| required_qualification | string |  |
| required_competency | string |  |
| required_experience_years | integer |  |
| current_qualifications | any |  |
| is_resolved | boolean |  |
| resolution_date | string |  |
| resolution_notes | string |  |
| recommended_action | string |  |
| estimated_resolution_time | string |  |
| unit | integer |  |
| assignment | integer |  |


### CompletionStatusEnum
Type: `string`


### ComplianceCheck
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| compliance_percentage | string |  |
| duration_display | string |  |
| check_id | string |  |
| tenant | string |  |
| check_type | string |  |
| check_status | CheckStatusEnum |  |
| trainer_ids | any |  |
| unit_codes | any |  |
| total_assignments_checked | integer |  |
| compliant_assignments | integer |  |
| non_compliant_assignments | integer |  |
| gaps_found | integer |  |
| critical_gaps | integer |  |
| high_gaps | integer |  |
| medium_gaps | integer |  |
| low_gaps | integer |  |
| overall_compliance_score | number |  |
| report_summary | string |  |
| detailed_results | any |  |
| recommendations | any |  |
| started_at | string |  |
| completed_at | string |  |
| execution_time_seconds | number |  |
| error_message | string |  |
| created_at | string |  |
| updated_at | string |  |


### ComplianceCheckDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| trainer_name | string |  |
| trainer_role | string |  |
| compliance_percentage | string |  |
| is_urgent | string |  |
| check_number | string |  |
| check_date | string |  |
| check_period_start | string |  |
| check_period_end | string |  |
| checked_by | string |  |
| overall_status | OverallStatusEnum |  |
| rules_checked | any |  |
| rules_met | any |  |
| rules_not_met | any |  |
| compliance_score | number |  |
| hours_required | number |  |
| hours_completed | number |  |
| hours_shortfall | number |  |
| findings | any |  |
| recommendations | any |  |
| requires_action | boolean |  |
| action_deadline | string |  |
| actions_taken | string |  |
| created_at | string |  |
| trainer_profile | integer |  |


### ComplianceCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| check_type | string |  |
| check_status | CheckStatusEnum |  |
| trainer_ids | any |  |
| unit_codes | any |  |
| total_assignments_checked | integer |  |
| compliant_assignments | integer |  |
| non_compliant_assignments | integer |  |
| gaps_found | integer |  |
| critical_gaps | integer |  |
| high_gaps | integer |  |
| medium_gaps | integer |  |
| low_gaps | integer |  |
| overall_compliance_score | number |  |
| report_summary | string |  |
| detailed_results | any |  |
| recommendations | any |  |
| started_at | string |  |
| completed_at | string |  |
| execution_time_seconds | number |  |
| error_message | string |  |


### ComplianceLevelEnum
Type: `string`


### ComplianceRule
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| rule_number | string |  |
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| regulatory_source | RegulatorySourceEnum |  |
| reference_code | string |  |
| applies_to_roles | any |  |
| applies_to_sectors | any |  |
| applies_to_qualifications | any |  |
| requirement_type | RequirementTypeEnum |  |
| requirement_details | any |  |
| is_active | boolean |  |
| effective_date | string |  |
| expiry_date | string |  |
| created_at | string |  |
| updated_at | string |  |


### ComplianceRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| regulatory_source | RegulatorySourceEnum |  |
| reference_code | string |  |
| applies_to_roles | any |  |
| applies_to_sectors | any |  |
| applies_to_qualifications | any |  |
| requirement_type | RequirementTypeEnum |  |
| requirement_details | any |  |
| is_active | boolean |  |
| effective_date | string |  |
| expiry_date | string |  |


### ComplianceStatusF51Enum
Type: `string`


### ConditionTypeEnum
Type: `string`


### ConfidenceLevelEnum
Type: `string`


### ContentEmbedding
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| embedding_number | string |  |
| step | integer |  |
| step_title | string |  |
| embedding_vector | [number] | 384-dimensional embedding vector from sentence-transformers |
| embedding_dimension | integer |  |
| model_name | string | Name of the embedding model used |
| text_content | string | Text used to generate embedding (title + description + objectives) |
| similar_content | object | Cached list of similar step_numbers with similarity scores |
| created_at | string |  |
| updated_at | string |  |


### ContentEmbeddingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| step | integer |  |
| embedding_vector | [number] | 384-dimensional embedding vector from sentence-transformers |
| model_name | string | Name of the embedding model used |
| text_content | string | Text used to generate embedding (title + description + objectives) |
| similar_content | object | Cached list of similar step_numbers with similarity scores |


### ContentTypeEnum
Type: `string`


### ConversationThread
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| messages_count | string |  |
| thread_number | string |  |
| tenant | string |  |
| student_email | string |  |
| student_name | string |  |
| subject | string |  |
| message_count | integer |  |
| first_message_date | string |  |
| last_message_date | string |  |
| is_active | boolean |  |
| is_resolved | boolean |  |
| resolved_at | string |  |
| primary_category | string |  |
| tags | any |  |
| created_at | string |  |
| updated_at | string |  |


### ConversationThreadRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_email | string |  |
| student_name | string |  |
| subject | string |  |
| message_count | integer |  |
| first_message_date | string |  |
| last_message_date | string |  |
| is_active | boolean |  |
| is_resolved | boolean |  |
| resolved_at | string |  |
| primary_category | string |  |
| tags | any |  |


### CreateEligibilityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| person_id | string |  |
| course_id | string |  |
| jurisdiction_code | string |  |
| input | any |  |
| metadata | any |  |


### CreateEligibilityRequestRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| person_id | string |  |
| course_id | string |  |
| jurisdiction_code | string |  |
| input | any |  |
| metadata | any |  |


### CriteriaTag
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tagged_length | string |  |
| tag_number | string |  |
| criterion_id | string | Reference to assessment criterion |
| criterion_name | string |  |
| criterion_description | string |  |
| tagged_text | string | Excerpt from submission linked to criterion |
| text_start_position | integer | Character position in original text |
| text_end_position | integer |  |
| context_before | string | Text before tagged excerpt |
| context_after | string | Text after tagged excerpt |
| tag_type | TagTypeEnum |  |
| confidence_level | ConfidenceLevelEnum |  |
| confidence_score | number | Automated confidence score (0-1) |
| notes | string | Assessor notes about this evidence |
| keywords | object | Extracted keywords from tagged text |
| is_validated | boolean |  |
| validated_by | string |  |
| validated_at | string |  |
| tagged_by | string |  |
| tagged_at | string |  |
| evidence | integer |  |


### CriteriaTagRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_id | string | Reference to assessment criterion |
| criterion_name | string |  |
| criterion_description | string |  |
| tagged_text | string | Excerpt from submission linked to criterion |
| text_start_position | integer | Character position in original text |
| text_end_position | integer |  |
| context_before | string | Text before tagged excerpt |
| context_after | string | Text after tagged excerpt |
| tag_type | TagTypeEnum |  |
| confidence_level | ConfidenceLevelEnum |  |
| confidence_score | number | Automated confidence score (0-1) |
| notes | string | Assessor notes about this evidence |
| keywords | object | Extracted keywords from tagged text |
| is_validated | boolean |  |
| validated_by | string |  |
| validated_at | string |  |
| tagged_by | string |  |
| evidence | integer |  |


### CriterionScore
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| criterion | object |  |
| similarity_score | number |  |
| points_awarded | number |  |
| matched_content | string |  |
| missing_elements | any |  |
| created_at | string |  |


### CriterionScoreRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_id | integer |  |
| similarity_score | number |  |
| points_awarded | number |  |
| matched_content | string |  |
| missing_elements | any |  |


### CurrencyEvidence
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| evidence_number | string |  |
| evidence_type | CurrencyEvidenceEvidenceTypeEnum |  |
| title | string |  |
| content | string |  |
| evidence_start_date | string |  |
| evidence_end_date | string |  |
| total_activities | integer |  |
| relevant_activities | integer |  |
| currency_score | number |  |
| linkedin_activities_included | any |  |
| github_activities_included | any |  |
| file_format | FileFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| meets_rto_standards | boolean |  |
| compliance_notes | string |  |
| is_approved | boolean |  |
| approved_by | string |  |
| approved_at | string |  |
| created_at | string |  |
| trainer_profile | integer |  |
| verification_scan | integer |  |


### CurrencyEvidenceEvidenceTypeEnum
Type: `string`


### CurrencyEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| evidence_type | CurrencyEvidenceEvidenceTypeEnum |  |
| title | string |  |
| content | string |  |
| evidence_start_date | string |  |
| evidence_end_date | string |  |
| total_activities | integer |  |
| relevant_activities | integer |  |
| currency_score | number |  |
| linkedin_activities_included | any |  |
| github_activities_included | any |  |
| file_format | FileFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| meets_rto_standards | boolean |  |
| compliance_notes | string |  |
| is_approved | boolean |  |
| approved_by | string |  |
| approved_at | string |  |
| trainer_profile | integer |  |
| verification_scan | integer |  |


### CurrencyStatusEnum
Type: `string`


### DailySummary
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| summary_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| summary_date | string |  |
| total_sessions | integer |  |
| total_teaching_hours | number |  |
| total_students | integer |  |
| courses_taught | any |  |
| daily_highlights | string |  |
| overall_student_engagement | string |  |
| key_achievements | any |  |
| challenges_summary | string |  |
| action_items_pending | any |  |
| diary_entries_included | any |  |
| evidence_documents_created | integer |  |
| generated_by_model | string |  |
| generation_date | string |  |


### DailySummaryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| summary_date | string |  |
| total_sessions | integer |  |
| total_teaching_hours | number |  |
| total_students | integer |  |
| courses_taught | any |  |
| daily_highlights | string |  |
| overall_student_engagement | string |  |
| key_achievements | any |  |
| challenges_summary | string |  |
| action_items_pending | any |  |
| diary_entries_included | any |  |
| evidence_documents_created | integer |  |
| generated_by_model | string |  |


### DecidedByEnum
Type: `string`


### DecisionOverride
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| decision | integer |  |
| reason_code | string |  |
| justification | string | Detailed justification for override |
| final_outcome | FinalOutcomeEnum |  |
| approver | integer |  |
| approver_details | object |  |
| approved_at | string |  |
| policy_version | string | Override policy version applied |
| evidence_refs | any |  |


### DecisionOverrideRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| decision | integer |  |
| reason_code | string |  |
| justification | string | Detailed justification for override |
| final_outcome | FinalOutcomeEnum |  |
| policy_version | string | Override policy version applied |
| evidence_refs | any |  |


### DiaryEntry
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| recordings | [AudioRecording] |  |
| entry_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| session_date | string |  |
| session_time_start | string |  |
| session_time_end | string |  |
| session_duration_minutes | integer |  |
| course_name | string |  |
| course_code | string |  |
| unit_of_competency | string |  |
| student_count | integer |  |
| delivery_mode | DiaryEntryDeliveryModeEnum |  |
| raw_transcript | string |  |
| manual_notes | string |  |
| session_summary | string |  |
| key_topics_covered | any |  |
| student_engagement_notes | string |  |
| challenges_encountered | string |  |
| follow_up_actions | any |  |
| learning_outcomes_addressed | any |  |
| assessment_activities | string |  |
| resources_used | any |  |
| evidence_attachments | any |  |
| transcription_model | string |  |
| summarization_model | string |  |
| transcription_duration_seconds | number |  |
| summarization_tokens | integer |  |
| entry_status | EntryStatusEnum |  |
| is_pinned | boolean |  |
| is_shared | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### DiaryEntryDeliveryModeEnum
Type: `string`


### DiaryEntryList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| entry_number | string |  |
| trainer_name | string |  |
| session_date | string |  |
| course_name | string |  |
| session_duration_minutes | integer |  |
| student_count | integer |  |
| entry_status | EntryStatusEnum |  |
| recordings_count | string |  |
| created_at | string |  |


### DiaryEntryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| session_date | string |  |
| session_time_start | string |  |
| session_time_end | string |  |
| session_duration_minutes | integer |  |
| course_name | string |  |
| course_code | string |  |
| unit_of_competency | string |  |
| student_count | integer |  |
| delivery_mode | DiaryEntryDeliveryModeEnum |  |
| raw_transcript | string |  |
| manual_notes | string |  |
| session_summary | string |  |
| key_topics_covered | any |  |
| student_engagement_notes | string |  |
| challenges_encountered | string |  |
| follow_up_actions | any |  |
| learning_outcomes_addressed | any |  |
| assessment_activities | string |  |
| resources_used | any |  |
| evidence_attachments | any |  |
| transcription_model | string |  |
| summarization_model | string |  |
| transcription_duration_seconds | number |  |
| summarization_tokens | integer |  |
| entry_status | EntryStatusEnum |  |
| is_pinned | boolean |  |
| is_shared | boolean |  |


### DifficultyAdjustmentEnum
Type: `string`


### DifficultyLevelEnum
Type: `string`


### DiscussionSentiment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| sentiment_number | string |  |
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| timestamp | string |  |
| message_type | DiscussionSentimentMessageTypeEnum |  |
| message_content | string |  |
| sentiment_score | string | Sentiment polarity: -1 (very negative) to +1 (very positive) |
| sentiment_label | object |  |
| confidence | string | Confidence in sentiment classification (0-1) |
| primary_emotion | object |  |
| emotion_scores | object | Emotion probabilities: {joy: 0.2, frustration: 0.6, ...} |
| word_count | integer |  |
| question_count | integer |  |
| exclamation_count | integer |  |
| negative_keywords | [string] | Detected negative or concerning keywords |
| help_seeking_keywords | [string] | Keywords indicating student needs help |
| discussion_topic | string |  |
| reply_count | integer |  |
| created_at | string |  |


### DiscussionSentimentMessageTypeEnum
Type: `string`


### DiscussionSentimentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| timestamp | string |  |
| message_type | DiscussionSentimentMessageTypeEnum |  |
| message_content | string |  |
| sentiment_score | string | Sentiment polarity: -1 (very negative) to +1 (very positive) |
| confidence | string | Confidence in sentiment classification (0-1) |
| primary_emotion | object |  |
| emotion_scores | object | Emotion probabilities: {joy: 0.2, frustration: 0.6, ...} |
| word_count | integer |  |
| question_count | integer |  |
| exclamation_count | integer |  |
| negative_keywords | [string] | Detected negative or concerning keywords |
| help_seeking_keywords | [string] | Keywords indicating student needs help |
| discussion_topic | string |  |
| reply_count | integer |  |


### DocumentFormatEnum
Type: `string`


### DraftReply
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| student_message_details | object |  |
| draft_number | string |  |
| reply_body | string |  |
| reply_subject | string |  |
| tone_used | string |  |
| formality_level | integer |  |
| include_greeting | boolean |  |
| include_signature | boolean |  |
| confidence_score | number |  |
| readability_score | number |  |
| word_count | integer |  |
| estimated_reading_time_seconds | integer |  |
| was_edited | boolean |  |
| was_sent | boolean |  |
| was_rejected | boolean |  |
| rejection_reason | string |  |
| generation_status | GenerationStatusEnum |  |
| generation_time_ms | integer |  |
| llm_model_used | string |  |
| generation_prompt | string |  |
| generated_at | string |  |
| sent_at | string |  |
| student_message | integer |  |
| template_used | integer |  |


### DraftReplyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| reply_body | string |  |
| reply_subject | string |  |
| tone_used | string |  |
| formality_level | integer |  |
| include_greeting | boolean |  |
| include_signature | boolean |  |
| confidence_score | number |  |
| readability_score | number |  |
| word_count | integer |  |
| estimated_reading_time_seconds | integer |  |
| was_edited | boolean |  |
| was_sent | boolean |  |
| was_rejected | boolean |  |
| rejection_reason | string |  |
| generation_status | GenerationStatusEnum |  |
| generation_time_ms | integer |  |
| llm_model_used | string |  |
| generation_prompt | string |  |
| sent_at | string |  |
| student_message | integer |  |
| template_used | integer |  |


### EligibilityCheck
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| check_number | string |  |
| student_first_name | string |  |
| student_last_name | string |  |
| student_dob | string | Date of birth |
| student_email | string |  |
| student_phone | string |  |
| course_code | string |  |
| course_name | string |  |
| aqf_level | integer | AQF level of course (1-10) |
| intended_start_date | string |  |
| jurisdiction | JurisdictionEnum |  |
| jurisdiction_display | string |  |
| jurisdiction_requirement | integer |  |
| jurisdiction_requirement_name | string |  |
| funding_program_code | string |  |
| student_data | object | Student eligibility information including citizenship, residency, employment, etc. |
| status | StatusE22Enum |  |
| status_display | string |  |
| is_eligible | boolean |  |
| eligibility_percentage | string | Percentage of rules passed |
| rules_checked | integer |  |
| rules_passed | integer |  |
| rules_failed | integer |  |
| check_results | object | Detailed results of each rule evaluation |
| failed_rules | object | List of failed rule details |
| warnings | object | Non-critical warnings |
| api_verified | boolean |  |
| api_response | object | Response from external API verification |
| api_verified_at | string |  |
| override_required | boolean |  |
| override_approved | boolean |  |
| override_reason | string |  |
| override_approved_by_name | string |  |
| override_approved_at | string |  |
| prevents_enrollment | boolean | If ineligible, prevent enrollment |
| compliance_notes | string |  |
| valid_from | string |  |
| valid_until | string | Eligibility expiry date |
| student_age | string |  |
| is_currently_valid | boolean |  |
| eligibility_summary | string |  |
| checked_at | string |  |
| checked_by_name | string |  |
| updated_at | string |  |


### EligibilityCheckDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| check_number | string |  |
| student_first_name | string |  |
| student_last_name | string |  |
| student_dob | string | Date of birth |
| student_email | string |  |
| student_phone | string |  |
| course_code | string |  |
| course_name | string |  |
| aqf_level | integer | AQF level of course (1-10) |
| intended_start_date | string |  |
| jurisdiction | JurisdictionEnum |  |
| jurisdiction_display | string |  |
| jurisdiction_requirement | integer |  |
| jurisdiction_requirement_name | string |  |
| funding_program_code | string |  |
| student_data | object | Student eligibility information including citizenship, residency, employment, etc. |
| status | StatusE22Enum |  |
| status_display | string |  |
| is_eligible | boolean |  |
| eligibility_percentage | string | Percentage of rules passed |
| rules_checked | integer |  |
| rules_passed | integer |  |
| rules_failed | integer |  |
| check_results | object | Detailed results of each rule evaluation |
| failed_rules | object | List of failed rule details |
| warnings | object | Non-critical warnings |
| api_verified | boolean |  |
| api_response | object | Response from external API verification |
| api_verified_at | string |  |
| override_required | boolean |  |
| override_approved | boolean |  |
| override_reason | string |  |
| override_approved_by_name | string |  |
| override_approved_at | string |  |
| prevents_enrollment | boolean | If ineligible, prevent enrollment |
| compliance_notes | string |  |
| valid_from | string |  |
| valid_until | string | Eligibility expiry date |
| student_age | string |  |
| is_currently_valid | boolean |  |
| eligibility_summary | string |  |
| checked_at | string |  |
| checked_by_name | string |  |
| updated_at | string |  |
| logs | [EligibilityCheckLog] |  |


### EligibilityCheckLog
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action | EligibilityCheckLogActionEnum |  |
| action_display | string |  |
| details | any |  |
| notes | string |  |
| performed_by_name | string |  |
| performed_at | string |  |


### EligibilityCheckLogActionEnum
Type: `string`


### EligibilityCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_first_name | string |  |
| student_last_name | string |  |
| student_dob | string | Date of birth |
| student_email | string |  |
| student_phone | string |  |
| course_code | string |  |
| course_name | string |  |
| aqf_level | integer | AQF level of course (1-10) |
| intended_start_date | string |  |
| jurisdiction | JurisdictionEnum |  |
| jurisdiction_requirement | integer |  |
| funding_program_code | string |  |
| student_data | object | Student eligibility information including citizenship, residency, employment, etc. |
| status | StatusE22Enum |  |
| is_eligible | boolean |  |
| eligibility_percentage | string | Percentage of rules passed |
| rules_checked | integer |  |
| rules_passed | integer |  |
| rules_failed | integer |  |
| check_results | object | Detailed results of each rule evaluation |
| failed_rules | object | List of failed rule details |
| warnings | object | Non-critical warnings |
| api_verified | boolean |  |
| api_response | object | Response from external API verification |
| api_verified_at | string |  |
| override_required | boolean |  |
| override_approved | boolean |  |
| override_reason | string |  |
| override_approved_at | string |  |
| prevents_enrollment | boolean | If ineligible, prevent enrollment |
| compliance_notes | string |  |
| valid_until | string | Eligibility expiry date |


### EligibilityDecision
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| request | integer |  |
| ruleset | integer |  |
| ruleset_details | object |  |
| outcome | OutcomeEb8Enum |  |
| reasons | object | Reason codes for the decision |
| clause_refs | object | Relevant clause/policy references |
| decision_data | object | Complete decision output from rules engine |
| explanation | string |  |
| decided_by | object |  |
| decided_by_user | integer |  |
| decided_by_user_details | object |  |
| decided_at | string |  |
| overrides | [DecisionOverride] |  |


### EligibilityDecisionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| request | integer |  |
| ruleset | integer |  |
| outcome | OutcomeEb8Enum |  |
| reasons | object | Reason codes for the decision |
| clause_refs | object | Relevant clause/policy references |
| decision_data | object | Complete decision output from rules engine |
| explanation | string |  |


### EligibilityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| person_id | string | Person identifier in SMS/LMS |
| course_id | string | Course identifier |
| jurisdiction_code | string |  |
| input | object | Complete input data for evaluation |
| evidence_refs | object | References to attached evidence documents |
| status | object |  |
| requested_at | string |  |
| evaluated_at | string |  |
| requested_by | integer |  |
| requested_by_details | object |  |
| metadata | object | Additional metadata |
| external_lookups | [ExternalLookup] |  |
| decision | object |  |
| attachments | [EvidenceAttachment] |  |


### EligibilityRequestList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| person_id | string | Person identifier in SMS/LMS |
| course_id | string | Course identifier |
| jurisdiction_code | string |  |
| status | object |  |
| outcome | string |  |
| requested_at | string |  |
| evaluated_at | string |  |
| requested_by_details | object |  |


### EligibilityRequestRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| person_id | string | Person identifier in SMS/LMS |
| course_id | string | Course identifier |
| jurisdiction_code | string |  |
| input | object | Complete input data for evaluation |
| evidence_refs | object | References to attached evidence documents |
| metadata | object | Additional metadata |


### EligibilityRule
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| jurisdiction_requirement | integer | Link to specific jurisdiction requirement (optional) |
| jurisdiction_name | string |  |
| rule_type | RuleTypeEnum |  |
| rule_type_display | string |  |
| name | string |  |
| description | string |  |
| field_name | string | Field to evaluate (e.g., 'age', 'citizenship_status', 'income') |
| operator | OperatorEnum |  |
| operator_display | string |  |
| expected_value | string | Expected value or comma-separated list for comparison |
| is_mandatory | boolean | Must pass for eligibility (vs. optional/bonus points) |
| priority | integer | Evaluation priority (1=highest) |
| error_message | string | Message shown when rule fails |
| override_allowed | boolean | Can be manually overridden by authorized staff |
| is_active | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### EligibilityRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| jurisdiction_requirement | integer | Link to specific jurisdiction requirement (optional) |
| rule_type | RuleTypeEnum |  |
| name | string |  |
| description | string |  |
| field_name | string | Field to evaluate (e.g., 'age', 'citizenship_status', 'income') |
| operator | OperatorEnum |  |
| expected_value | string | Expected value or comma-separated list for comparison |
| is_mandatory | boolean | Must pass for eligibility (vs. optional/bonus points) |
| priority | integer | Evaluation priority (1=highest) |
| error_message | string | Message shown when rule fails |
| override_allowed | boolean | Can be manually overridden by authorized staff |
| is_active | boolean |  |


### EmbeddingSearch
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| search_number | string |  |
| search_type | SearchTypeEnum |  |
| query_text | string |  |
| query_embedding | object | Vector embedding of query |
| filter_criteria | object | Additional filters (student, date range, etc.) |
| results_count | integer |  |
| top_results | object | Top matching results with scores |
| search_time_ms | integer | Search execution time |
| performed_by | string |  |
| timestamp | string |  |
| mapping | integer |  |


### EngagementAlert
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| alert_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| alert_type | AlertTypeEnum |  |
| severity | SeverityE88Enum |  |
| title | string |  |
| description | string |  |
| trigger_metrics | object | Metrics that triggered this alert: {attendance_score: 45, days_absent: 5} |
| recommended_actions | [string] | Suggested interventions |
| status | EngagementAlertStatusEnum |  |
| acknowledged_by | string |  |
| acknowledged_at | string |  |
| resolved_at | string |  |
| resolution_notes | string |  |
| created_at | string |  |
| updated_at | string |  |


### EngagementAlertRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| alert_type | AlertTypeEnum |  |
| severity | SeverityE88Enum |  |
| title | string |  |
| description | string |  |
| trigger_metrics | object | Metrics that triggered this alert: {attendance_score: 45, days_absent: 5} |
| recommended_actions | [string] | Suggested interventions |
| status | EngagementAlertStatusEnum |  |
| acknowledged_by | string |  |
| acknowledged_at | string |  |
| resolved_at | string |  |
| resolution_notes | string |  |


### EngagementAlertStatusEnum
Type: `string`


### EngagementHeatmap
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| heatmap_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| time_period | object |  |
| start_date | string |  |
| end_date | string |  |
| overall_engagement_score | string | Weighted composite: 40% attendance + 35% LMS + 25% sentiment |
| attendance_score | string |  |
| lms_activity_score | string |  |
| sentiment_score | string | Normalized sentiment (0=very negative, 100=very positive) |
| risk_level | object |  |
| risk_flags | [string] | Specific risk indicators: low_attendance, inactive_lms, negative_sentiment, etc. |
| heatmap_data | object | Daily engagement data: {date: {attendance: bool, lms_minutes: int, sentiment: float}} |
| engagement_trend | EngagementTrendEnum |  |
| change_percentage | string | Percentage change from previous period |
| alerts_triggered | integer |  |
| interventions_applied | integer |  |
| created_at | string |  |
| updated_at | string |  |
| attendance_records | [AttendanceRecord] |  |
| lms_activities | [LMSActivity] |  |
| discussion_sentiments | [DiscussionSentiment] |  |
| engagement_alerts | [EngagementAlert] |  |


### EngagementHeatmapRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| time_period | object |  |
| start_date | string |  |
| end_date | string |  |
| attendance_score | string |  |
| lms_activity_score | string |  |
| sentiment_score | string | Normalized sentiment (0=very negative, 100=very positive) |
| risk_flags | [string] | Specific risk indicators: low_attendance, inactive_lms, negative_sentiment, etc. |
| heatmap_data | object | Daily engagement data: {date: {attendance: bool, lms_minutes: int, sentiment: float}} |
| engagement_trend | EngagementTrendEnum |  |
| change_percentage | string | Percentage change from previous period |
| alerts_triggered | integer |  |
| interventions_applied | integer |  |


### EngagementHeatmapRiskLevelEnum
Type: `string`


### EngagementLevelEnum
Type: `string`


### EngagementTrendEnum
Type: `string`


### EntityExtraction
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| extraction_number | string |  |
| source_type | EntityExtractionSourceTypeEnum |  |
| source_url | string |  |
| source_text | string |  |
| entities | any |  |
| extraction_confidence | number |  |
| entity_count | integer |  |
| nlp_model_used | string |  |
| processing_time_ms | number |  |
| extracted_at | string |  |
| verification_scan | integer |  |


### EntityExtractionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| source_type | EntityExtractionSourceTypeEnum |  |
| source_url | string |  |
| source_text | string |  |
| entities | any |  |
| extraction_confidence | number |  |
| entity_count | integer |  |
| nlp_model_used | string |  |
| processing_time_ms | number |  |
| verification_scan | integer |  |


### EntityExtractionSourceTypeEnum
Type: `string`


### EntryStatusEnum
Type: `string`


### Evidence
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| evidence_number | string |  |
| title | string |  |
| description | string |  |
| evidence_type | EvidenceEvidenceTypeEnum |  |
| file | string | Supported formats: PDF, Word, Excel, Text, Images |
| file_url | string |  |
| file_name | string |  |
| file_size | integer | File size in bytes |
| extracted_text | string | Text extracted from uploaded file |
| ner_entities | object | Named entities extracted: {entity: str, type: str, start: int, end: int} |
| ner_processed_at | string |  |
| status | EvidenceStatusEnum |  |
| tags | object | Custom tags for categorization |
| evidence_date | string | Date the evidence was created/issued |
| uploaded_at | string |  |
| uploaded_by | integer |  |
| uploaded_by_name | string |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| reviewer_notes | string |  |
| tagged_clauses_count | string |  |
| auto_tagged_count | string |  |


### EvidenceAttachment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| request | integer |  |
| file_uri | string | S3/storage URI |
| filename | string |  |
| file_size | integer | Size in bytes |
| mime_type | string |  |
| type | EvidenceAttachmentTypeEnum |  |
| verified | boolean |  |
| verifier | integer |  |
| verifier_details | object |  |
| verified_at | string |  |
| verification_notes | string |  |
| uploaded_by | integer |  |
| uploaded_by_details | object |  |
| uploaded_at | string |  |


### EvidenceAttachmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| request | integer |  |
| filename | string |  |
| mime_type | string |  |
| type | EvidenceAttachmentTypeEnum |  |
| verified | boolean |  |
| verifier | integer |  |
| verified_at | string |  |
| verification_notes | string |  |


### EvidenceAttachmentTypeEnum
Type: `string`


### EvidenceAudit
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action | EvidenceAuditActionEnum |  |
| description | string |  |
| submission_id | string |  |
| criterion_id | string |  |
| tag_id | integer |  |
| action_data | object | Detailed data about the action performed |
| changes_made | object | Before/after values for modifications |
| processing_time_ms | integer |  |
| performed_by | string |  |
| user_role | string |  |
| ip_address | string |  |
| user_agent | string |  |
| timestamp | string |  |
| mapping | integer |  |


### EvidenceAuditActionEnum
Type: `string`


### EvidenceDocument
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| document_number | string |  |
| document_type | EvidenceDocumentDocumentTypeEnum |  |
| document_title | string |  |
| document_content | string |  |
| document_format | DocumentFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| generated_by | string |  |
| generation_method | GenerationMethodEnum |  |
| meets_compliance_standards | boolean |  |
| compliance_notes | string |  |
| created_at | string |  |
| diary_entry | integer |  |


### EvidenceDocumentDocumentTypeEnum
Type: `string`


### EvidenceDocumentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| document_type | EvidenceDocumentDocumentTypeEnum |  |
| document_title | string |  |
| document_content | string |  |
| document_format | DocumentFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| generated_by | string |  |
| generation_method | GenerationMethodEnum |  |
| meets_compliance_standards | boolean |  |
| compliance_notes | string |  |
| diary_entry | integer |  |


### EvidenceEvidenceTypeEnum
Type: `string`


### EvidenceMapping
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| coverage_percentage_calculated | string |  |
| mapping_number | string |  |
| name | string |  |
| description | string |  |
| assessment_type | EvidenceMappingAssessmentTypeEnum |  |
| assessment_title | string |  |
| unit_code | string |  |
| total_criteria | integer |  |
| total_submissions | integer |  |
| auto_extract_text | boolean | Automatically extract text from submissions |
| generate_embeddings | boolean | Generate embeddings for semantic search |
| require_evidence_per_criterion | boolean |  |
| min_evidence_length | integer | Minimum characters for valid evidence |
| total_evidence_tagged | integer |  |
| total_text_extracted | integer |  |
| embeddings_generated | integer |  |
| coverage_percentage | number |  |
| status | EvidenceMappingStatusEnum |  |
| created_at | string |  |
| updated_at | string |  |
| created_by | string |  |


### EvidenceMappingAssessmentTypeEnum
Type: `string`


### EvidenceMappingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| assessment_type | EvidenceMappingAssessmentTypeEnum |  |
| assessment_title | string |  |
| unit_code | string |  |
| total_criteria | integer |  |
| total_submissions | integer |  |
| auto_extract_text | boolean | Automatically extract text from submissions |
| generate_embeddings | boolean | Generate embeddings for semantic search |
| require_evidence_per_criterion | boolean |  |
| min_evidence_length | integer | Minimum characters for valid evidence |
| status | EvidenceMappingStatusEnum |  |
| created_by | string |  |


### EvidenceMappingStatusEnum
Type: `string`


### EvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| evidence_number | string |  |
| title | string |  |
| description | string |  |
| evidence_type | EvidenceEvidenceTypeEnum |  |
| file | string | Supported formats: PDF, Word, Excel, Text, Images |
| ner_entities | object | Named entities extracted: {entity: str, type: str, start: int, end: int} |
| status | EvidenceStatusEnum |  |
| tags | object | Custom tags for categorization |
| evidence_date | string | Date the evidence was created/issued |
| uploaded_by | integer |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |
| reviewer_notes | string |  |


### EvidenceStatusEnum
Type: `string`


### EvidenceType1d4Enum
Type: `string`


### ExternalLookup
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| request | integer |  |
| provider | string | API provider (USI, visa, etc.) |
| request_data | any |  |
| response_data | object |  |
| status | object |  |
| error_message | string |  |
| latency_ms | integer |  |
| cached_until | string |  |
| created_at | string |  |


### ExternalLookupRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| request | integer |  |
| provider | string | API provider (USI, visa, etc.) |
| request_data | any |  |


### ExternalLookupStatusEnum
Type: `string`


### ExtractionStatusEnum
Type: `string`


### FactorTypeEnum
Type: `string`


### FeedbackCriterion
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| criterion_name | string |  |
| description | string |  |
| rubric_criterion | integer |  |
| rubric_criterion_name | string |  |
| excellent_feedback | string | Feedback for excellent performance |
| good_feedback | string | Feedback for good performance |
| satisfactory_feedback | string | Feedback for satisfactory performance |
| needs_improvement_feedback | string | Feedback for needs improvement |
| weight | number | Importance of this criterion |
| display_order | integer |  |
| created_at | string |  |
| updated_at | string |  |


### FeedbackCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_name | string |  |
| description | string |  |
| rubric_criterion | integer |  |
| excellent_feedback | string | Feedback for excellent performance |
| good_feedback | string | Feedback for good performance |
| satisfactory_feedback | string | Feedback for satisfactory performance |
| needs_improvement_feedback | string | Feedback for needs improvement |
| weight | number | Importance of this criterion |
| display_order | integer |  |


### FeedbackLog
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| template | integer |  |
| template_name | string |  |
| feedback | integer |  |
| action | FeedbackLogActionEnum |  |
| performed_by | integer |  |
| performed_by_name | string |  |
| feedbacks_generated | integer |  |
| total_time | number | Total processing time in seconds |
| average_time_per_feedback | number |  |
| average_sentiment | number |  |
| average_personalization | number |  |
| changes_made | string |  |
| previous_version | string |  |
| details | any |  |
| timestamp | string |  |


### FeedbackLogActionEnum
Type: `string`


### FeedbackTemplateDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| template_number | string |  |
| name | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| feedback_type | FeedbackTypeEnum |  |
| sentiment | Sentiment9ddEnum |  |
| tone | ToneEnum |  |
| rubric | integer |  |
| rubric_name | string |  |
| maps_to_criteria | object | List of rubric criterion IDs |
| include_student_name | boolean |  |
| include_strengths | boolean |  |
| include_improvements | boolean |  |
| include_next_steps | boolean |  |
| include_encouragement | boolean |  |
| opening_template | string | Opening statement template |
| strengths_template | string |  |
| improvements_template | string |  |
| next_steps_template | string |  |
| closing_template | string |  |
| positivity_level | integer | 1=Very Critical, 10=Very Positive |
| directness_level | integer | 1=Very Indirect, 10=Very Direct |
| formality_level | integer | 1=Very Casual, 10=Very Formal |
| sentiment_description | string |  |
| total_feedback_generated | integer |  |
| average_generation_time | number | Average time in seconds |
| status | Status118Enum |  |
| criteria | [FeedbackCriterion] |  |
| created_at | string |  |
| updated_at | string |  |


### FeedbackTemplateDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| feedback_type | FeedbackTypeEnum |  |
| sentiment | Sentiment9ddEnum |  |
| tone | ToneEnum |  |
| rubric | integer |  |
| maps_to_criteria | object | List of rubric criterion IDs |
| include_student_name | boolean |  |
| include_strengths | boolean |  |
| include_improvements | boolean |  |
| include_next_steps | boolean |  |
| include_encouragement | boolean |  |
| opening_template | string | Opening statement template |
| strengths_template | string |  |
| improvements_template | string |  |
| next_steps_template | string |  |
| closing_template | string |  |
| positivity_level | integer | 1=Very Critical, 10=Very Positive |
| directness_level | integer | 1=Very Indirect, 10=Very Direct |
| formality_level | integer | 1=Very Casual, 10=Very Formal |
| status | Status118Enum |  |


### FeedbackTemplateList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| template_number | string |  |
| name | string |  |
| description | string |  |
| tenant | string |  |
| feedback_type | FeedbackTypeEnum |  |
| sentiment | Sentiment9ddEnum |  |
| tone | ToneEnum |  |
| rubric | integer |  |
| rubric_name | string |  |
| positivity_level | integer | 1=Very Critical, 10=Very Positive |
| directness_level | integer | 1=Very Indirect, 10=Very Direct |
| formality_level | integer | 1=Very Casual, 10=Very Formal |
| total_feedback_generated | integer |  |
| total_generated | string |  |
| status | Status118Enum |  |
| created_at | string |  |
| updated_at | string |  |


### FeedbackTemplateListRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| tenant | string |  |
| feedback_type | FeedbackTypeEnum |  |
| sentiment | Sentiment9ddEnum |  |
| tone | ToneEnum |  |
| rubric | integer |  |
| positivity_level | integer | 1=Very Critical, 10=Very Positive |
| directness_level | integer | 1=Very Indirect, 10=Very Direct |
| formality_level | integer | 1=Very Casual, 10=Very Formal |
| total_feedback_generated | integer |  |
| status | Status118Enum |  |


### FeedbackTypeEnum
Type: `string`


### FileFormatEnum
Type: `string`


### FinalOutcomeEnum
Type: `string`


### GapSeverityEnum
Type: `string`


### GapTypeEnum
Type: `string`


### GeneratedFeedbackDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| feedback_number | string |  |
| template | object |  |
| student_id | string |  |
| student_name | string |  |
| assessment_title | string |  |
| score | number |  |
| max_score | number |  |
| percentage_score | string |  |
| grade | string |  |
| rubric_scores | object | Scores per rubric criterion |
| feedback_text | string |  |
| strengths_identified | any |  |
| improvements_identified | any |  |
| next_steps_suggested | any |  |
| sentiment_score | number | Sentiment: -1 (negative) to +1 (positive) |
| tone_consistency | number | How well tone matches template settings |
| word_count | integer |  |
| reading_level | string | e.g., Grade 10, University |
| personalization_score | number | How personalized the feedback is |
| requires_review | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| delivered_at | string |  |
| delivery_method | string | email, LMS, portal, etc. |
| status | Status5d3Enum |  |
| generation_time | number | Time to generate in seconds |
| generated_at | string |  |
| updated_at | string |  |


### GeneratedFeedbackDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| assessment_title | string |  |
| score | number |  |
| max_score | number |  |
| grade | string |  |
| rubric_scores | object | Scores per rubric criterion |
| feedback_text | string |  |
| strengths_identified | any |  |
| improvements_identified | any |  |
| next_steps_suggested | any |  |
| reading_level | string | e.g., Grade 10, University |
| requires_review | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |
| delivered_at | string |  |
| delivery_method | string | email, LMS, portal, etc. |
| status | Status5d3Enum |  |


### GeneratedFeedbackList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| feedback_number | string |  |
| template | integer |  |
| template_name | string |  |
| student_id | string |  |
| student_name | string |  |
| assessment_title | string |  |
| score | number |  |
| max_score | number |  |
| percentage_score | string |  |
| grade | string |  |
| word_count | integer |  |
| sentiment_score | number | Sentiment: -1 (negative) to +1 (positive) |
| personalization_score | number | How personalized the feedback is |
| requires_review | boolean |  |
| status | Status5d3Enum |  |
| generated_at | string |  |


### GenerationMethodEnum
Type: `string`


### GenerationStatusEnum
Type: `string`


### GitHubActivity
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| activity_number | string |  |
| activity_type | GitHubActivityActivityTypeEnum |  |
| repository_name | string |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| last_updated | string |  |
| language | string |  |
| languages_used | any |  |
| topics | any |  |
| stars | integer |  |
| forks | integer |  |
| technologies | any |  |
| frameworks | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| commits_count | integer |  |
| contributions_count | integer |  |
| raw_data | any |  |
| extracted_at | string |  |
| verification_scan | integer |  |


### GitHubActivityActivityTypeEnum
Type: `string`


### GitHubActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| activity_type | GitHubActivityActivityTypeEnum |  |
| repository_name | string |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| last_updated | string |  |
| language | string |  |
| languages_used | any |  |
| topics | any |  |
| stars | integer |  |
| forks | integer |  |
| technologies | any |  |
| frameworks | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| commits_count | integer |  |
| contributions_count | integer |  |
| raw_data | any |  |
| verification_scan | integer |  |


### GradeEnum
Type: `string`


### ImpactRatingEnum
Type: `string`


### ImprovementAction
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action_number | string |  |
| title | string |  |
| description | string | Detailed description of the improvement action |
| category | integer |  |
| category_name | string |  |
| priority | PriorityE88Enum |  |
| priority_display | string |  |
| source | SourceA98Enum |  |
| source_display | string |  |
| status | Status354Enum |  |
| status_display | string |  |
| ai_classified_category | string | AI-suggested category based on content analysis |
| ai_classification_confidence | number | Confidence score (0.0-1.0) for AI classification |
| ai_summary | string | AI-generated summary of the action |
| ai_keywords | object | AI-extracted keywords from description |
| ai_related_standards | object | AI-identified ASQA standards related to this action |
| ai_processed_at | string |  |
| identified_date | string |  |
| planned_start_date | string |  |
| target_completion_date | string |  |
| actual_completion_date | string |  |
| responsible_person | integer |  |
| responsible_person_name | string |  |
| root_cause | string | Root cause analysis |
| proposed_solution | string |  |
| resources_required | string |  |
| estimated_cost | string |  |
| actual_cost | string |  |
| success_criteria | string | How to measure success |
| expected_impact | string |  |
| actual_impact | string | Post-implementation impact |
| effectiveness_rating | integer | Rating 1-5 after completion |
| compliance_status | object |  |
| compliance_status_display | string |  |
| is_critical_compliance | boolean | Critical for maintaining RTO registration |
| is_overdue | boolean |  |
| days_until_due | integer |  |
| progress_percentage | integer |  |
| requires_approval | boolean |  |
| approved_by | integer |  |
| approved_by_name | string |  |
| approved_at | string |  |
| tags | object | Custom tags for filtering |
| attachments | object | List of attachment URLs/metadata |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| updated_at | string |  |
| tracking_updates_count | string |  |


### ImprovementActionDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action_number | string |  |
| title | string |  |
| description | string | Detailed description of the improvement action |
| category | integer |  |
| category_name | string |  |
| priority | PriorityE88Enum |  |
| priority_display | string |  |
| source | SourceA98Enum |  |
| source_display | string |  |
| status | Status354Enum |  |
| status_display | string |  |
| ai_classified_category | string | AI-suggested category based on content analysis |
| ai_classification_confidence | number | Confidence score (0.0-1.0) for AI classification |
| ai_summary | string | AI-generated summary of the action |
| ai_keywords | object | AI-extracted keywords from description |
| ai_related_standards | object | AI-identified ASQA standards related to this action |
| ai_processed_at | string |  |
| identified_date | string |  |
| planned_start_date | string |  |
| target_completion_date | string |  |
| actual_completion_date | string |  |
| responsible_person | integer |  |
| responsible_person_name | string |  |
| root_cause | string | Root cause analysis |
| proposed_solution | string |  |
| resources_required | string |  |
| estimated_cost | string |  |
| actual_cost | string |  |
| success_criteria | string | How to measure success |
| expected_impact | string |  |
| actual_impact | string | Post-implementation impact |
| effectiveness_rating | integer | Rating 1-5 after completion |
| compliance_status | object |  |
| compliance_status_display | string |  |
| is_critical_compliance | boolean | Critical for maintaining RTO registration |
| is_overdue | boolean |  |
| days_until_due | integer |  |
| progress_percentage | integer |  |
| requires_approval | boolean |  |
| approved_by | integer |  |
| approved_by_name | string |  |
| approved_at | string |  |
| tags | object | Custom tags for filtering |
| attachments | object | List of attachment URLs/metadata |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| updated_at | string |  |
| tracking_updates_count | string |  |
| tracking_updates | [ActionTracking] |  |
| supporting_staff_details | string |  |


### ImprovementActionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| action_number | string |  |
| title | string |  |
| description | string | Detailed description of the improvement action |
| category | integer |  |
| priority | PriorityE88Enum |  |
| source | SourceA98Enum |  |
| status | Status354Enum |  |
| ai_classified_category | string | AI-suggested category based on content analysis |
| ai_classification_confidence | number | Confidence score (0.0-1.0) for AI classification |
| ai_summary | string | AI-generated summary of the action |
| ai_keywords | object | AI-extracted keywords from description |
| ai_related_standards | object | AI-identified ASQA standards related to this action |
| identified_date | string |  |
| planned_start_date | string |  |
| target_completion_date | string |  |
| actual_completion_date | string |  |
| responsible_person | integer |  |
| root_cause | string | Root cause analysis |
| proposed_solution | string |  |
| resources_required | string |  |
| estimated_cost | string |  |
| actual_cost | string |  |
| success_criteria | string | How to measure success |
| expected_impact | string |  |
| actual_impact | string | Post-implementation impact |
| effectiveness_rating | integer | Rating 1-5 after completion |
| is_critical_compliance | boolean | Critical for maintaining RTO registration |
| requires_approval | boolean |  |
| approved_by | integer |  |
| approved_at | string |  |
| tags | object | Custom tags for filtering |
| attachments | object | List of attachment URLs/metadata |
| created_by | integer |  |


### ImprovementCategory
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| name | string |  |
| category_type | CategoryTypeEnum |  |
| category_type_display | string |  |
| description | string |  |
| color_code | string | Hex color code for UI display |
| related_standards | object | List of ASQA standard numbers this category relates to |
| is_active | boolean |  |
| actions_count | string |  |
| created_at | string |  |


### ImprovementCategoryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| category_type | CategoryTypeEnum |  |
| description | string |  |
| color_code | string | Hex color code for UI display |
| related_standards | object | List of ASQA standard numbers this category relates to |
| is_active | boolean |  |


### ImprovementReview
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| review_number | string |  |
| title | string |  |
| review_type | ReviewTypeEnum |  |
| review_type_display | string |  |
| review_date | string |  |
| review_period_start | string |  |
| review_period_end | string |  |
| total_actions_reviewed | integer |  |
| actions_completed | integer |  |
| actions_on_track | integer |  |
| actions_at_risk | integer |  |
| actions_overdue | integer |  |
| ai_summary | string | AI-generated summary of review findings |
| ai_trends | object | AI-identified trends and patterns |
| ai_recommendations | object | AI-generated recommendations |
| key_findings | string |  |
| areas_of_concern | string |  |
| recommendations | string |  |
| action_items | object | New actions arising from review |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| approved_by | integer |  |
| approved_by_name | string |  |
| approved_at | string |  |
| notes | string |  |
| attachments | any |  |
| created_at | string |  |
| updated_at | string |  |


### ImprovementReviewRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| review_number | string |  |
| title | string |  |
| review_type | ReviewTypeEnum |  |
| review_date | string |  |
| review_period_start | string |  |
| review_period_end | string |  |
| ai_summary | string | AI-generated summary of review findings |
| ai_trends | object | AI-identified trends and patterns |
| ai_recommendations | object | AI-generated recommendations |
| key_findings | string |  |
| areas_of_concern | string |  |
| recommendations | string |  |
| action_items | object | New actions arising from review |
| reviewed_by | integer |  |
| approved_by | integer |  |
| approved_at | string |  |
| notes | string |  |
| attachments | any |  |


### IndustryCurrencyStatusEnum
Type: `string`


### Integration
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | string |  |
| tenant | string |  |
| integration_type | IntegrationTypeEnum |  |
| integration_type_display | string |  |
| name | string |  |
| description | string |  |
| status | IntegrationStatusEnum |  |
| status_display | string |  |
| config | object | Integration-specific configuration |
| client_id | string |  |
| api_base_url | string |  |
| api_key | string |  |
| webhook_url | string |  |
| webhook_secret | string |  |
| auto_sync_enabled | boolean |  |
| sync_interval_minutes | integer |  |
| last_sync_at | string |  |
| last_sync_status | string |  |
| last_sync_error | string |  |
| is_token_expired | boolean |  |
| needs_sync | boolean |  |
| created_at | string |  |
| updated_at | string |  |
| created_by | string |  |


### IntegrationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| integration_type | IntegrationTypeEnum |  |
| name | string |  |
| description | string |  |
| status | IntegrationStatusEnum |  |
| config | object | Integration-specific configuration |
| client_id | string |  |
| api_base_url | string |  |
| api_key | string |  |
| webhook_url | string |  |
| webhook_secret | string |  |
| auto_sync_enabled | boolean |  |
| sync_interval_minutes | integer |  |
| last_sync_status | string |  |
| last_sync_error | string |  |
| created_by | string |  |


### IntegrationStatusEnum
Type: `string`


### IntegrationTypeEnum
Type: `string`


### IntegrityStatusEnum
Type: `string`


### Intervention
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| workflow_steps | [InterventionStep] |  |
| outcomes | [InterventionOutcome] |  |
| audit_logs | [AuditLog] |  |
| intervention_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| course_id | string |  |
| course_name | string |  |
| intervention_type | InterventionTypeEnum |  |
| priority_level | PriorityLevelD67Enum |  |
| status | Status65aEnum |  |
| trigger_type | TriggerTypeEnum |  |
| trigger_rule_id | string |  |
| trigger_details | any |  |
| action_description | string |  |
| action_taken_by | string |  |
| action_taken_by_role | string |  |
| action_date | string |  |
| communication_method | object |  |
| communication_notes | string |  |
| outcome_achieved | OutcomeAchievedEnum |  |
| outcome_description | string |  |
| outcome_evidence | any |  |
| requires_followup | boolean |  |
| followup_date | string |  |
| followup_notes | string |  |
| referred_to | string |  |
| referral_accepted | boolean |  |
| referral_date | string |  |
| created_at | string |  |
| updated_at | string |  |
| completed_at | string |  |
| audit_notes | string |  |
| compliance_category | string |  |
| attachments | any |  |


### InterventionAction
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action_number | string |  |
| action_type | InterventionActionActionTypeEnum |  |
| description | string |  |
| priority | PriorityD67Enum |  |
| scheduled_date | string |  |
| completed_date | string |  |
| status | StatusF31Enum |  |
| assigned_to | integer |  |
| assigned_to_name | string |  |
| outcome_notes | string |  |
| effectiveness_rating | integer | Effectiveness rating (1-5) |
| created_by | integer |  |
| created_by_name | string |  |
| created_at | string |  |
| updated_at | string |  |


### InterventionActionActionTypeEnum
Type: `string`


### InterventionActionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| action_type | InterventionActionActionTypeEnum |  |
| description | string |  |
| priority | PriorityD67Enum |  |
| scheduled_date | string |  |
| completed_date | string |  |
| status | StatusF31Enum |  |
| assigned_to | integer |  |
| outcome_notes | string |  |
| effectiveness_rating | integer | Effectiveness rating (1-5) |
| created_by | integer |  |


### InterventionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| intervention_number | string |  |
| student_name | string |  |
| intervention_type | InterventionTypeEnum |  |
| priority_level | PriorityLevelD67Enum |  |
| status | Status65aEnum |  |
| action_taken_by | string |  |
| action_date | string |  |
| outcome_achieved | OutcomeAchievedEnum |  |
| requires_followup | boolean |  |
| created_at | string |  |


### InterventionOutcome
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| outcome_number | string |  |
| metric_type | MetricTypeEnum |  |
| baseline_value | number |  |
| target_value | number |  |
| actual_value | number |  |
| measurement_date | string |  |
| improvement_percentage | number |  |
| target_achieved | boolean |  |
| impact_rating | object |  |
| evidence_description | string |  |
| evidence_links | any |  |
| notes | string |  |
| created_at | string |  |
| intervention | integer |  |


### InterventionOutcomeRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| metric_type | MetricTypeEnum |  |
| baseline_value | number |  |
| target_value | number |  |
| actual_value | number |  |
| measurement_date | string |  |
| impact_rating | object |  |
| evidence_description | string |  |
| evidence_links | any |  |
| notes | string |  |
| intervention | integer |  |


### InterventionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| course_id | string |  |
| course_name | string |  |
| intervention_type | InterventionTypeEnum |  |
| priority_level | PriorityLevelD67Enum |  |
| status | Status65aEnum |  |
| trigger_type | TriggerTypeEnum |  |
| trigger_rule_id | string |  |
| trigger_details | any |  |
| action_description | string |  |
| action_taken_by | string |  |
| action_taken_by_role | string |  |
| action_date | string |  |
| communication_method | object |  |
| communication_notes | string |  |
| outcome_achieved | OutcomeAchievedEnum |  |
| outcome_description | string |  |
| outcome_evidence | any |  |
| requires_followup | boolean |  |
| followup_date | string |  |
| followup_notes | string |  |
| referred_to | string |  |
| referral_accepted | boolean |  |
| referral_date | string |  |
| completed_at | string |  |
| audit_notes | string |  |
| compliance_category | string |  |
| attachments | any |  |


### InterventionRule
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| rule_number | string |  |
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| is_active | boolean |  |
| priority | integer |  |
| condition_type | ConditionTypeEnum |  |
| conditions | any |  |
| intervention_type | string |  |
| priority_level | string |  |
| assigned_to_role | string |  |
| notify_staff | boolean |  |
| notification_recipients | any |  |
| notification_template | string |  |
| compliance_requirement | string |  |
| last_triggered | string |  |
| trigger_count | integer |  |
| created_at | string |  |
| updated_at | string |  |


### InterventionRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| is_active | boolean |  |
| priority | integer |  |
| condition_type | ConditionTypeEnum |  |
| conditions | any |  |
| intervention_type | string |  |
| priority_level | string |  |
| assigned_to_role | string |  |
| notify_staff | boolean |  |
| notification_recipients | any |  |
| notification_template | string |  |
| compliance_requirement | string |  |


### InterventionStep
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| step_number | integer |  |
| step_name | string |  |
| step_description | string |  |
| status | InterventionStepStatusEnum |  |
| completed_by | string |  |
| completed_at | string |  |
| completion_notes | string |  |
| duration_minutes | integer |  |
| evidence_provided | any |  |
| attachments | any |  |
| created_at | string |  |
| updated_at | string |  |
| intervention | integer |  |
| workflow | integer |  |


### InterventionStepRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| step_number | integer |  |
| step_name | string |  |
| step_description | string |  |
| status | InterventionStepStatusEnum |  |
| completed_by | string |  |
| completed_at | string |  |
| completion_notes | string |  |
| duration_minutes | integer |  |
| evidence_provided | any |  |
| attachments | any |  |
| intervention | integer |  |
| workflow | integer |  |


### InterventionStepStatusEnum
Type: `string`


### InterventionTypeEnum
Type: `string`


### InterventionWorkflow
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| workflow_number | string |  |
| tenant | string |  |
| workflow_name | string |  |
| description | string |  |
| intervention_types | any |  |
| is_active | boolean |  |
| steps | any |  |
| requires_approval | boolean |  |
| approval_roles | any |  |
| required_documentation | any |  |
| compliance_standard | string |  |
| audit_requirements | any |  |
| created_at | string |  |
| updated_at | string |  |


### InterventionWorkflowRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| workflow_name | string |  |
| description | string |  |
| intervention_types | any |  |
| is_active | boolean |  |
| steps | any |  |
| requires_approval | boolean |  |
| approval_roles | any |  |
| required_documentation | any |  |
| compliance_standard | string |  |
| audit_requirements | any |  |


### JobStatusEnum
Type: `string`


### Jurisdiction
Type: `object`

| Property | Type | Description |
|---|---|---|
| code | string |  |
| name | string |  |
| active | boolean |  |
| config | object | Jurisdiction-specific configuration |
| default_ruleset | integer |  |


### JurisdictionEnum
Type: `string`


### JurisdictionRequirement
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| jurisdiction | JurisdictionEnum |  |
| jurisdiction_display | string |  |
| name | string | Name of funding program (e.g., 'Smart and Skilled NSW') |
| code | string | Program code (e.g., 'SS-NSW', 'STS-VIC') |
| requires_australian_citizen | boolean |  |
| requires_permanent_resident | boolean |  |
| requires_jurisdiction_resident | boolean |  |
| min_jurisdiction_residency_months | integer | Minimum months of residency required |
| min_age | integer |  |
| max_age | integer |  |
| requires_year_12 | boolean |  |
| allows_year_10_completion | boolean |  |
| requires_unemployed | boolean |  |
| allows_employed | boolean |  |
| requires_apprentice_trainee | boolean |  |
| restricts_higher_qualifications | boolean | Student cannot have a higher qualification than what they're enrolling in |
| max_aqf_level | integer | Maximum AQF level student can already have |
| has_income_threshold | boolean |  |
| max_annual_income | string | Maximum annual income in AUD |
| allows_concession_card | boolean |  |
| allows_disability | boolean |  |
| allows_indigenous | boolean |  |
| priority_indigenous | boolean |  |
| funding_percentage | string | Percentage of course fees covered |
| student_contribution | string | Student contribution/co-payment amount in AUD |
| api_endpoint | string | External API endpoint for eligibility verification |
| api_key_required | boolean |  |
| additional_rules | object | Additional eligibility rules in JSON format |
| is_active | boolean |  |
| effective_from | string |  |
| effective_to | string |  |
| is_currently_effective | boolean |  |
| custom_rules_count | string |  |
| created_at | string |  |
| updated_at | string |  |


### JurisdictionRequirementRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| jurisdiction | JurisdictionEnum |  |
| name | string | Name of funding program (e.g., 'Smart and Skilled NSW') |
| code | string | Program code (e.g., 'SS-NSW', 'STS-VIC') |
| requires_australian_citizen | boolean |  |
| requires_permanent_resident | boolean |  |
| requires_jurisdiction_resident | boolean |  |
| min_jurisdiction_residency_months | integer | Minimum months of residency required |
| min_age | integer |  |
| max_age | integer |  |
| requires_year_12 | boolean |  |
| allows_year_10_completion | boolean |  |
| requires_unemployed | boolean |  |
| allows_employed | boolean |  |
| requires_apprentice_trainee | boolean |  |
| restricts_higher_qualifications | boolean | Student cannot have a higher qualification than what they're enrolling in |
| max_aqf_level | integer | Maximum AQF level student can already have |
| has_income_threshold | boolean |  |
| max_annual_income | string | Maximum annual income in AUD |
| allows_concession_card | boolean |  |
| allows_disability | boolean |  |
| allows_indigenous | boolean |  |
| priority_indigenous | boolean |  |
| funding_percentage | string | Percentage of course fees covered |
| student_contribution | string | Student contribution/co-payment amount in AUD |
| api_endpoint | string | External API endpoint for eligibility verification |
| api_key_required | boolean |  |
| additional_rules | object | Additional eligibility rules in JSON format |
| is_active | boolean |  |
| effective_from | string |  |
| effective_to | string |  |


### KPISnapshot
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| period | PeriodEnum |  |
| period_display | string |  |
| period_start | string |  |
| period_end | string |  |
| computed_at | string |  |
| metric_key | string | Metric identifier |
| metric_value | string | Numeric metric value |
| metric_unit | string | Unit of measurement (%, count, days, etc.) |
| metadata | object | Additional metric metadata and breakdown |
| previous_value | string |  |
| variance_percentage | string |  |
| trend | string |  |


### KPISnapshotRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| period | PeriodEnum |  |
| period_start | string |  |
| period_end | string |  |
| metric_key | string | Metric identifier |
| metric_value | string | Numeric metric value |
| metric_unit | string | Unit of measurement (%, count, days, etc.) |
| metadata | object | Additional metric metadata and breakdown |
| previous_value | string |  |
| variance_percentage | string |  |


### KindEnum
Type: `string`


### KnowledgeDocument
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| document_number | string |  |
| tenant | string |  |
| title | string |  |
| document_type | KnowledgeDocumentDocumentTypeEnum |  |
| subject | string |  |
| topic | string |  |
| content | string |  |
| summary | string |  |
| keywords | any |  |
| vector_id | string |  |
| embedding_model | string |  |
| chunk_size | integer |  |
| chunks_count | integer |  |
| retrieval_count | integer |  |
| average_relevance_score | number |  |
| last_retrieved_at | string |  |
| visibility | KnowledgeDocumentVisibilityEnum |  |
| course_ids | any |  |
| created_at | string |  |
| updated_at | string |  |


### KnowledgeDocumentDocumentTypeEnum
Type: `string`


### KnowledgeDocumentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| document_type | KnowledgeDocumentDocumentTypeEnum |  |
| subject | string |  |
| topic | string |  |
| content | string |  |
| summary | string |  |
| keywords | any |  |
| embedding_model | string |  |
| chunk_size | integer |  |
| chunks_count | integer |  |
| visibility | KnowledgeDocumentVisibilityEnum |  |
| course_ids | any |  |


### KnowledgeDocumentVisibilityEnum
Type: `string`


### LMSActivity
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| activity_number | string |  |
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| activity_type | LMSActivityActivityTypeEnum |  |
| activity_name | string |  |
| timestamp | string |  |
| duration_minutes | integer |  |
| completion_status | CompletionStatusEnum |  |
| interaction_count | integer | Number of clicks, views, or interactions |
| course_name | string |  |
| module_name | string |  |
| quality_score | string | Score for submissions, quiz results, etc. |
| created_at | string |  |


### LMSActivityActivityTypeEnum
Type: `string`


### LMSActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| activity_type | LMSActivityActivityTypeEnum |  |
| activity_name | string |  |
| timestamp | string |  |
| duration_minutes | integer |  |
| completion_status | CompletionStatusEnum |  |
| interaction_count | integer | Number of clicks, views, or interactions |
| course_name | string |  |
| module_name | string |  |
| quality_score | string | Score for submissions, quiz results, etc. |


### LearningPathway
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| pathway_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| pathway_name | string |  |
| description | string |  |
| difficulty_level | DifficultyLevelEnum |  |
| estimated_duration_hours | string |  |
| recommendation_confidence | string | Confidence score from collaborative filtering algorithm (0-100%) |
| similarity_score | string | Cosine similarity from embedding vectors (0-1) |
| status | LearningPathwayStatusEnum |  |
| total_steps | integer |  |
| completed_steps | integer |  |
| completion_percentage | string |  |
| personalization_factors | object | Factors used for personalization: learning_style, pace, interests, prior_knowledge |
| similar_students | object | Student IDs with similar learning patterns (collaborative filtering) |
| created_at | string |  |
| started_at | string |  |
| completed_at | string |  |
| last_activity | string |  |
| steps | [LearningStep] |  |


### LearningPathwayRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| pathway_name | string |  |
| description | string |  |
| difficulty_level | DifficultyLevelEnum |  |
| estimated_duration_hours | string |  |
| recommendation_confidence | string | Confidence score from collaborative filtering algorithm (0-100%) |
| similarity_score | string | Cosine similarity from embedding vectors (0-1) |
| status | LearningPathwayStatusEnum |  |
| total_steps | integer |  |
| completed_steps | integer |  |
| personalization_factors | object | Factors used for personalization: learning_style, pace, interests, prior_knowledge |
| similar_students | object | Student IDs with similar learning patterns (collaborative filtering) |
| started_at | string |  |
| completed_at | string |  |


### LearningPathwayStatusEnum
Type: `string`


### LearningStep
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| step_number | string |  |
| title | string |  |
| description | string |  |
| content_type | ContentTypeEnum |  |
| content_url | string |  |
| sequence_order | integer |  |
| is_prerequisite | boolean |  |
| prerequisites | [string] | Step numbers that must be completed first |
| estimated_minutes | integer |  |
| difficulty_rating | string | Difficulty rating 1-5 |
| learning_objectives | [string] |  |
| tags | [string] | Content tags for similarity matching |
| status | LearningStepStatusEnum |  |
| completion_score | string |  |
| created_at | string |  |
| started_at | string |  |
| completed_at | string |  |


### LearningStepRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| content_type | ContentTypeEnum |  |
| content_url | string |  |
| sequence_order | integer |  |
| is_prerequisite | boolean |  |
| prerequisites | [string] | Step numbers that must be completed first |
| estimated_minutes | integer |  |
| difficulty_rating | string | Difficulty rating 1-5 |
| learning_objectives | [string] |  |
| tags | [string] | Content tags for similarity matching |
| status | LearningStepStatusEnum |  |
| completion_score | string |  |
| started_at | string |  |
| completed_at | string |  |


### LearningStepStatusEnum
Type: `string`


### LevelTypeEnum
Type: `string`


### LinkedInActivity
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| activity_number | string |  |
| activity_type | LinkedInActivityActivityTypeEnum |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| date_text | string |  |
| skills_mentioned | any |  |
| technologies | any |  |
| companies | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| raw_data | any |  |
| extracted_at | string |  |
| verification_scan | integer |  |


### LinkedInActivityActivityTypeEnum
Type: `string`


### LinkedInActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| activity_type | LinkedInActivityActivityTypeEnum |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| date_text | string |  |
| skills_mentioned | any |  |
| technologies | any |  |
| companies | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| raw_data | any |  |
| verification_scan | integer |  |


### MappingTypeEnum
Type: `string`


### MarkedResponseDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| response_number | string |  |
| auto_marker | object |  |
| student_id | string |  |
| student_name | string |  |
| response_text | string |  |
| word_count | integer |  |
| similarity_score | number | Semantic similarity to model answer (0.0-1.0) |
| keyword_match_score | number | Keyword matching score (0.0-1.0) |
| combined_score | number | Weighted combination of similarity and keyword scores |
| marks_awarded | number |  |
| confidence_score | number | Confidence in the automated marking |
| matched_keywords | object |  |
| missing_keywords | object |  |
| key_phrases_detected | object |  |
| similarity_breakdown | object | Detailed similarity analysis |
| requires_review | boolean |  |
| review_reason | string |  |
| automated_feedback | string |  |
| reviewer_notes | string |  |
| status | StatusFf6Enum |  |
| marking_time | number | Time taken to mark in seconds |
| marked_at | string |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| criterion_scores | [CriterionScore] |  |
| created_at | string |  |
| updated_at | string |  |


### MarkedResponseDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| response_text | string |  |
| requires_review | boolean |  |
| review_reason | string |  |
| automated_feedback | string |  |
| reviewer_notes | string |  |
| status | StatusFf6Enum |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |


### MarkedResponseList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| response_number | string |  |
| auto_marker | integer |  |
| auto_marker_title | string |  |
| student_id | string |  |
| student_name | string |  |
| word_count | integer |  |
| similarity_score | number | Semantic similarity to model answer (0.0-1.0) |
| combined_score | number | Weighted combination of similarity and keyword scores |
| marks_awarded | number |  |
| confidence_score | number | Confidence in the automated marking |
| requires_review | boolean |  |
| status | StatusFf6Enum |  |
| marked_at | string |  |
| created_at | string |  |


### MarkingCriterion
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| criterion_name | string |  |
| description | string |  |
| expected_content | string | Expected content for this criterion |
| weight | number | Weight of this criterion (0.0-1.0) |
| max_points | integer |  |
| criterion_keywords | any |  |
| required | boolean | Is this criterion required? |
| display_order | integer |  |
| created_at | string |  |
| updated_at | string |  |


### MarkingCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_name | string |  |
| description | string |  |
| expected_content | string | Expected content for this criterion |
| weight | number | Weight of this criterion (0.0-1.0) |
| max_points | integer |  |
| criterion_keywords | any |  |
| required | boolean | Is this criterion required? |
| display_order | integer |  |


### MarkingLog
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| auto_marker | integer |  |
| auto_marker_title | string |  |
| response | integer |  |
| action | MarkingLogActionEnum |  |
| performed_by | integer |  |
| performed_by_name | string |  |
| similarity_model | string |  |
| model_version | string |  |
| responses_processed | integer |  |
| total_time | number | Total processing time in seconds |
| average_time_per_response | number |  |
| original_score | number |  |
| new_score | number |  |
| adjustment_reason | string |  |
| details | any |  |
| timestamp | string |  |


### MarkingLogActionEnum
Type: `string`


### MatchTypeEnum
Type: `string`


### MessageTemplate
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| template_number | string |  |
| tenant | string |  |
| name | string |  |
| description | string |  |
| template_type | MessageTemplateTemplateTypeEnum |  |
| template_body | string |  |
| placeholders | any |  |
| default_tone | string |  |
| formality_level | integer |  |
| usage_count | integer |  |
| success_rate | number |  |
| last_used_at | string |  |
| is_active | boolean |  |
| is_system_template | boolean |  |
| created_by | string |  |
| created_at | string |  |
| updated_at | string |  |


### MessageTemplateRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| template_type | MessageTemplateTemplateTypeEnum |  |
| template_body | string |  |
| placeholders | any |  |
| default_tone | string |  |
| formality_level | integer |  |
| usage_count | integer |  |
| success_rate | number |  |
| last_used_at | string |  |
| is_active | boolean |  |
| is_system_template | boolean |  |
| created_by | string |  |


### MessageTemplateTemplateTypeEnum
Type: `string`


### MessageTypeA94Enum
Type: `string`


### MetadataVerification
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| verification_number | string |  |
| submission_analysis | integer |  |
| file_metadata | object | Complete file metadata (EXIF, document properties, etc.) |
| creation_timestamp | string |  |
| modification_timestamp | string |  |
| modification_history | object | History of file modifications |
| author_info | object | Author metadata from file (if available) |
| author_matches_student | boolean |  |
| verification_status | object |  |
| verification_status_display | string |  |
| anomalies_detected | object | List of detected metadata anomalies |
| verification_score | number | Verification score (0-100) |
| verified_at | string |  |


### MetadataVerificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| submission_analysis | integer |  |
| file_metadata | object | Complete file metadata (EXIF, document properties, etc.) |
| creation_timestamp | string |  |
| modification_timestamp | string |  |
| modification_history | object | History of file modifications |
| author_info | object | Author metadata from file (if available) |
| author_matches_student | boolean |  |
| anomalies_detected | object | List of detected metadata anomalies |


### MetadataVerificationVerificationStatusEnum
Type: `string`


### MetricTypeEnum
Type: `string`


### MicroCredential
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| title | string |  |
| code | string | Internal course code |
| description | string |  |
| duration_hours | integer | Total duration in hours |
| delivery_mode | MicroCredentialDeliveryModeEnum |  |
| delivery_mode_display | string |  |
| target_audience | string |  |
| learning_outcomes | object | List of learning outcomes |
| source_units | object | List of units used: [{code, title, nominal_hours, elements}] |
| compressed_content | object | Compressed curriculum with key competencies and assessment tasks |
| tags | object | Searchable tags for categorization |
| skills_covered | object | List of specific skills |
| industry_sectors | object | Relevant industry sectors |
| aqf_level | string | Equivalent AQF level |
| assessment_strategy | string |  |
| assessment_tasks | object | List of assessment tasks with mapping to elements |
| price | string |  |
| max_participants | integer |  |
| prerequisites | string |  |
| status | Status204Enum |  |
| status_display | string |  |
| gpt_generated | boolean |  |
| gpt_model_used | string |  |
| generation_time_seconds | number |  |
| created_by | integer |  |
| created_by_details | string |  |
| enrollment_count | string |  |
| created_at | string |  |
| updated_at | string |  |
| published_at | string |  |


### MicroCredentialDeliveryModeEnum
Type: `string`


### MicroCredentialEnrollment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| micro_credential | integer |  |
| micro_credential_details | string |  |
| student_name | string |  |
| student_email | string |  |
| student_id | string |  |
| status | MicroCredentialEnrollmentStatusEnum |  |
| status_display | string |  |
| enrolled_at | string |  |
| started_at | string |  |
| completed_at | string |  |
| withdrawn_at | string |  |
| progress_data | object | Track completion of learning outcomes and assessments |


### MicroCredentialEnrollmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| micro_credential | integer |  |
| student_name | string |  |
| student_email | string |  |
| student_id | string |  |
| status | MicroCredentialEnrollmentStatusEnum |  |
| started_at | string |  |
| completed_at | string |  |
| withdrawn_at | string |  |
| progress_data | object | Track completion of learning outcomes and assessments |


### MicroCredentialEnrollmentStatusEnum
Type: `string`


### MicroCredentialRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| code | string | Internal course code |
| description | string |  |
| duration_hours | integer | Total duration in hours |
| delivery_mode | MicroCredentialDeliveryModeEnum |  |
| target_audience | string |  |
| learning_outcomes | object | List of learning outcomes |
| source_units | object | List of units used: [{code, title, nominal_hours, elements}] |
| compressed_content | object | Compressed curriculum with key competencies and assessment tasks |
| tags | object | Searchable tags for categorization |
| skills_covered | object | List of specific skills |
| industry_sectors | object | Relevant industry sectors |
| aqf_level | string | Equivalent AQF level |
| assessment_strategy | string |  |
| assessment_tasks | object | List of assessment tasks with mapping to elements |
| price | string |  |
| max_participants | integer |  |
| prerequisites | string |  |
| status | Status204Enum |  |
| created_by | integer |  |
| published_at | string |  |


### MicroCredentialVersion
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| micro_credential | integer |  |
| version_number | integer |  |
| change_summary | string |  |
| content_snapshot | object | Full snapshot of the micro-credential at this version |
| created_by | integer |  |
| created_by_details | string |  |
| created_at | string |  |


### ModerationLog
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| action | ModerationLogActionEnum |  |
| description | string |  |
| decisions_processed | integer |  |
| outliers_found | integer |  |
| bias_flags | integer |  |
| processing_time_ms | integer |  |
| performed_by | string |  |
| timestamp | string |  |
| session | integer |  |


### ModerationLogActionEnum
Type: `string`


### ModerationSession
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| fairness_score | string |  |
| session_number | string |  |
| name | string |  |
| description | string |  |
| assessment_type | ModerationSessionAssessmentTypeEnum |  |
| assessment_title | string |  |
| total_submissions | integer |  |
| assessors_count | integer |  |
| outlier_threshold | number | Standard deviations for outlier detection |
| bias_sensitivity | integer | Sensitivity level for bias detection (1=low, 10=high) |
| status | ModerationSessionStatusEnum |  |
| outliers_detected | integer |  |
| bias_flags_raised | integer |  |
| decisions_compared | integer |  |
| average_agreement_rate | number |  |
| created_at | string |  |
| updated_at | string |  |
| created_by | string |  |


### ModerationSessionAssessmentTypeEnum
Type: `string`


### ModerationSessionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| assessment_type | ModerationSessionAssessmentTypeEnum |  |
| assessment_title | string |  |
| total_submissions | integer |  |
| assessors_count | integer |  |
| outlier_threshold | number | Standard deviations for outlier detection |
| bias_sensitivity | integer | Sensitivity level for bias detection (1=low, 10=high) |
| status | ModerationSessionStatusEnum |  |
| created_by | string |  |


### ModerationSessionStatusEnum
Type: `string`


### NullEnum
Type: `object`


### OperatorEnum
Type: `string`


### OutcomeAchievedEnum
Type: `string`


### OutcomeEb8Enum
Type: `string`


### OutlierDetection
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| decision_details | object |  |
| outlier_number | string |  |
| outlier_type | OutlierTypeEnum |  |
| severity | SeverityE88Enum |  |
| z_score | number | Standard deviations from mean |
| deviation_percentage | number | Percentage deviation from average |
| expected_score | number |  |
| actual_score | number |  |
| cohort_mean | number |  |
| cohort_std_dev | number |  |
| assessor_mean | number | Assessor's average score across all submissions |
| explanation | string |  |
| confidence_score | number | Confidence in outlier detection (0-1) |
| is_resolved | boolean |  |
| resolution_notes | string |  |
| resolved_by | string |  |
| resolved_at | string |  |
| detected_at | string |  |
| session | integer |  |
| decision | integer |  |


### OutlierDetectionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| outlier_type | OutlierTypeEnum |  |
| severity | SeverityE88Enum |  |
| z_score | number | Standard deviations from mean |
| deviation_percentage | number | Percentage deviation from average |
| expected_score | number |  |
| actual_score | number |  |
| cohort_mean | number |  |
| cohort_std_dev | number |  |
| assessor_mean | number | Assessor's average score across all submissions |
| explanation | string |  |
| confidence_score | number | Confidence in outlier detection (0-1) |
| is_resolved | boolean |  |
| resolution_notes | string |  |
| resolved_by | string |  |
| resolved_at | string |  |
| session | integer |  |
| decision | integer |  |


### OutlierTypeEnum
Type: `string`


### OverallStatusEnum
Type: `string`


### PDActivity
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| activity_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| trainer_role | string |  |
| department | string |  |
| activity_type | ActivityType9adEnum |  |
| activity_title | string |  |
| description | string |  |
| provider | string |  |
| start_date | string |  |
| end_date | string |  |
| hours_completed | number |  |
| compliance_areas | any |  |
| industry_sectors | any |  |
| qualification_levels | any |  |
| evidence_type | object |  |
| evidence_files | any |  |
| verification_status | VerificationStatus901Enum |  |
| verified_by | string |  |
| verified_date | string |  |
| learning_outcomes | string |  |
| application_to_practice | string |  |
| reflection_notes | string |  |
| maintains_vocational_currency | boolean |  |
| maintains_industry_currency | boolean |  |
| maintains_teaching_currency | boolean |  |
| meets_asqa_requirements | boolean |  |
| compliance_notes | string |  |
| status | StatusF31Enum |  |
| created_at | string |  |
| updated_at | string |  |


### PDActivityDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| days_duration | string |  |
| is_recent | string |  |
| activity_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| trainer_role | string |  |
| department | string |  |
| activity_type | ActivityType9adEnum |  |
| activity_title | string |  |
| description | string |  |
| provider | string |  |
| start_date | string |  |
| end_date | string |  |
| hours_completed | number |  |
| compliance_areas | any |  |
| industry_sectors | any |  |
| qualification_levels | any |  |
| evidence_type | object |  |
| evidence_files | any |  |
| verification_status | VerificationStatus901Enum |  |
| verified_by | string |  |
| verified_date | string |  |
| learning_outcomes | string |  |
| application_to_practice | string |  |
| reflection_notes | string |  |
| maintains_vocational_currency | boolean |  |
| maintains_industry_currency | boolean |  |
| maintains_teaching_currency | boolean |  |
| meets_asqa_requirements | boolean |  |
| compliance_notes | string |  |
| status | StatusF31Enum |  |
| created_at | string |  |
| updated_at | string |  |


### PDActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| trainer_role | string |  |
| department | string |  |
| activity_type | ActivityType9adEnum |  |
| activity_title | string |  |
| description | string |  |
| provider | string |  |
| start_date | string |  |
| end_date | string |  |
| hours_completed | number |  |
| compliance_areas | any |  |
| industry_sectors | any |  |
| qualification_levels | any |  |
| evidence_type | object |  |
| evidence_files | any |  |
| verification_status | VerificationStatus901Enum |  |
| verified_by | string |  |
| verified_date | string |  |
| learning_outcomes | string |  |
| application_to_practice | string |  |
| reflection_notes | string |  |
| maintains_vocational_currency | boolean |  |
| maintains_industry_currency | boolean |  |
| maintains_teaching_currency | boolean |  |
| meets_asqa_requirements | boolean |  |
| compliance_notes | string |  |
| status | StatusF31Enum |  |


### PDSuggestion
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| trainer_name | string |  |
| suggestion_number | string |  |
| suggested_activity_type | string |  |
| activity_title | string |  |
| description | string |  |
| rationale | string |  |
| addresses_currency_gap | AddressesCurrencyGapEnum |  |
| priority_level | PriorityLevelF2aEnum |  |
| suggested_providers | any |  |
| estimated_hours | number |  |
| estimated_cost | number |  |
| suggested_timeframe | string |  |
| deadline | string |  |
| generated_by_model | string |  |
| generation_date | string |  |
| prompt_used | string |  |
| confidence_score | number |  |
| status | Status251Enum |  |
| trainer_feedback | string |  |
| created_at | string |  |
| trainer_profile | integer |  |
| linked_activity | integer |  |


### PDSuggestionDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| trainer_name | string |  |
| trainer_role | string |  |
| is_urgent | string |  |
| days_until_deadline | string |  |
| suggestion_number | string |  |
| suggested_activity_type | string |  |
| activity_title | string |  |
| description | string |  |
| rationale | string |  |
| addresses_currency_gap | AddressesCurrencyGapEnum |  |
| priority_level | PriorityLevelF2aEnum |  |
| suggested_providers | any |  |
| estimated_hours | number |  |
| estimated_cost | number |  |
| suggested_timeframe | string |  |
| deadline | string |  |
| generated_by_model | string |  |
| generation_date | string |  |
| prompt_used | string |  |
| confidence_score | number |  |
| status | Status251Enum |  |
| trainer_feedback | string |  |
| created_at | string |  |
| trainer_profile | integer |  |
| linked_activity | integer |  |


### PDSuggestionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| suggested_activity_type | string |  |
| activity_title | string |  |
| description | string |  |
| rationale | string |  |
| addresses_currency_gap | AddressesCurrencyGapEnum |  |
| priority_level | PriorityLevelF2aEnum |  |
| suggested_providers | any |  |
| estimated_hours | number |  |
| estimated_cost | number |  |
| suggested_timeframe | string |  |
| deadline | string |  |
| generated_by_model | string |  |
| prompt_used | string |  |
| confidence_score | number |  |
| status | Status251Enum |  |
| trainer_feedback | string |  |
| trainer_profile | integer |  |
| linked_activity | integer |  |


### PaginatedAIRunList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AIRun] |  |


### PaginatedASQAClauseList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ASQAClause] |  |


### PaginatedASQAStandardList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ASQAStandard] |  |


### PaginatedActionStepList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ActionStep] |  |


### PaginatedActionTrackingList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ActionTracking] |  |


### PaginatedAnomalyDetectionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AnomalyDetection] |  |


### PaginatedAssessmentCriteriaList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AssessmentCriteria] |  |


### PaginatedAssessmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Assessment] |  |


### PaginatedAssessmentTaskList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AssessmentTask] |  |


### PaginatedAssessorDecisionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AssessorDecision] |  |


### PaginatedAttachmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Attachment] |  |


### PaginatedAttendanceRecordList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AttendanceRecord] |  |


### PaginatedAudioRecordingList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AudioRecording] |  |


### PaginatedAuditList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Audit] |  |


### PaginatedAuditLogList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AuditLog] |  |


### PaginatedAuditReportList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AuditReport] |  |


### PaginatedAuthenticityCheckListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AuthenticityCheckList] |  |


### PaginatedAutoMarkerListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [AutoMarkerList] |  |


### PaginatedBiasScoreList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [BiasScore] |  |


### PaginatedChatMessageList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ChatMessage] |  |


### PaginatedChatSessionListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ChatSessionList] |  |


### PaginatedClauseEvidenceList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ClauseEvidence] |  |


### PaginatedClauseLinkList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ClauseLink] |  |


### PaginatedCoachConfigurationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [CoachConfiguration] |  |


### PaginatedCoachingInsightList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [CoachingInsight] |  |


### PaginatedCommentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Comment] |  |


### PaginatedComparisonSessionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ComparisonSession] |  |


### PaginatedCompetencyGapList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [CompetencyGap] |  |


### PaginatedComplianceCheckList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ComplianceCheck] |  |


### PaginatedComplianceRuleList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ComplianceRule] |  |


### PaginatedContentEmbeddingList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ContentEmbedding] |  |


### PaginatedConversationThreadList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ConversationThread] |  |


### PaginatedCriteriaTagList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [CriteriaTag] |  |


### PaginatedCurrencyEvidenceList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [CurrencyEvidence] |  |


### PaginatedDailySummaryList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [DailySummary] |  |


### PaginatedDecisionOverrideList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [DecisionOverride] |  |


### PaginatedDiaryEntryListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [DiaryEntryList] |  |


### PaginatedDiscussionSentimentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [DiscussionSentiment] |  |


### PaginatedDraftReplyList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [DraftReply] |  |


### PaginatedEligibilityCheckList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EligibilityCheck] |  |


### PaginatedEligibilityRequestListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EligibilityRequestList] |  |


### PaginatedEligibilityRuleList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EligibilityRule] |  |


### PaginatedEmbeddingSearchList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EmbeddingSearch] |  |


### PaginatedEngagementAlertList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EngagementAlert] |  |


### PaginatedEngagementHeatmapList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EngagementHeatmap] |  |


### PaginatedEntityExtractionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EntityExtraction] |  |


### PaginatedEvidenceAttachmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EvidenceAttachment] |  |


### PaginatedEvidenceAuditList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EvidenceAudit] |  |


### PaginatedEvidenceDocumentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EvidenceDocument] |  |


### PaginatedEvidenceList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Evidence] |  |


### PaginatedEvidenceMappingList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [EvidenceMapping] |  |


### PaginatedFeedbackCriterionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [FeedbackCriterion] |  |


### PaginatedFeedbackLogList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [FeedbackLog] |  |


### PaginatedFeedbackTemplateListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [FeedbackTemplateList] |  |


### PaginatedGeneratedFeedbackListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [GeneratedFeedbackList] |  |


### PaginatedGitHubActivityList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [GitHubActivity] |  |


### PaginatedImprovementActionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ImprovementAction] |  |


### PaginatedImprovementCategoryList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ImprovementCategory] |  |


### PaginatedImprovementReviewList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ImprovementReview] |  |


### PaginatedIntegrationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Integration] |  |


### PaginatedInterventionActionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [InterventionAction] |  |


### PaginatedInterventionListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [InterventionList] |  |


### PaginatedInterventionRuleList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [InterventionRule] |  |


### PaginatedInterventionWorkflowList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [InterventionWorkflow] |  |


### PaginatedJurisdictionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Jurisdiction] |  |


### PaginatedJurisdictionRequirementList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [JurisdictionRequirement] |  |


### PaginatedKPISnapshotList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [KPISnapshot] |  |


### PaginatedKnowledgeDocumentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [KnowledgeDocument] |  |


### PaginatedLMSActivityList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [LMSActivity] |  |


### PaginatedLearningPathwayList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [LearningPathway] |  |


### PaginatedLearningStepList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [LearningStep] |  |


### PaginatedLinkedInActivityList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [LinkedInActivity] |  |


### PaginatedMarkedResponseListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MarkedResponseList] |  |


### PaginatedMarkingCriterionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MarkingCriterion] |  |


### PaginatedMarkingLogList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MarkingLog] |  |


### PaginatedMessageTemplateList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MessageTemplate] |  |


### PaginatedMetadataVerificationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MetadataVerification] |  |


### PaginatedMicroCredentialEnrollmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MicroCredentialEnrollment] |  |


### PaginatedMicroCredentialList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MicroCredential] |  |


### PaginatedMicroCredentialVersionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [MicroCredentialVersion] |  |


### PaginatedModerationLogList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ModerationLog] |  |


### PaginatedModerationSessionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ModerationSession] |  |


### PaginatedOutlierDetectionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [OutlierDetection] |  |


### PaginatedPDActivityList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [PDActivity] |  |


### PaginatedPDSuggestionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [PDSuggestion] |  |


### PaginatedPathwayRecommendationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [PathwayRecommendation] |  |


### PaginatedPlagiarismMatchList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [PlagiarismMatch] |  |


### PaginatedPolicyList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Policy] |  |


### PaginatedQualificationMappingList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [QualificationMapping] |  |


### PaginatedReferenceTableList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ReferenceTable] |  |


### PaginatedReplyHistoryList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ReplyHistory] |  |


### PaginatedRiskAssessmentListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [RiskAssessmentList] |  |


### PaginatedRiskFactorList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [RiskFactor] |  |


### PaginatedRubricCriterionList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [RubricCriterion] |  |


### PaginatedRubricLevelList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [RubricLevel] |  |


### PaginatedRubricList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Rubric] |  |


### PaginatedRulesetList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Ruleset] |  |


### PaginatedSLAPolicyList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [SLAPolicy] |  |


### PaginatedSentimentAnalysisList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [SentimentAnalysis] |  |


### PaginatedStudentEngagementMetricList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [StudentEngagementMetric] |  |


### PaginatedStudentMessageList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [StudentMessage] |  |


### PaginatedStudentProgressList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [StudentProgress] |  |


### PaginatedSubmissionAnalysisListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [SubmissionAnalysisList] |  |


### PaginatedSubmissionEvidenceList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [SubmissionEvidence] |  |


### PaginatedTASList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TAS] |  |


### PaginatedTASTemplateList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TASTemplate] |  |


### PaginatedTaxonomyLabelList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TaxonomyLabel] |  |


### PaginatedTenantAPIKeyList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TenantAPIKey] |  |


### PaginatedTenantList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Tenant] |  |


### PaginatedTenantUserList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TenantUser] |  |


### PaginatedToneProfileList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [ToneProfile] |  |


### PaginatedTrainerAssignmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TrainerAssignment] |  |


### PaginatedTrainerProfileList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TrainerProfile] |  |


### PaginatedTrainerProfileListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TrainerProfileList] |  |


### PaginatedTrainerQualificationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TrainerQualification] |  |


### PaginatedTranscriptionJobList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [TranscriptionJob] |  |


### PaginatedUnitOfCompetencyList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [UnitOfCompetency] |  |


### PaginatedUserInvitationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [UserInvitation] |  |


### PaginatedVerificationList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [Verification] |  |


### PaginatedVerificationScanListList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [VerificationScanList] |  |


### PaginatedWebhookEndpointList
Type: `object`

| Property | Type | Description |
|---|---|---|
| count | integer |  |
| next | string |  |
| previous | string |  |
| results | [WebhookEndpoint] |  |


### ParticipationLevelEnum
Type: `string`


### PatchedASQAClauseRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| standard | integer |  |
| clause_number | string | e.g., 1.1, 1.2, 1.3 |
| title | string |  |
| clause_text | string | Full text of the clause |
| evidence_required | object | Types of evidence needed |
| keywords | object | Key terms for text similarity |
| compliance_level | ComplianceLevelEnum |  |
| is_active | boolean |  |


### PatchedASQAStandardRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| standard_number | string | e.g., Standard 1.1 (2015) or QA1.1 (2025) |
| title | string |  |
| description | string |  |
| standard_type | StandardTypeEnum |  |
| full_text | string | Complete text of the ASQA standard |
| requirements | object | List of specific requirements |
| is_active | boolean |  |
| effective_date | string |  |
| version | object |  |


### PatchedActionStepRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| title | string |  |
| description | string |  |
| sequence_order | integer | Order of execution |
| owner | integer |  |
| status | ActionStepStatusEnum |  |
| due_date | string |  |
| started_at | string |  |
| completed_at | string |  |
| progress_notes | string |  |
| evidence_refs | object | References to evidence documents/files |
| is_blocked | boolean |  |
| blocker_description | string |  |
| blocker_resolved_at | string |  |


### PatchedActionTrackingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| update_type | UpdateTypeEnum |  |
| update_text | string | Description of the update |
| progress_percentage | integer | Overall progress (0-100) |
| old_status | string |  |
| new_status | string |  |
| is_blocker | boolean |  |
| blocker_resolved | boolean |  |
| blocker_resolution | string |  |
| evidence_provided | object | Evidence of progress (file URLs, references) |
| created_by | integer |  |


### PatchedAnomalyDetectionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| submission_analysis | integer |  |
| anomaly_type | AnomalyTypeEnum |  |
| severity | SeverityE88Enum |  |
| anomaly_data | object | Detailed anomaly data and evidence |
| description | string |  |
| confidence_score | number | Confidence in anomaly detection (0.0-1.0) |
| acknowledged | boolean |  |
| false_positive | boolean |  |
| resolution_notes | string |  |


### PatchedAssessmentCriteriaRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| task | integer | Optional: Link to specific task |
| criterion_number | string |  |
| criterion_text | string | What the student must demonstrate |
| unit_element | string |  |
| performance_criterion | string |  |
| knowledge_evidence | string |  |
| satisfactory_evidence | string | What constitutes satisfactory performance |
| not_satisfactory_evidence | string | What would be unsatisfactory |
| ai_generated | boolean |  |
| display_order | integer |  |


### PatchedAssessmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| unit_code | string | Training package unit code (e.g., BSBWHS211) |
| unit_title | string |  |
| training_package | string | e.g., BSB - Business Services |
| unit_release | string | Release number |
| assessment_type | AssessmentType64bEnum |  |
| title | string |  |
| version | string |  |
| instructions | string | AI-generated assessment instructions |
| context | string | Assessment context and scenario |
| conditions | string | Assessment conditions (equipment, resources, etc.) |
| ai_generated | boolean |  |
| ai_model | string | e.g., GPT-4 |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| blooms_analysis | object | Bloom's taxonomy verb analysis: {level: count} |
| blooms_distribution | object | Distribution percentages across Bloom's levels |
| dominant_blooms_level | string | Most prominent Bloom's level |
| is_compliant | boolean |  |
| compliance_score | integer | Overall compliance score (0-100) |
| compliance_notes | string |  |
| elements_covered | object | List of unit elements covered |
| performance_criteria_covered | object | List of performance criteria covered |
| knowledge_evidence_covered | object | List of knowledge evidence items covered |
| performance_evidence_covered | object | List of performance evidence items covered |
| estimated_duration_hours | string | Estimated completion time in hours |
| status | Status304Enum |  |
| reviewed_at | string |  |
| approved_at | string |  |


### PatchedAssessmentTaskRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| task_number | string | e.g., '1', '1a', 'A.1' |
| task_type | AssessmentTaskTaskTypeEnum |  |
| question | string | The task question or instruction |
| context | string | Additional context, scenario, or information for the task |
| ai_generated | boolean |  |
| ai_rationale | string | AI explanation of why this task was generated |
| blooms_level | string | Primary Bloom's taxonomy level |
| blooms_verbs | object | Bloom's taxonomy verbs detected in this task |
| maps_to_elements | object | Unit elements this task addresses |
| maps_to_performance_criteria | object | Performance criteria this task addresses |
| maps_to_knowledge_evidence | object | Knowledge evidence this task addresses |
| question_count | integer | Number of sub-questions (for multi-part tasks) |
| estimated_time_minutes | integer | Estimated completion time in minutes |
| marks_available | integer | Total marks for this task |
| display_order | integer |  |


### PatchedAssessorDecisionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| assessor_id | string |  |
| assessor_name | string |  |
| score | number |  |
| max_score | number |  |
| grade | GradeEnum |  |
| criterion_scores | object | Dictionary of criterion_id -> score |
| requires_review | boolean |  |
| comments | string |  |
| marking_time_minutes | integer |  |
| marked_at | string |  |
| session | integer |  |


### PatchedAttachmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| file_uri | string | S3 URI or file path |
| filename | string |  |
| file_size | integer | Size in bytes |
| mime_type | string |  |
| kind | KindEnum |  |
| sha256_hash | string | File integrity hash |
| description | string |  |


### PatchedAttendanceRecordRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| status | AttendanceRecordStatusEnum |  |
| session_name | string |  |
| scheduled_start | string |  |
| scheduled_end | string |  |
| actual_arrival | string |  |
| actual_departure | string |  |
| minutes_late | integer |  |
| minutes_attended | integer |  |
| participation_level | ParticipationLevelEnum |  |
| notes | string |  |


### PatchedAudioRecordingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| recording_filename | string |  |
| recording_file_path | string |  |
| recording_file_size_mb | number |  |
| recording_duration_seconds | number |  |
| recording_format | string |  |
| transcript_text | string |  |
| transcript_confidence | number |  |
| transcript_language | string |  |
| processing_status | ProcessingStatusEnum |  |
| error_message | string |  |
| diary_entry | integer |  |


### PatchedAuditReportRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| report_number | string |  |
| title | string |  |
| description | string |  |
| asqa_standards | [integer] | ASQA standards included in this audit |
| audit_period_start | string | Start date of audit period |
| audit_period_end | string | End date of audit period |
| status | Status9adEnum |  |
| findings | object | List of findings: [{clause: str, finding: str, severity: str, recommendation: str}] |
| recommendations | object | Overall recommendations |
| created_by | integer |  |
| completed_at | string |  |
| submitted_at | string |  |
| submitted_by | integer |  |


### PatchedAuthenticityCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| assessment | integer |  |
| name | string |  |
| description | string |  |
| plagiarism_threshold | number | Similarity threshold for plagiarism detection (0.0-1.0) |
| metadata_verification_enabled | boolean |  |
| anomaly_detection_enabled | boolean |  |
| academic_integrity_mode | boolean | Enable strict academic integrity compliance |
| status | Status24eEnum |  |
| created_by | integer |  |


### PatchedAutoMarkerDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| answer_type | AnswerTypeEnum |  |
| question_text | string | The question being asked |
| model_answer | string | The ideal/model answer for comparison |
| max_marks | integer |  |
| similarity_model | SimilarityModelEnum |  |
| similarity_threshold | number | Minimum similarity score for full marks (0.0-1.0) |
| partial_credit_enabled | boolean |  |
| min_similarity_for_credit | number | Minimum similarity for partial credit |
| use_keywords | boolean | Enable keyword matching |
| keywords | object | Required keywords for full marks |
| keyword_weight | number | Weight of keyword matching in final score |
| status | Status86cEnum |  |


### PatchedBiasScoreRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| assessor_id | string |  |
| assessor_name | string |  |
| bias_type | BiasTypeEnum |  |
| bias_score | number | Bias score (0=no bias, 1=severe bias) |
| sample_size | integer | Number of decisions analyzed |
| mean_difference | number | Difference from cohort mean |
| std_dev_ratio | number | Ratio to cohort standard deviation |
| evidence | object | Statistical evidence and patterns detected |
| affected_students | object | List of student IDs affected by bias |
| is_validated | boolean |  |
| validation_notes | string |  |
| validated_by | string |  |
| validated_at | string |  |
| recommendation | string | Action recommended to address bias |
| severity_level | integer | Severity level (1=minor, 10=critical) |
| session | integer |  |


### PatchedChangePasswordRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| old_password | string |  |
| new_password | string |  |
| new_password_confirm | string |  |


### PatchedChatSessionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| subject | string |  |
| topic | string |  |
| session_type | SessionTypeEnum |  |
| status | StatusF84Enum |  |
| message_count | integer |  |
| total_duration_minutes | integer |  |
| satisfaction_rating | integer |  |
| student_feedback | string |  |
| referenced_materials | any |  |
| key_concepts_discussed | any |  |
| follow_up_needed | boolean |  |
| follow_up_reason | string |  |
| completed_at | string |  |


### PatchedClauseEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| asqa_clause | integer |  |
| evidence | integer |  |
| mapping_type | MappingTypeEnum |  |
| confidence_score | number | Confidence score (0.0-1.0) for auto-tagged matches |
| matched_entities | object | NER entities that triggered this mapping: [{entity: str, type: str}] |
| matched_keywords | object | Keywords that matched between clause and evidence |
| rule_name | string | Name of rule that triggered mapping |
| rule_metadata | object | Additional rule processing data |
| is_verified | boolean | Manually verified by reviewer |
| verified_by | integer |  |
| verified_at | string |  |
| relevance_notes | string | Notes on evidence relevance to clause |


### PatchedClauseLinkRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| clause | integer |  |
| source | ClauseLinkSourceEnum |  |
| confidence | number | Confidence score for AI suggestions (0.0-1.0) |
| rationale | string | Explanation for the clause link |
| reviewed | boolean |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |


### PatchedCoachConfigurationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| primary_model | string |  |
| fallback_model | string |  |
| temperature | number |  |
| max_tokens | integer |  |
| coaching_style | CoachingStyleEnum |  |
| personality_traits | any |  |
| system_prompt | string |  |
| response_guidelines | any |  |
| prohibited_topics | any |  |
| vector_db_enabled | boolean |  |
| top_k_results | integer |  |
| similarity_threshold | number |  |
| content_filter_enabled | boolean |  |
| profanity_filter | boolean |  |
| escalation_keywords | any |  |
| available_24_7 | boolean |  |
| business_hours_only | boolean |  |
| timezone | string |  |


### PatchedCoachingInsightRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| time_period | string |  |
| total_sessions | integer |  |
| total_messages | integer |  |
| total_duration_minutes | integer |  |
| average_session_length | number |  |
| session_type_distribution | any |  |
| most_discussed_subjects | any |  |
| most_discussed_topics | any |  |
| knowledge_gaps_identified | any |  |
| average_sentiment_score | number |  |
| sentiment_trend | SentimentTrendEnum |  |
| average_satisfaction | number |  |
| sessions_with_feedback | integer |  |
| recommended_resources | any |  |
| follow_up_actions | any |  |
| at_risk_indicators | any |  |


### PatchedCommentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| body | string |  |
| visibility | Visibility757Enum |  |
| parent | integer |  |
| mentioned_users | [integer] |  |


### PatchedCompetencyGapRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| gap_type | GapTypeEnum |  |
| gap_severity | GapSeverityEnum |  |
| gap_description | string |  |
| required_qualification | string |  |
| required_competency | string |  |
| required_experience_years | integer |  |
| current_qualifications | any |  |
| is_resolved | boolean |  |
| resolution_date | string |  |
| resolution_notes | string |  |
| recommended_action | string |  |
| estimated_resolution_time | string |  |
| unit | integer |  |
| assignment | integer |  |


### PatchedComplianceCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| check_type | string |  |
| check_status | CheckStatusEnum |  |
| trainer_ids | any |  |
| unit_codes | any |  |
| total_assignments_checked | integer |  |
| compliant_assignments | integer |  |
| non_compliant_assignments | integer |  |
| gaps_found | integer |  |
| critical_gaps | integer |  |
| high_gaps | integer |  |
| medium_gaps | integer |  |
| low_gaps | integer |  |
| overall_compliance_score | number |  |
| report_summary | string |  |
| detailed_results | any |  |
| recommendations | any |  |
| started_at | string |  |
| completed_at | string |  |
| execution_time_seconds | number |  |
| error_message | string |  |


### PatchedComplianceRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| regulatory_source | RegulatorySourceEnum |  |
| reference_code | string |  |
| applies_to_roles | any |  |
| applies_to_sectors | any |  |
| applies_to_qualifications | any |  |
| requirement_type | RequirementTypeEnum |  |
| requirement_details | any |  |
| is_active | boolean |  |
| effective_date | string |  |
| expiry_date | string |  |


### PatchedContentEmbeddingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| step | integer |  |
| embedding_vector | [number] | 384-dimensional embedding vector from sentence-transformers |
| model_name | string | Name of the embedding model used |
| text_content | string | Text used to generate embedding (title + description + objectives) |
| similar_content | object | Cached list of similar step_numbers with similarity scores |


### PatchedConversationThreadRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_email | string |  |
| student_name | string |  |
| subject | string |  |
| message_count | integer |  |
| first_message_date | string |  |
| last_message_date | string |  |
| is_active | boolean |  |
| is_resolved | boolean |  |
| resolved_at | string |  |
| primary_category | string |  |
| tags | any |  |


### PatchedCriteriaTagRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_id | string | Reference to assessment criterion |
| criterion_name | string |  |
| criterion_description | string |  |
| tagged_text | string | Excerpt from submission linked to criterion |
| text_start_position | integer | Character position in original text |
| text_end_position | integer |  |
| context_before | string | Text before tagged excerpt |
| context_after | string | Text after tagged excerpt |
| tag_type | TagTypeEnum |  |
| confidence_level | ConfidenceLevelEnum |  |
| confidence_score | number | Automated confidence score (0-1) |
| notes | string | Assessor notes about this evidence |
| keywords | object | Extracted keywords from tagged text |
| is_validated | boolean |  |
| validated_by | string |  |
| validated_at | string |  |
| tagged_by | string |  |
| evidence | integer |  |


### PatchedCurrencyEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| evidence_type | CurrencyEvidenceEvidenceTypeEnum |  |
| title | string |  |
| content | string |  |
| evidence_start_date | string |  |
| evidence_end_date | string |  |
| total_activities | integer |  |
| relevant_activities | integer |  |
| currency_score | number |  |
| linkedin_activities_included | any |  |
| github_activities_included | any |  |
| file_format | FileFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| meets_rto_standards | boolean |  |
| compliance_notes | string |  |
| is_approved | boolean |  |
| approved_by | string |  |
| approved_at | string |  |
| trainer_profile | integer |  |
| verification_scan | integer |  |


### PatchedDailySummaryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| summary_date | string |  |
| total_sessions | integer |  |
| total_teaching_hours | number |  |
| total_students | integer |  |
| courses_taught | any |  |
| daily_highlights | string |  |
| overall_student_engagement | string |  |
| key_achievements | any |  |
| challenges_summary | string |  |
| action_items_pending | any |  |
| diary_entries_included | any |  |
| evidence_documents_created | integer |  |
| generated_by_model | string |  |


### PatchedDecisionOverrideRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| decision | integer |  |
| reason_code | string |  |
| justification | string | Detailed justification for override |
| final_outcome | FinalOutcomeEnum |  |
| policy_version | string | Override policy version applied |
| evidence_refs | any |  |


### PatchedDiaryEntryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| session_date | string |  |
| session_time_start | string |  |
| session_time_end | string |  |
| session_duration_minutes | integer |  |
| course_name | string |  |
| course_code | string |  |
| unit_of_competency | string |  |
| student_count | integer |  |
| delivery_mode | DiaryEntryDeliveryModeEnum |  |
| raw_transcript | string |  |
| manual_notes | string |  |
| session_summary | string |  |
| key_topics_covered | any |  |
| student_engagement_notes | string |  |
| challenges_encountered | string |  |
| follow_up_actions | any |  |
| learning_outcomes_addressed | any |  |
| assessment_activities | string |  |
| resources_used | any |  |
| evidence_attachments | any |  |
| transcription_model | string |  |
| summarization_model | string |  |
| transcription_duration_seconds | number |  |
| summarization_tokens | integer |  |
| entry_status | EntryStatusEnum |  |
| is_pinned | boolean |  |
| is_shared | boolean |  |


### PatchedDiscussionSentimentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| timestamp | string |  |
| message_type | DiscussionSentimentMessageTypeEnum |  |
| message_content | string |  |
| sentiment_score | string | Sentiment polarity: -1 (very negative) to +1 (very positive) |
| confidence | string | Confidence in sentiment classification (0-1) |
| primary_emotion | object |  |
| emotion_scores | object | Emotion probabilities: {joy: 0.2, frustration: 0.6, ...} |
| word_count | integer |  |
| question_count | integer |  |
| exclamation_count | integer |  |
| negative_keywords | [string] | Detected negative or concerning keywords |
| help_seeking_keywords | [string] | Keywords indicating student needs help |
| discussion_topic | string |  |
| reply_count | integer |  |


### PatchedDraftReplyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| reply_body | string |  |
| reply_subject | string |  |
| tone_used | string |  |
| formality_level | integer |  |
| include_greeting | boolean |  |
| include_signature | boolean |  |
| confidence_score | number |  |
| readability_score | number |  |
| word_count | integer |  |
| estimated_reading_time_seconds | integer |  |
| was_edited | boolean |  |
| was_sent | boolean |  |
| was_rejected | boolean |  |
| rejection_reason | string |  |
| generation_status | GenerationStatusEnum |  |
| generation_time_ms | integer |  |
| llm_model_used | string |  |
| generation_prompt | string |  |
| sent_at | string |  |
| student_message | integer |  |
| template_used | integer |  |


### PatchedEligibilityCheckRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_first_name | string |  |
| student_last_name | string |  |
| student_dob | string | Date of birth |
| student_email | string |  |
| student_phone | string |  |
| course_code | string |  |
| course_name | string |  |
| aqf_level | integer | AQF level of course (1-10) |
| intended_start_date | string |  |
| jurisdiction | JurisdictionEnum |  |
| jurisdiction_requirement | integer |  |
| funding_program_code | string |  |
| student_data | object | Student eligibility information including citizenship, residency, employment, etc. |
| status | StatusE22Enum |  |
| is_eligible | boolean |  |
| eligibility_percentage | string | Percentage of rules passed |
| rules_checked | integer |  |
| rules_passed | integer |  |
| rules_failed | integer |  |
| check_results | object | Detailed results of each rule evaluation |
| failed_rules | object | List of failed rule details |
| warnings | object | Non-critical warnings |
| api_verified | boolean |  |
| api_response | object | Response from external API verification |
| api_verified_at | string |  |
| override_required | boolean |  |
| override_approved | boolean |  |
| override_reason | string |  |
| override_approved_at | string |  |
| prevents_enrollment | boolean | If ineligible, prevent enrollment |
| compliance_notes | string |  |
| valid_until | string | Eligibility expiry date |


### PatchedEligibilityRequestRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| person_id | string | Person identifier in SMS/LMS |
| course_id | string | Course identifier |
| jurisdiction_code | string |  |
| input | object | Complete input data for evaluation |
| evidence_refs | object | References to attached evidence documents |
| metadata | object | Additional metadata |


### PatchedEligibilityRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| jurisdiction_requirement | integer | Link to specific jurisdiction requirement (optional) |
| rule_type | RuleTypeEnum |  |
| name | string |  |
| description | string |  |
| field_name | string | Field to evaluate (e.g., 'age', 'citizenship_status', 'income') |
| operator | OperatorEnum |  |
| expected_value | string | Expected value or comma-separated list for comparison |
| is_mandatory | boolean | Must pass for eligibility (vs. optional/bonus points) |
| priority | integer | Evaluation priority (1=highest) |
| error_message | string | Message shown when rule fails |
| override_allowed | boolean | Can be manually overridden by authorized staff |
| is_active | boolean |  |


### PatchedEngagementAlertRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| alert_type | AlertTypeEnum |  |
| severity | SeverityE88Enum |  |
| title | string |  |
| description | string |  |
| trigger_metrics | object | Metrics that triggered this alert: {attendance_score: 45, days_absent: 5} |
| recommended_actions | [string] | Suggested interventions |
| status | EngagementAlertStatusEnum |  |
| acknowledged_by | string |  |
| acknowledged_at | string |  |
| resolved_at | string |  |
| resolution_notes | string |  |


### PatchedEngagementHeatmapRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| time_period | object |  |
| start_date | string |  |
| end_date | string |  |
| attendance_score | string |  |
| lms_activity_score | string |  |
| sentiment_score | string | Normalized sentiment (0=very negative, 100=very positive) |
| risk_flags | [string] | Specific risk indicators: low_attendance, inactive_lms, negative_sentiment, etc. |
| heatmap_data | object | Daily engagement data: {date: {attendance: bool, lms_minutes: int, sentiment: float}} |
| engagement_trend | EngagementTrendEnum |  |
| change_percentage | string | Percentage change from previous period |
| alerts_triggered | integer |  |
| interventions_applied | integer |  |


### PatchedEntityExtractionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| source_type | EntityExtractionSourceTypeEnum |  |
| source_url | string |  |
| source_text | string |  |
| entities | any |  |
| extraction_confidence | number |  |
| entity_count | integer |  |
| nlp_model_used | string |  |
| processing_time_ms | number |  |
| verification_scan | integer |  |


### PatchedEvidenceAttachmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| request | integer |  |
| filename | string |  |
| mime_type | string |  |
| type | EvidenceAttachmentTypeEnum |  |
| verified | boolean |  |
| verifier | integer |  |
| verified_at | string |  |
| verification_notes | string |  |


### PatchedEvidenceDocumentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| document_type | EvidenceDocumentDocumentTypeEnum |  |
| document_title | string |  |
| document_content | string |  |
| document_format | DocumentFormatEnum |  |
| file_path | string |  |
| file_size_kb | number |  |
| generated_by | string |  |
| generation_method | GenerationMethodEnum |  |
| meets_compliance_standards | boolean |  |
| compliance_notes | string |  |
| diary_entry | integer |  |


### PatchedEvidenceMappingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| assessment_type | EvidenceMappingAssessmentTypeEnum |  |
| assessment_title | string |  |
| unit_code | string |  |
| total_criteria | integer |  |
| total_submissions | integer |  |
| auto_extract_text | boolean | Automatically extract text from submissions |
| generate_embeddings | boolean | Generate embeddings for semantic search |
| require_evidence_per_criterion | boolean |  |
| min_evidence_length | integer | Minimum characters for valid evidence |
| status | EvidenceMappingStatusEnum |  |
| created_by | string |  |


### PatchedEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| evidence_number | string |  |
| title | string |  |
| description | string |  |
| evidence_type | EvidenceEvidenceTypeEnum |  |
| file | string | Supported formats: PDF, Word, Excel, Text, Images |
| ner_entities | object | Named entities extracted: {entity: str, type: str, start: int, end: int} |
| status | EvidenceStatusEnum |  |
| tags | object | Custom tags for categorization |
| evidence_date | string | Date the evidence was created/issued |
| uploaded_by | integer |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |
| reviewer_notes | string |  |


### PatchedFeedbackCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_name | string |  |
| description | string |  |
| rubric_criterion | integer |  |
| excellent_feedback | string | Feedback for excellent performance |
| good_feedback | string | Feedback for good performance |
| satisfactory_feedback | string | Feedback for satisfactory performance |
| needs_improvement_feedback | string | Feedback for needs improvement |
| weight | number | Importance of this criterion |
| display_order | integer |  |


### PatchedFeedbackTemplateDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| tenant | string |  |
| created_by | integer |  |
| feedback_type | FeedbackTypeEnum |  |
| sentiment | Sentiment9ddEnum |  |
| tone | ToneEnum |  |
| rubric | integer |  |
| maps_to_criteria | object | List of rubric criterion IDs |
| include_student_name | boolean |  |
| include_strengths | boolean |  |
| include_improvements | boolean |  |
| include_next_steps | boolean |  |
| include_encouragement | boolean |  |
| opening_template | string | Opening statement template |
| strengths_template | string |  |
| improvements_template | string |  |
| next_steps_template | string |  |
| closing_template | string |  |
| positivity_level | integer | 1=Very Critical, 10=Very Positive |
| directness_level | integer | 1=Very Indirect, 10=Very Direct |
| formality_level | integer | 1=Very Casual, 10=Very Formal |
| status | Status118Enum |  |


### PatchedGeneratedFeedbackDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| assessment_title | string |  |
| score | number |  |
| max_score | number |  |
| grade | string |  |
| rubric_scores | object | Scores per rubric criterion |
| feedback_text | string |  |
| strengths_identified | any |  |
| improvements_identified | any |  |
| next_steps_suggested | any |  |
| reading_level | string | e.g., Grade 10, University |
| requires_review | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |
| delivered_at | string |  |
| delivery_method | string | email, LMS, portal, etc. |
| status | Status5d3Enum |  |


### PatchedGitHubActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| activity_type | GitHubActivityActivityTypeEnum |  |
| repository_name | string |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| last_updated | string |  |
| language | string |  |
| languages_used | any |  |
| topics | any |  |
| stars | integer |  |
| forks | integer |  |
| technologies | any |  |
| frameworks | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| commits_count | integer |  |
| contributions_count | integer |  |
| raw_data | any |  |
| verification_scan | integer |  |


### PatchedImprovementActionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| action_number | string |  |
| title | string |  |
| description | string | Detailed description of the improvement action |
| category | integer |  |
| priority | PriorityE88Enum |  |
| source | SourceA98Enum |  |
| status | Status354Enum |  |
| ai_classified_category | string | AI-suggested category based on content analysis |
| ai_classification_confidence | number | Confidence score (0.0-1.0) for AI classification |
| ai_summary | string | AI-generated summary of the action |
| ai_keywords | object | AI-extracted keywords from description |
| ai_related_standards | object | AI-identified ASQA standards related to this action |
| identified_date | string |  |
| planned_start_date | string |  |
| target_completion_date | string |  |
| actual_completion_date | string |  |
| responsible_person | integer |  |
| root_cause | string | Root cause analysis |
| proposed_solution | string |  |
| resources_required | string |  |
| estimated_cost | string |  |
| actual_cost | string |  |
| success_criteria | string | How to measure success |
| expected_impact | string |  |
| actual_impact | string | Post-implementation impact |
| effectiveness_rating | integer | Rating 1-5 after completion |
| is_critical_compliance | boolean | Critical for maintaining RTO registration |
| requires_approval | boolean |  |
| approved_by | integer |  |
| approved_at | string |  |
| tags | object | Custom tags for filtering |
| attachments | object | List of attachment URLs/metadata |
| created_by | integer |  |


### PatchedImprovementCategoryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| category_type | CategoryTypeEnum |  |
| description | string |  |
| color_code | string | Hex color code for UI display |
| related_standards | object | List of ASQA standard numbers this category relates to |
| is_active | boolean |  |


### PatchedImprovementReviewRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| review_number | string |  |
| title | string |  |
| review_type | ReviewTypeEnum |  |
| review_date | string |  |
| review_period_start | string |  |
| review_period_end | string |  |
| ai_summary | string | AI-generated summary of review findings |
| ai_trends | object | AI-identified trends and patterns |
| ai_recommendations | object | AI-generated recommendations |
| key_findings | string |  |
| areas_of_concern | string |  |
| recommendations | string |  |
| action_items | object | New actions arising from review |
| reviewed_by | integer |  |
| approved_by | integer |  |
| approved_at | string |  |
| notes | string |  |
| attachments | any |  |


### PatchedIntegrationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| integration_type | IntegrationTypeEnum |  |
| name | string |  |
| description | string |  |
| status | IntegrationStatusEnum |  |
| config | object | Integration-specific configuration |
| client_id | string |  |
| api_base_url | string |  |
| api_key | string |  |
| webhook_url | string |  |
| webhook_secret | string |  |
| auto_sync_enabled | boolean |  |
| sync_interval_minutes | integer |  |
| last_sync_status | string |  |
| last_sync_error | string |  |
| created_by | string |  |


### PatchedInterventionActionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| action_type | InterventionActionActionTypeEnum |  |
| description | string |  |
| priority | PriorityD67Enum |  |
| scheduled_date | string |  |
| completed_date | string |  |
| status | StatusF31Enum |  |
| assigned_to | integer |  |
| outcome_notes | string |  |
| effectiveness_rating | integer | Effectiveness rating (1-5) |
| created_by | integer |  |


### PatchedInterventionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| course_id | string |  |
| course_name | string |  |
| intervention_type | InterventionTypeEnum |  |
| priority_level | PriorityLevelD67Enum |  |
| status | Status65aEnum |  |
| trigger_type | TriggerTypeEnum |  |
| trigger_rule_id | string |  |
| trigger_details | any |  |
| action_description | string |  |
| action_taken_by | string |  |
| action_taken_by_role | string |  |
| action_date | string |  |
| communication_method | object |  |
| communication_notes | string |  |
| outcome_achieved | OutcomeAchievedEnum |  |
| outcome_description | string |  |
| outcome_evidence | any |  |
| requires_followup | boolean |  |
| followup_date | string |  |
| followup_notes | string |  |
| referred_to | string |  |
| referral_accepted | boolean |  |
| referral_date | string |  |
| completed_at | string |  |
| audit_notes | string |  |
| compliance_category | string |  |
| attachments | any |  |


### PatchedInterventionRuleRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| rule_name | string |  |
| description | string |  |
| is_active | boolean |  |
| priority | integer |  |
| condition_type | ConditionTypeEnum |  |
| conditions | any |  |
| intervention_type | string |  |
| priority_level | string |  |
| assigned_to_role | string |  |
| notify_staff | boolean |  |
| notification_recipients | any |  |
| notification_template | string |  |
| compliance_requirement | string |  |


### PatchedInterventionWorkflowRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| workflow_name | string |  |
| description | string |  |
| intervention_types | any |  |
| is_active | boolean |  |
| steps | any |  |
| requires_approval | boolean |  |
| approval_roles | any |  |
| required_documentation | any |  |
| compliance_standard | string |  |
| audit_requirements | any |  |


### PatchedJurisdictionRequirementRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| jurisdiction | JurisdictionEnum |  |
| name | string | Name of funding program (e.g., 'Smart and Skilled NSW') |
| code | string | Program code (e.g., 'SS-NSW', 'STS-VIC') |
| requires_australian_citizen | boolean |  |
| requires_permanent_resident | boolean |  |
| requires_jurisdiction_resident | boolean |  |
| min_jurisdiction_residency_months | integer | Minimum months of residency required |
| min_age | integer |  |
| max_age | integer |  |
| requires_year_12 | boolean |  |
| allows_year_10_completion | boolean |  |
| requires_unemployed | boolean |  |
| allows_employed | boolean |  |
| requires_apprentice_trainee | boolean |  |
| restricts_higher_qualifications | boolean | Student cannot have a higher qualification than what they're enrolling in |
| max_aqf_level | integer | Maximum AQF level student can already have |
| has_income_threshold | boolean |  |
| max_annual_income | string | Maximum annual income in AUD |
| allows_concession_card | boolean |  |
| allows_disability | boolean |  |
| allows_indigenous | boolean |  |
| priority_indigenous | boolean |  |
| funding_percentage | string | Percentage of course fees covered |
| student_contribution | string | Student contribution/co-payment amount in AUD |
| api_endpoint | string | External API endpoint for eligibility verification |
| api_key_required | boolean |  |
| additional_rules | object | Additional eligibility rules in JSON format |
| is_active | boolean |  |
| effective_from | string |  |
| effective_to | string |  |


### PatchedKnowledgeDocumentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| document_type | KnowledgeDocumentDocumentTypeEnum |  |
| subject | string |  |
| topic | string |  |
| content | string |  |
| summary | string |  |
| keywords | any |  |
| embedding_model | string |  |
| chunk_size | integer |  |
| chunks_count | integer |  |
| visibility | KnowledgeDocumentVisibilityEnum |  |
| course_ids | any |  |


### PatchedLMSActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| date | string |  |
| activity_type | LMSActivityActivityTypeEnum |  |
| activity_name | string |  |
| timestamp | string |  |
| duration_minutes | integer |  |
| completion_status | CompletionStatusEnum |  |
| interaction_count | integer | Number of clicks, views, or interactions |
| course_name | string |  |
| module_name | string |  |
| quality_score | string | Score for submissions, quiz results, etc. |


### PatchedLearningPathwayRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| pathway_name | string |  |
| description | string |  |
| difficulty_level | DifficultyLevelEnum |  |
| estimated_duration_hours | string |  |
| recommendation_confidence | string | Confidence score from collaborative filtering algorithm (0-100%) |
| similarity_score | string | Cosine similarity from embedding vectors (0-1) |
| status | LearningPathwayStatusEnum |  |
| total_steps | integer |  |
| completed_steps | integer |  |
| personalization_factors | object | Factors used for personalization: learning_style, pace, interests, prior_knowledge |
| similar_students | object | Student IDs with similar learning patterns (collaborative filtering) |
| started_at | string |  |
| completed_at | string |  |


### PatchedLearningStepRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| content_type | ContentTypeEnum |  |
| content_url | string |  |
| sequence_order | integer |  |
| is_prerequisite | boolean |  |
| prerequisites | [string] | Step numbers that must be completed first |
| estimated_minutes | integer |  |
| difficulty_rating | string | Difficulty rating 1-5 |
| learning_objectives | [string] |  |
| tags | [string] | Content tags for similarity matching |
| status | LearningStepStatusEnum |  |
| completion_score | string |  |
| started_at | string |  |
| completed_at | string |  |


### PatchedLinkedInActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| activity_type | LinkedInActivityActivityTypeEnum |  |
| title | string |  |
| description | string |  |
| url | string |  |
| activity_date | string |  |
| date_text | string |  |
| skills_mentioned | any |  |
| technologies | any |  |
| companies | any |  |
| keywords | any |  |
| relevance_score | number |  |
| is_industry_relevant | boolean |  |
| relevance_reasoning | string |  |
| raw_data | any |  |
| verification_scan | integer |  |


### PatchedMarkedResponseDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| response_text | string |  |
| requires_review | boolean |  |
| review_reason | string |  |
| automated_feedback | string |  |
| reviewer_notes | string |  |
| status | StatusFf6Enum |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |


### PatchedMarkingCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_name | string |  |
| description | string |  |
| expected_content | string | Expected content for this criterion |
| weight | number | Weight of this criterion (0.0-1.0) |
| max_points | integer |  |
| criterion_keywords | any |  |
| required | boolean | Is this criterion required? |
| display_order | integer |  |


### PatchedMessageTemplateRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| template_type | MessageTemplateTemplateTypeEnum |  |
| template_body | string |  |
| placeholders | any |  |
| default_tone | string |  |
| formality_level | integer |  |
| usage_count | integer |  |
| success_rate | number |  |
| last_used_at | string |  |
| is_active | boolean |  |
| is_system_template | boolean |  |
| created_by | string |  |


### PatchedMetadataVerificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| submission_analysis | integer |  |
| file_metadata | object | Complete file metadata (EXIF, document properties, etc.) |
| creation_timestamp | string |  |
| modification_timestamp | string |  |
| modification_history | object | History of file modifications |
| author_info | object | Author metadata from file (if available) |
| author_matches_student | boolean |  |
| anomalies_detected | object | List of detected metadata anomalies |


### PatchedMicroCredentialRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| code | string | Internal course code |
| description | string |  |
| duration_hours | integer | Total duration in hours |
| delivery_mode | MicroCredentialDeliveryModeEnum |  |
| target_audience | string |  |
| learning_outcomes | object | List of learning outcomes |
| source_units | object | List of units used: [{code, title, nominal_hours, elements}] |
| compressed_content | object | Compressed curriculum with key competencies and assessment tasks |
| tags | object | Searchable tags for categorization |
| skills_covered | object | List of specific skills |
| industry_sectors | object | Relevant industry sectors |
| aqf_level | string | Equivalent AQF level |
| assessment_strategy | string |  |
| assessment_tasks | object | List of assessment tasks with mapping to elements |
| price | string |  |
| max_participants | integer |  |
| prerequisites | string |  |
| status | Status204Enum |  |
| created_by | integer |  |
| published_at | string |  |


### PatchedModerationSessionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| assessment_type | ModerationSessionAssessmentTypeEnum |  |
| assessment_title | string |  |
| total_submissions | integer |  |
| assessors_count | integer |  |
| outlier_threshold | number | Standard deviations for outlier detection |
| bias_sensitivity | integer | Sensitivity level for bias detection (1=low, 10=high) |
| status | ModerationSessionStatusEnum |  |
| created_by | string |  |


### PatchedOutlierDetectionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| outlier_type | OutlierTypeEnum |  |
| severity | SeverityE88Enum |  |
| z_score | number | Standard deviations from mean |
| deviation_percentage | number | Percentage deviation from average |
| expected_score | number |  |
| actual_score | number |  |
| cohort_mean | number |  |
| cohort_std_dev | number |  |
| assessor_mean | number | Assessor's average score across all submissions |
| explanation | string |  |
| confidence_score | number | Confidence in outlier detection (0-1) |
| is_resolved | boolean |  |
| resolution_notes | string |  |
| resolved_by | string |  |
| resolved_at | string |  |
| session | integer |  |
| decision | integer |  |


### PatchedPDActivityRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| trainer_role | string |  |
| department | string |  |
| activity_type | ActivityType9adEnum |  |
| activity_title | string |  |
| description | string |  |
| provider | string |  |
| start_date | string |  |
| end_date | string |  |
| hours_completed | number |  |
| compliance_areas | any |  |
| industry_sectors | any |  |
| qualification_levels | any |  |
| evidence_type | object |  |
| evidence_files | any |  |
| verification_status | VerificationStatus901Enum |  |
| verified_by | string |  |
| verified_date | string |  |
| learning_outcomes | string |  |
| application_to_practice | string |  |
| reflection_notes | string |  |
| maintains_vocational_currency | boolean |  |
| maintains_industry_currency | boolean |  |
| maintains_teaching_currency | boolean |  |
| meets_asqa_requirements | boolean |  |
| compliance_notes | string |  |
| status | StatusF31Enum |  |


### PatchedPDSuggestionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| suggested_activity_type | string |  |
| activity_title | string |  |
| description | string |  |
| rationale | string |  |
| addresses_currency_gap | AddressesCurrencyGapEnum |  |
| priority_level | PriorityLevelF2aEnum |  |
| suggested_providers | any |  |
| estimated_hours | number |  |
| estimated_cost | number |  |
| suggested_timeframe | string |  |
| deadline | string |  |
| generated_by_model | string |  |
| prompt_used | string |  |
| confidence_score | number |  |
| status | Status251Enum |  |
| trainer_feedback | string |  |
| trainer_profile | integer |  |
| linked_activity | integer |  |


### PatchedPathwayRecommendationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| recommended_pathway | integer |  |
| algorithm_used | AlgorithmUsedEnum |  |
| recommendation_score | string | Overall recommendation score (0-1) |
| collaborative_score | string | Score from collaborative filtering |
| embedding_similarity | string | Cosine similarity from content embeddings |
| similar_students_count | integer |  |
| similar_students_list | [string] | Student IDs with similar learning patterns |
| common_pathways | [string] | Pathway numbers completed by similar students |
| recommendation_reasons | object | Human-readable reasons for recommendation |
| is_accepted | boolean |  |
| feedback_score | integer | User rating of recommendation (1-5) |
| expires_at | string | Recommendation expiry date |


### PatchedPlagiarismMatchRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| source_analysis | integer |  |
| matched_analysis | integer |  |
| similarity_score | number | Similarity score between submissions (0.0-1.0) |
| match_type | MatchTypeEnum |  |
| matched_text_segments | object | List of matched text segments with positions |
| matched_words_count | integer |  |
| matched_percentage | number | Percentage of text that matches |
| reviewed | boolean |  |
| false_positive | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |


### PatchedPolicyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| policy_number | string |  |
| title | string |  |
| description | string |  |
| policy_type | PolicyTypeEnum |  |
| content | string | Full policy content |
| version | string |  |
| status | PolicyStatusEnum |  |
| effective_date | string |  |
| review_date | string |  |
| file_path | string | Path to uploaded policy document |
| created_by | integer |  |


### PatchedQualificationMappingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| source_qualification_code | string |  |
| source_qualification_name | string |  |
| competency_areas | any |  |
| match_strength | number |  |
| match_confidence | number |  |
| equivalent_qualifications | any |  |
| superseded_by | string |  |
| supersedes | string |  |
| units_covered | any |  |
| units_partially_covered | any |  |
| mapping_source | string |  |
| verified | boolean |  |


### PatchedReferenceTableRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| namespace | string | Data namespace (e.g., 'vic.concessions') |
| version | string |  |
| data | object | Reference data as JSON |
| source | string | Data source URL or description |
| valid_from | string |  |
| valid_until | string |  |


### PatchedReplyHistoryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| final_reply_body | string |  |
| final_subject | string |  |
| time_to_first_draft_seconds | integer |  |
| time_to_send_seconds | integer |  |
| edit_count | integer |  |
| estimated_manual_time_seconds | integer |  |
| time_saved_seconds | integer |  |
| time_saved_percentage | number |  |
| sent_by | string |  |
| sent_at | string |  |
| student_responded | boolean |  |
| student_satisfied | boolean |  |
| follow_up_required | boolean |  |
| student_message | integer |  |
| draft_reply | integer |  |


### PatchedRiskAssessmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| dropout_probability | number | Predicted dropout probability (0.0 - 1.0) |
| risk_score | integer | Overall risk score (0-100) |
| engagement_score | number | Engagement level score |
| performance_score | number | Academic performance score |
| attendance_score | number | Attendance rate score |
| sentiment_score | number | Sentiment analysis score (-1.0 to 1.0) |
| model_version | string |  |
| confidence | number | Model confidence percentage |
| status | Status4c9Enum |  |
| alert_acknowledged | boolean |  |
| alert_acknowledged_by | integer |  |
| alert_acknowledged_at | string |  |
| intervention_assigned | boolean |  |
| intervention_notes | string |  |
| created_by | integer |  |


### PatchedRubricCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_number | string | e.g., 1, 1.1, A |
| title | string |  |
| description | string |  |
| weight | integer | Weight of this criterion |
| max_points | integer | Maximum points for this criterion |
| maps_to_elements | any |  |
| maps_to_performance_criteria | any |  |
| maps_to_knowledge_evidence | any |  |
| taxonomy_tags | object | Tags like "Bloom's: Apply", "SOLO: Relational" |
| blooms_level | string | Primary Bloom's level for this criterion |
| ai_generated | boolean |  |
| ai_rationale | string | Why this criterion was generated |
| nlp_keywords | object | NLP-extracted keywords |
| display_order | integer |  |


### PatchedRubricLevelRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| level_name | string | e.g., Excellent, Good, Satisfactory |
| level_type | object |  |
| points | integer | Points awarded for this level |
| description | string | What performance looks like at this level |
| indicators | object | Specific indicators of this performance level |
| examples | string | Example responses or work at this level |
| ai_generated | boolean |  |
| nlp_summary | string | NLP summary of level description |
| display_order | integer |  |


### PatchedRubricRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| rubric_type | RubricTypeEnum |  |
| status | StatusF38Enum |  |
| assessment | integer | Assessment this rubric is for |
| task | integer | Specific task this rubric is for (optional) |
| total_points | integer | Maximum points achievable |
| passing_score | integer | Minimum points to pass |
| nlp_summary | string | NLP-generated summary of rubric purpose |
| nlp_key_points | object | Extracted key assessment points |
| taxonomy_tags | object | Educational taxonomy tags (Bloom's, SOLO, etc.) |
| blooms_levels | object | Distribution of Bloom's levels in criteria |
| created_by | integer |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |
| approved_by | integer |  |
| approved_at | string |  |


### PatchedRulesetRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| version | string | Semantic version (e.g., 1.7.2) |
| jurisdiction_code | string |  |
| status | Status634Enum |  |
| description | string |  |
| changelog | string | Changes from previous version |
| created_by | integer |  |


### PatchedSLAPolicyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| target_days | integer | Target completion time in days |
| applies_to_priorities | object | List of priorities this policy applies to |
| applies_to_sources | object | List of source types this policy applies to |
| applies_to_categories | object | List of category IDs this policy applies to |
| warning_days_before | integer | Days before due date to trigger warning |
| escalate_on_breach | boolean | Auto-escalate when SLA is breached |
| escalation_recipients | object | User IDs to notify on escalation |
| is_active | boolean |  |


### PatchedStudentEngagementMetricRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| login_frequency | integer | Logins per week |
| time_on_platform | number | Hours per week |
| assignment_submission_rate | number | Assignment submission rate (%) |
| forum_participation | integer | Forum posts/comments count |
| peer_interaction_score | number | Peer interaction score |
| last_login | string |  |
| days_inactive | integer |  |
| activity_decline_rate | number | Week-over-week decline % |
| overall_engagement_score | number | Composite engagement score |


### PatchedStudentMessageRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_name | string |  |
| student_email | string |  |
| student_id | string |  |
| message_type | MessageTypeA94Enum |  |
| subject | string |  |
| message_body | string |  |
| received_date | string |  |
| priority | PriorityD67Enum |  |
| category | string |  |
| detected_sentiment | string |  |
| detected_topics | any |  |
| status | Status4e6Enum |  |
| requires_human_review | boolean |  |
| previous_message_count | integer |  |
| conversation_thread | integer |  |


### PatchedStudentProgressRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| pathway | integer |  |
| step | integer |  |
| time_spent_minutes | integer |  |
| attempts | integer |  |
| completion_score | string |  |
| struggle_indicators | object | Indicators of difficulty: multiple_attempts, extended_time, help_requests |
| engagement_level | EngagementLevelEnum |  |
| recommended_next_steps | [string] | Step numbers recommended based on performance |
| difficulty_adjustment | DifficultyAdjustmentEnum |  |
| is_completed | boolean |  |
| completed_at | string |  |


### PatchedSubmissionAnalysisRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| authenticity_check | integer |  |
| submission_id | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_content | string |  |
| content_embedding | object | 384-dimensional embedding vector for similarity comparison |
| plagiarism_score | number | Plagiarism similarity score (0.0-1.0) |
| metadata_verification_score | number | Metadata verification score (0-100) |
| anomaly_score | number | Anomaly detection score (0-100, higher is more suspicious) |
| combined_integrity_score | number | Combined integrity score (0-100) |
| plagiarism_detected | boolean |  |
| metadata_issues | boolean |  |
| anomalies_found | boolean |  |
| analysis_metadata | object | Additional analysis metadata (language, typing patterns, etc.) |


### PatchedSubmissionEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| submission_title | string |  |
| submission_type | string | e.g., PDF, DOCX, Video |
| file_path | string |  |
| file_size_bytes | integer |  |
| extracted_text | string | Full text extracted from submission |
| extraction_status | ExtractionStatusEnum |  |
| extraction_method | string | e.g., OCR, PDF parser, Speech-to-text |
| text_embedding | object | Vector embedding for semantic search |
| embedding_model | string | e.g., sentence-transformers |
| embedding_dimension | integer |  |
| metadata | object | Additional submission metadata (language, readability, keywords, etc.) |
| criteria_covered | object | List of criterion IDs with evidence |
| submitted_at | string |  |
| mapping | integer |  |


### PatchedTASRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| code | string | Qualification code (e.g., BSB50120) |
| description | string |  |
| qualification_name | string |  |
| aqf_level | AqfLevelEnum |  |
| training_package | string |  |
| template | integer |  |
| sections | object | Document sections with content |
| status | Status204Enum |  |
| is_current_version | boolean |  |
| gpt_generated | boolean |  |
| gpt_model_used | string | GPT model version used |
| gpt_tokens_used | integer |  |
| generation_time_seconds | number | Time taken to generate |
| content | object | Full document content including all sections |
| metadata | object | Additional metadata (units, assessments, etc.) |
| submitted_by | integer |  |
| reviewed_by | integer |  |
| approved_by | integer |  |
| created_by | integer |  |


### PatchedTASTemplateRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| template_type | TASTemplateTemplateTypeEnum |  |
| aqf_level | AqfLevelEnum |  |
| structure | object | Template structure with sections and GPT-4 prompts |
| default_sections | object | List of default sections to include |
| gpt_prompts | object | GPT-4 prompts for each section |
| is_active | boolean |  |
| is_system_template | boolean | System templates cannot be deleted |


### PatchedTaxonomyLabelRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| key | string | Label key (e.g., 'type:non-conformance') |
| name | string | Display name |
| description | string |  |
| color | string | Hex color code |
| icon | string | Icon identifier |
| category | string | Label category (type, origin, risk, etc.) |
| is_active | boolean |  |


### PatchedTenantAPIKeyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string | Key description |
| description | string | Optional description of key usage |
| is_active | boolean |  |
| expires_at | string |  |
| scopes | object | List of allowed scopes |


### PatchedTenantRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string | Organization name |
| slug | string | URL-safe identifier |
| domain | string | Custom domain (optional) |
| status | TenantStatusEnum |  |
| subscription_tier | SubscriptionTierEnum |  |
| contact_email | string |  |
| contact_name | string |  |
| contact_phone | string |  |
| registered_business_name | string | ASIC-registered business name |
| trading_name | string | Trading name (if different from registered name) |
| abn | string | Australian Business Number (11 digits) |
| acn | string | Australian Company Number (9 digits, required for companies) |
| business_structure | object | Legal structure of the business  * `sole_trader` - Sole Trader * `partnership` - Partnership * `company` - Company (Pty Ltd) * `trust` - Trust * `incorporated_association` - Incorporated Association |
| registered_address | string | Registered business address |
| postal_address | string | Postal address (if different from registered address) |
| billing_email | string |  |
| suspension_reason | string |  |
| settings | any |  |


### PatchedTenantUserRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| user | integer |  |
| role | RoleCadEnum |  |


### PatchedToneProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| tone_descriptor | string |  |
| formality_level | integer |  |
| empathy_level | integer |  |
| brevity_level | integer |  |
| use_contractions | boolean |  |
| use_emojis | boolean |  |
| greeting_style | string |  |
| closing_style | string |  |
| recommended_for | any |  |
| usage_count | integer |  |
| is_default | boolean |  |
| is_active | boolean |  |


### PatchedTrainerAssignmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| assignment_status | AssignmentStatusEnum |  |
| approved_by | string |  |
| approved_date | string |  |
| meets_requirements | boolean |  |
| compliance_score | number |  |
| gaps_identified | any |  |
| matching_qualifications | any |  |
| assignment_notes | string |  |
| rejection_reason | string |  |
| unit | integer |  |


### PatchedTrainerProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| email | string |  |
| linkedin_url | string |  |
| github_url | string |  |
| twitter_url | string |  |
| personal_website | string |  |
| primary_industry | string |  |
| specializations | any |  |
| years_experience | integer |  |
| last_verified_date | string |  |
| currency_status | CurrencyStatusEnum |  |
| currency_score | number |  |
| auto_verify_enabled | boolean |  |
| verification_frequency_days | integer |  |
| next_verification_date | string |  |


### PatchedTrainerQualificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| qualification_type | QualificationTypeEnum |  |
| qualification_code | string |  |
| qualification_name | string |  |
| issuing_organization | string |  |
| date_obtained | string |  |
| expiry_date | string |  |
| verification_status | TrainerQualificationVerificationStatusEnum |  |
| verification_document | string |  |
| competency_areas | any |  |
| units_covered | any |  |
| industry_experience_years | integer |  |
| recent_industry_work | boolean |  |


### PatchedTranscriptionJobRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| job_status | JobStatusEnum |  |
| transcription_engine | TranscriptionEngineEnum |  |
| language | string |  |
| enable_speaker_diarization | boolean |  |
| enable_punctuation | boolean |  |
| transcript_result | string |  |
| confidence_score | number |  |
| processing_time_seconds | number |  |
| error_message | string |  |
| retry_count | integer |  |
| max_retries | integer |  |
| audio_recording | integer |  |


### PatchedUnitOfCompetencyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| unit_code | string |  |
| unit_name | string |  |
| unit_type | UnitTypeEnum |  |
| qualification_code | string |  |
| required_qualifications | any |  |
| required_competency_areas | any |  |
| required_industry_experience | integer |  |
| requires_tae | boolean |  |
| requires_industry_currency | boolean |  |
| learning_outcomes | any |  |
| assessment_methods | any |  |
| technical_skills | any |  |
| prerequisite_units | any |  |
| related_units | any |  |


### PatchedUserProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### PatchedVerificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| outcome | VerificationOutcomeEnum |  |
| notes | string | Verification findings and observations |
| evidence_reviewed | object | List of evidence items reviewed |
| effectiveness_score | integer | Effectiveness rating 1-5 |
| requires_followup | boolean |  |
| followup_actions | string |  |
| followup_due_date | string |  |


### PatchedVerificationScanRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| scan_type | ScanTypeEnum |  |
| sources_to_scan | any |  |
| scan_status | ScanStatusEnum |  |
| total_items_found | integer |  |
| relevant_items_count | integer |  |
| currency_score | number |  |
| scan_duration_seconds | number |  |
| error_message | string |  |
| trainer_profile | integer |  |


### PatchedWebhookEndpointRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| target | TargetEnum |  |
| url | string |  |
| secret | string | HMAC secret for signing |
| events | object | Event types to send (e.g., ['decision.finalized', 'override.approved']) |
| active | boolean |  |


### PathwayRecommendation
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| recommendation_number | string |  |
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| recommended_pathway | integer |  |
| pathway_name | string |  |
| pathway_description | string |  |
| algorithm_used | AlgorithmUsedEnum |  |
| recommendation_score | string | Overall recommendation score (0-1) |
| collaborative_score | string | Score from collaborative filtering |
| embedding_similarity | string | Cosine similarity from content embeddings |
| similar_students_count | integer |  |
| similar_students_list | [string] | Student IDs with similar learning patterns |
| common_pathways | [string] | Pathway numbers completed by similar students |
| recommendation_reasons | object | Human-readable reasons for recommendation |
| is_accepted | boolean |  |
| feedback_score | integer | User rating of recommendation (1-5) |
| created_at | string |  |
| expires_at | string | Recommendation expiry date |


### PathwayRecommendationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| student_name | string |  |
| recommended_pathway | integer |  |
| algorithm_used | AlgorithmUsedEnum |  |
| recommendation_score | string | Overall recommendation score (0-1) |
| collaborative_score | string | Score from collaborative filtering |
| embedding_similarity | string | Cosine similarity from content embeddings |
| similar_students_count | integer |  |
| similar_students_list | [string] | Student IDs with similar learning patterns |
| common_pathways | [string] | Pathway numbers completed by similar students |
| recommendation_reasons | object | Human-readable reasons for recommendation |
| is_accepted | boolean |  |
| feedback_score | integer | User rating of recommendation (1-5) |
| expires_at | string | Recommendation expiry date |


### PeriodEnum
Type: `string`


### PlagiarismMatch
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| match_number | string |  |
| source_analysis | integer |  |
| matched_analysis | integer |  |
| similarity_score | number | Similarity score between submissions (0.0-1.0) |
| match_type | MatchTypeEnum |  |
| match_type_display | string |  |
| severity | object |  |
| severity_display | string |  |
| matched_text_segments | object | List of matched text segments with positions |
| matched_words_count | integer |  |
| matched_percentage | number | Percentage of text that matches |
| reviewed | boolean |  |
| false_positive | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |
| detected_at | string |  |


### PlagiarismMatchRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| source_analysis | integer |  |
| matched_analysis | integer |  |
| similarity_score | number | Similarity score between submissions (0.0-1.0) |
| match_type | MatchTypeEnum |  |
| matched_text_segments | object | List of matched text segments with positions |
| matched_words_count | integer |  |
| matched_percentage | number | Percentage of text that matches |
| reviewed | boolean |  |
| false_positive | boolean |  |
| review_notes | string |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |


### Policy
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| policy_number | string |  |
| title | string |  |
| description | string |  |
| policy_type | PolicyTypeEnum |  |
| policy_type_display | string |  |
| content | string | Full policy content |
| version | string |  |
| status | PolicyStatusEnum |  |
| status_display | string |  |
| effective_date | string |  |
| review_date | string |  |
| last_compared_at | string |  |
| compliance_score | number | Overall compliance score (0-100) |
| file_path | string | Path to uploaded policy document |
| created_by | integer |  |
| created_by_details | object |  |
| created_at | string |  |
| updated_at | string |  |
| comparison_count | string |  |
| compliance_status | string |  |


### PolicyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| policy_number | string |  |
| title | string |  |
| description | string |  |
| policy_type | PolicyTypeEnum |  |
| content | string | Full policy content |
| version | string |  |
| status | PolicyStatusEnum |  |
| effective_date | string |  |
| review_date | string |  |
| file_path | string | Path to uploaded policy document |
| created_by | integer |  |


### PolicyStatusEnum
Type: `string`


### PolicyTypeEnum
Type: `string`


### PrimaryEmotionEnum
Type: `string`


### PriorityD67Enum
Type: `string`


### PriorityE88Enum
Type: `string`


### PriorityLevelD67Enum
Type: `string`


### PriorityLevelF2aEnum
Type: `string`


### ProcessingStatusEnum
Type: `string`


### QualificationMapping
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| mapping_id | string |  |
| tenant | string |  |
| source_qualification_code | string |  |
| source_qualification_name | string |  |
| competency_areas | any |  |
| match_strength | number |  |
| match_confidence | number |  |
| equivalent_qualifications | any |  |
| superseded_by | string |  |
| supersedes | string |  |
| units_covered | any |  |
| units_partially_covered | any |  |
| mapping_source | string |  |
| verified | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### QualificationMappingRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| source_qualification_code | string |  |
| source_qualification_name | string |  |
| competency_areas | any |  |
| match_strength | number |  |
| match_confidence | number |  |
| equivalent_qualifications | any |  |
| superseded_by | string |  |
| supersedes | string |  |
| units_covered | any |  |
| units_partially_covered | any |  |
| mapping_source | string |  |
| verified | boolean |  |


### QualificationTypeEnum
Type: `string`


### ReferenceTable
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| namespace | string | Data namespace (e.g., 'vic.concessions') |
| version | string |  |
| data | object | Reference data as JSON |
| source | string | Data source URL or description |
| checksum | string | SHA256 of data |
| valid_from | string |  |
| valid_until | string |  |
| created_at | string |  |
| updated_at | string |  |


### ReferenceTableRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| namespace | string | Data namespace (e.g., 'vic.concessions') |
| version | string |  |
| data | object | Reference data as JSON |
| source | string | Data source URL or description |
| valid_from | string |  |
| valid_until | string |  |


### RegulatorySourceEnum
Type: `string`


### ReplyHistory
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| history_number | string |  |
| final_reply_body | string |  |
| final_subject | string |  |
| time_to_first_draft_seconds | integer |  |
| time_to_send_seconds | integer |  |
| edit_count | integer |  |
| estimated_manual_time_seconds | integer |  |
| time_saved_seconds | integer |  |
| time_saved_percentage | number |  |
| sent_by | string |  |
| sent_at | string |  |
| student_responded | boolean |  |
| student_satisfied | boolean |  |
| follow_up_required | boolean |  |
| created_at | string |  |
| student_message | integer |  |
| draft_reply | integer |  |


### ReplyHistoryRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| final_reply_body | string |  |
| final_subject | string |  |
| time_to_first_draft_seconds | integer |  |
| time_to_send_seconds | integer |  |
| edit_count | integer |  |
| estimated_manual_time_seconds | integer |  |
| time_saved_seconds | integer |  |
| time_saved_percentage | number |  |
| sent_by | string |  |
| sent_at | string |  |
| student_responded | boolean |  |
| student_satisfied | boolean |  |
| follow_up_required | boolean |  |
| student_message | integer |  |
| draft_reply | integer |  |


### RequirementTypeEnum
Type: `string`


### ReviewTypeEnum
Type: `string`


### RiskAssessment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| assessment_number | string |  |
| student_id | string |  |
| student_name | string |  |
| dropout_probability | number | Predicted dropout probability (0.0 - 1.0) |
| risk_level | object |  |
| risk_score | integer | Overall risk score (0-100) |
| engagement_score | number | Engagement level score |
| performance_score | number | Academic performance score |
| attendance_score | number | Attendance rate score |
| sentiment_score | number | Sentiment analysis score (-1.0 to 1.0) |
| model_version | string |  |
| confidence | number | Model confidence percentage |
| status | Status4c9Enum |  |
| assessment_date | string |  |
| last_updated | string |  |
| alert_triggered | boolean |  |
| alert_acknowledged | boolean |  |
| alert_acknowledged_by | integer |  |
| alert_acknowledged_by_name | string |  |
| alert_acknowledged_at | string |  |
| intervention_assigned | boolean |  |
| intervention_notes | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| created_at | string |  |
| risk_factors | [RiskFactor] |  |
| sentiment_analyses | [SentimentAnalysis] |  |
| interventions | [InterventionAction] |  |


### RiskAssessmentList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| assessment_number | string |  |
| student_id | string |  |
| student_name | string |  |
| dropout_probability | number | Predicted dropout probability (0.0 - 1.0) |
| risk_level | RiskLevel623Enum |  |
| risk_score | integer | Overall risk score (0-100) |
| confidence | number | Model confidence percentage |
| status | Status4c9Enum |  |
| assessment_date | string |  |
| alert_triggered | boolean |  |
| alert_acknowledged | boolean |  |
| intervention_assigned | boolean |  |
| created_by_name | string |  |
| risk_factor_count | string |  |
| intervention_count | string |  |


### RiskAssessmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| dropout_probability | number | Predicted dropout probability (0.0 - 1.0) |
| risk_score | integer | Overall risk score (0-100) |
| engagement_score | number | Engagement level score |
| performance_score | number | Academic performance score |
| attendance_score | number | Attendance rate score |
| sentiment_score | number | Sentiment analysis score (-1.0 to 1.0) |
| model_version | string |  |
| confidence | number | Model confidence percentage |
| status | Status4c9Enum |  |
| alert_acknowledged | boolean |  |
| alert_acknowledged_by | integer |  |
| alert_acknowledged_at | string |  |
| intervention_assigned | boolean |  |
| intervention_notes | string |  |
| created_by | integer |  |


### RiskFactor
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| factor_number | string |  |
| factor_type | FactorTypeEnum |  |
| factor_name | string |  |
| description | string |  |
| weight | number | Factor weight in model (0.0 - 1.0) |
| contribution | number | Contribution to overall risk (%) |
| severity | SeverityE88Enum |  |
| current_value | number | Current measured value |
| threshold_value | number | Risk threshold value |
| threshold_exceeded | boolean |  |
| trend | TrendEnum |  |
| created_at | string |  |


### RiskFactorRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| factor_type | FactorTypeEnum |  |
| factor_name | string |  |
| description | string |  |
| weight | number | Factor weight in model (0.0 - 1.0) |
| contribution | number | Contribution to overall risk (%) |
| severity | SeverityE88Enum |  |
| current_value | number | Current measured value |
| threshold_value | number | Risk threshold value |
| trend | TrendEnum |  |


### RiskLevel623Enum
Type: `string`


### RoleCadEnum
Type: `string`


### Rubric
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| rubric_number | string |  |
| title | string |  |
| description | string |  |
| rubric_type | RubricTypeEnum |  |
| rubric_type_display | string |  |
| status | StatusF38Enum |  |
| status_display | string |  |
| assessment | integer | Assessment this rubric is for |
| assessment_title | string |  |
| task | integer | Specific task this rubric is for (optional) |
| task_question | string |  |
| total_points | integer | Maximum points achievable |
| passing_score | integer | Minimum points to pass |
| ai_generated | boolean |  |
| ai_model | string |  |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| nlp_summary | string | NLP-generated summary of rubric purpose |
| nlp_key_points | object | Extracted key assessment points |
| taxonomy_tags | object | Educational taxonomy tags (Bloom's, SOLO, etc.) |
| blooms_levels | object | Distribution of Bloom's levels in criteria |
| criterion_count | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| created_at | string |  |
| updated_at | string |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| approved_by | integer |  |
| approved_by_name | string |  |
| approved_at | string |  |


### RubricCriterion
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| criterion_number | string | e.g., 1, 1.1, A |
| title | string |  |
| description | string |  |
| weight | integer | Weight of this criterion |
| max_points | integer | Maximum points for this criterion |
| maps_to_elements | any |  |
| maps_to_performance_criteria | any |  |
| maps_to_knowledge_evidence | any |  |
| taxonomy_tags | object | Tags like "Bloom's: Apply", "SOLO: Relational" |
| blooms_level | string | Primary Bloom's level for this criterion |
| blooms_level_display | string |  |
| ai_generated | boolean |  |
| ai_rationale | string | Why this criterion was generated |
| nlp_keywords | object | NLP-extracted keywords |
| display_order | integer |  |
| levels | [RubricLevel] |  |


### RubricCriterionRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| criterion_number | string | e.g., 1, 1.1, A |
| title | string |  |
| description | string |  |
| weight | integer | Weight of this criterion |
| max_points | integer | Maximum points for this criterion |
| maps_to_elements | any |  |
| maps_to_performance_criteria | any |  |
| maps_to_knowledge_evidence | any |  |
| taxonomy_tags | object | Tags like "Bloom's: Apply", "SOLO: Relational" |
| blooms_level | string | Primary Bloom's level for this criterion |
| ai_generated | boolean |  |
| ai_rationale | string | Why this criterion was generated |
| nlp_keywords | object | NLP-extracted keywords |
| display_order | integer |  |


### RubricDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| rubric_number | string |  |
| title | string |  |
| description | string |  |
| rubric_type | RubricTypeEnum |  |
| rubric_type_display | string |  |
| status | StatusF38Enum |  |
| status_display | string |  |
| assessment | integer | Assessment this rubric is for |
| assessment_title | string |  |
| task | integer | Specific task this rubric is for (optional) |
| task_question | string |  |
| total_points | integer | Maximum points achievable |
| passing_score | integer | Minimum points to pass |
| ai_generated | boolean |  |
| ai_model | string |  |
| ai_generation_time | number | Generation time in seconds |
| ai_generated_at | string |  |
| nlp_summary | string | NLP-generated summary of rubric purpose |
| nlp_key_points | object | Extracted key assessment points |
| taxonomy_tags | object | Educational taxonomy tags (Bloom's, SOLO, etc.) |
| blooms_levels | object | Distribution of Bloom's levels in criteria |
| criterion_count | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| created_at | string |  |
| updated_at | string |  |
| reviewed_by | integer |  |
| reviewed_by_name | string |  |
| reviewed_at | string |  |
| approved_by | integer |  |
| approved_by_name | string |  |
| approved_at | string |  |
| criteria | [RubricCriterion] |  |


### RubricLevel
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| level_name | string | e.g., Excellent, Good, Satisfactory |
| level_type | object |  |
| level_type_display | string |  |
| points | integer | Points awarded for this level |
| description | string | What performance looks like at this level |
| indicators | object | Specific indicators of this performance level |
| examples | string | Example responses or work at this level |
| ai_generated | boolean |  |
| nlp_summary | string | NLP summary of level description |
| display_order | integer |  |


### RubricLevelRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| level_name | string | e.g., Excellent, Good, Satisfactory |
| level_type | object |  |
| points | integer | Points awarded for this level |
| description | string | What performance looks like at this level |
| indicators | object | Specific indicators of this performance level |
| examples | string | Example responses or work at this level |
| ai_generated | boolean |  |
| nlp_summary | string | NLP summary of level description |
| display_order | integer |  |


### RubricRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| title | string |  |
| description | string |  |
| rubric_type | RubricTypeEnum |  |
| status | StatusF38Enum |  |
| assessment | integer | Assessment this rubric is for |
| task | integer | Specific task this rubric is for (optional) |
| total_points | integer | Maximum points achievable |
| passing_score | integer | Minimum points to pass |
| nlp_summary | string | NLP-generated summary of rubric purpose |
| nlp_key_points | object | Extracted key assessment points |
| taxonomy_tags | object | Educational taxonomy tags (Bloom's, SOLO, etc.) |
| blooms_levels | object | Distribution of Bloom's levels in criteria |
| created_by | integer |  |
| reviewed_by | integer |  |
| reviewed_at | string |  |
| approved_by | integer |  |
| approved_at | string |  |


### RubricTypeEnum
Type: `string`


### RuleTypeEnum
Type: `string`


### Ruleset
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| version | string | Semantic version (e.g., 1.7.2) |
| jurisdiction_code | string |  |
| status | Status634Enum |  |
| checksum | string | SHA256 of rule content |
| description | string |  |
| changelog | string | Changes from previous version |
| artifacts | [RulesetArtifact] |  |
| created_by | integer |  |
| created_by_details | object |  |
| created_at | string |  |
| activated_at | string |  |
| retired_at | string |  |


### RulesetArtifact
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| type | RulesetArtifactTypeEnum |  |
| name | string | Artifact name/identifier |
| blob | string | Rule content |
| description | string |  |
| created_at | string |  |


### RulesetArtifactRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| type | RulesetArtifactTypeEnum |  |
| name | string | Artifact name/identifier |
| blob | string | Rule content |
| description | string |  |


### RulesetArtifactTypeEnum
Type: `string`


### RulesetMinimal
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| version | string | Semantic version (e.g., 1.7.2) |
| jurisdiction_code | string |  |
| status | Status634Enum |  |


### RulesetMinimalRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| version | string | Semantic version (e.g., 1.7.2) |
| jurisdiction_code | string |  |
| status | Status634Enum |  |


### RulesetRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| version | string | Semantic version (e.g., 1.7.2) |
| jurisdiction_code | string |  |
| status | Status634Enum |  |
| description | string |  |
| changelog | string | Changes from previous version |
| created_by | integer |  |


### SLAPolicy
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| name | string |  |
| description | string |  |
| target_days | integer | Target completion time in days |
| applies_to_priorities | object | List of priorities this policy applies to |
| applies_to_sources | object | List of source types this policy applies to |
| applies_to_categories | object | List of category IDs this policy applies to |
| warning_days_before | integer | Days before due date to trigger warning |
| escalate_on_breach | boolean | Auto-escalate when SLA is breached |
| escalation_recipients | object | User IDs to notify on escalation |
| is_active | boolean |  |
| created_at | string |  |
| created_by | integer |  |
| created_by_name | string |  |
| updated_at | string |  |
| applicable_actions_count | string |  |


### SLAPolicyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| target_days | integer | Target completion time in days |
| applies_to_priorities | object | List of priorities this policy applies to |
| applies_to_sources | object | List of source types this policy applies to |
| applies_to_categories | object | List of category IDs this policy applies to |
| warning_days_before | integer | Days before due date to trigger warning |
| escalate_on_breach | boolean | Auto-escalate when SLA is breached |
| escalation_recipients | object | User IDs to notify on escalation |
| is_active | boolean |  |


### ScanStatusEnum
Type: `string`


### ScanTypeEnum
Type: `string`


### SearchTypeEnum
Type: `string`


### Sentiment9ddEnum
Type: `string`


### SentimentAnalysis
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| analysis_number | string |  |
| source_type | SentimentAnalysisSourceTypeEnum |  |
| text_sample | string | Sample text analyzed |
| sentiment_score | number | Sentiment score (-1.0 = very negative, 1.0 = very positive) |
| sentiment_label | object |  |
| confidence | number | Sentiment model confidence |
| frustration_detected | boolean |  |
| stress_detected | boolean |  |
| confusion_detected | boolean |  |
| disengagement_detected | boolean |  |
| negative_keywords | any |  |
| risk_indicators | any |  |
| analysis_date | string |  |


### SentimentAnalysisRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| source_type | SentimentAnalysisSourceTypeEnum |  |
| text_sample | string | Sample text analyzed |
| sentiment_score | number | Sentiment score (-1.0 = very negative, 1.0 = very positive) |
| confidence | number | Sentiment model confidence |
| frustration_detected | boolean |  |
| stress_detected | boolean |  |
| confusion_detected | boolean |  |
| disengagement_detected | boolean |  |
| negative_keywords | any |  |
| risk_indicators | any |  |


### SentimentAnalysisSourceTypeEnum
Type: `string`


### SentimentLabelEnum
Type: `string`


### SentimentTrendEnum
Type: `string`


### SessionTypeEnum
Type: `string`


### SeverityE88Enum
Type: `string`


### SimilarityModelEnum
Type: `string`


### SourceA98Enum
Type: `string`


### StandardTypeEnum
Type: `string`


### Status118Enum
Type: `string`


### Status204Enum
Type: `string`


### Status24eEnum
Type: `string`


### Status251Enum
Type: `string`


### Status304Enum
Type: `string`


### Status354Enum
Type: `string`


### Status4c9Enum
Type: `string`


### Status4e6Enum
Type: `string`


### Status5d3Enum
Type: `string`


### Status5f9Enum
Type: `string`


### Status634Enum
Type: `string`


### Status65aEnum
Type: `string`


### Status86cEnum
Type: `string`


### Status9adEnum
Type: `string`


### StatusA8fEnum
Type: `string`


### StatusE22Enum
Type: `string`


### StatusF31Enum
Type: `string`


### StatusF38Enum
Type: `string`


### StatusF84Enum
Type: `string`


### StatusFf6Enum
Type: `string`


### StudentEngagementMetric
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| metric_number | string |  |
| student_id | string |  |
| student_name | string |  |
| login_frequency | integer | Logins per week |
| time_on_platform | number | Hours per week |
| assignment_submission_rate | number | Assignment submission rate (%) |
| forum_participation | integer | Forum posts/comments count |
| peer_interaction_score | number | Peer interaction score |
| last_login | string |  |
| days_inactive | integer |  |
| activity_decline_rate | number | Week-over-week decline % |
| overall_engagement_score | number | Composite engagement score |
| measurement_date | string |  |
| created_at | string |  |


### StudentEngagementMetricRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| login_frequency | integer | Logins per week |
| time_on_platform | number | Hours per week |
| assignment_submission_rate | number | Assignment submission rate (%) |
| forum_participation | integer | Forum posts/comments count |
| peer_interaction_score | number | Peer interaction score |
| last_login | string |  |
| days_inactive | integer |  |
| activity_decline_rate | number | Week-over-week decline % |
| overall_engagement_score | number | Composite engagement score |


### StudentMessage
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| drafts_count | string |  |
| message_number | string |  |
| tenant | string |  |
| student_name | string |  |
| student_email | string |  |
| student_id | string |  |
| message_type | MessageTypeA94Enum |  |
| subject | string |  |
| message_body | string |  |
| received_date | string |  |
| priority | PriorityD67Enum |  |
| category | string |  |
| detected_sentiment | string |  |
| detected_topics | any |  |
| status | Status4e6Enum |  |
| requires_human_review | boolean |  |
| previous_message_count | integer |  |
| created_at | string |  |
| updated_at | string |  |
| conversation_thread | integer |  |


### StudentMessageList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| message_number | string |  |
| student_name | string |  |
| subject | string |  |
| message_type | MessageTypeA94Enum |  |
| priority | PriorityD67Enum |  |
| status | Status4e6Enum |  |
| received_date | string |  |
| detected_sentiment | string |  |


### StudentMessageListRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_name | string |  |
| subject | string |  |
| message_type | MessageTypeA94Enum |  |
| priority | PriorityD67Enum |  |
| status | Status4e6Enum |  |
| received_date | string |  |
| detected_sentiment | string |  |


### StudentMessageRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_name | string |  |
| student_email | string |  |
| student_id | string |  |
| message_type | MessageTypeA94Enum |  |
| subject | string |  |
| message_body | string |  |
| received_date | string |  |
| priority | PriorityD67Enum |  |
| category | string |  |
| detected_sentiment | string |  |
| detected_topics | any |  |
| status | Status4e6Enum |  |
| requires_human_review | boolean |  |
| previous_message_count | integer |  |
| conversation_thread | integer |  |


### StudentProgress
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| progress_number | string |  |
| tenant | string |  |
| student_id | string |  |
| pathway | integer |  |
| pathway_name | string |  |
| step | integer |  |
| step_title | string |  |
| time_spent_minutes | integer |  |
| attempts | integer |  |
| completion_score | string |  |
| struggle_indicators | object | Indicators of difficulty: multiple_attempts, extended_time, help_requests |
| engagement_level | EngagementLevelEnum |  |
| recommended_next_steps | [string] | Step numbers recommended based on performance |
| difficulty_adjustment | DifficultyAdjustmentEnum |  |
| is_completed | boolean |  |
| completed_at | string |  |
| started_at | string |  |
| last_activity | string |  |


### StudentProgressRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| student_id | string |  |
| pathway | integer |  |
| step | integer |  |
| time_spent_minutes | integer |  |
| attempts | integer |  |
| completion_score | string |  |
| struggle_indicators | object | Indicators of difficulty: multiple_attempts, extended_time, help_requests |
| engagement_level | EngagementLevelEnum |  |
| recommended_next_steps | [string] | Step numbers recommended based on performance |
| difficulty_adjustment | DifficultyAdjustmentEnum |  |
| is_completed | boolean |  |
| completed_at | string |  |


### SubmissionAnalysis
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| analysis_number | string |  |
| authenticity_check | integer |  |
| submission_id | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_content | string |  |
| content_hash | string |  |
| word_count | integer |  |
| character_count | integer |  |
| content_embedding | object | 384-dimensional embedding vector for similarity comparison |
| plagiarism_score | number | Plagiarism similarity score (0.0-1.0) |
| metadata_verification_score | number | Metadata verification score (0-100) |
| anomaly_score | number | Anomaly detection score (0-100, higher is more suspicious) |
| combined_integrity_score | number | Combined integrity score (0-100) |
| integrity_status | object |  |
| integrity_status_display | string |  |
| plagiarism_detected | boolean |  |
| metadata_issues | boolean |  |
| anomalies_found | boolean |  |
| analysis_metadata | object | Additional analysis metadata (language, typing patterns, etc.) |
| analyzed_at | string |  |
| plagiarism_matches_source | [PlagiarismMatch] |  |
| plagiarism_matches_matched | [PlagiarismMatch] |  |
| metadata_verifications | [MetadataVerification] |  |
| anomaly_detections | [AnomalyDetection] |  |


### SubmissionAnalysisList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| analysis_number | string |  |
| submission_id | string |  |
| student_id | string |  |
| student_name | string |  |
| word_count | integer |  |
| plagiarism_score | number | Plagiarism similarity score (0.0-1.0) |
| metadata_verification_score | number | Metadata verification score (0-100) |
| anomaly_score | number | Anomaly detection score (0-100, higher is more suspicious) |
| combined_integrity_score | number | Combined integrity score (0-100) |
| integrity_status | IntegrityStatusEnum |  |
| integrity_status_display | string |  |
| plagiarism_detected | boolean |  |
| metadata_issues | boolean |  |
| anomalies_found | boolean |  |
| analyzed_at | string |  |


### SubmissionAnalysisListRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| submission_id | string |  |
| student_id | string |  |
| student_name | string |  |
| word_count | integer |  |
| plagiarism_score | number | Plagiarism similarity score (0.0-1.0) |
| metadata_verification_score | number | Metadata verification score (0-100) |
| anomaly_score | number | Anomaly detection score (0-100, higher is more suspicious) |
| combined_integrity_score | number | Combined integrity score (0-100) |
| integrity_status | IntegrityStatusEnum |  |
| plagiarism_detected | boolean |  |
| metadata_issues | boolean |  |
| anomalies_found | boolean |  |


### SubmissionAnalysisRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| authenticity_check | integer |  |
| submission_id | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_content | string |  |
| content_embedding | object | 384-dimensional embedding vector for similarity comparison |
| plagiarism_score | number | Plagiarism similarity score (0.0-1.0) |
| metadata_verification_score | number | Metadata verification score (0-100) |
| anomaly_score | number | Anomaly detection score (0-100, higher is more suspicious) |
| combined_integrity_score | number | Combined integrity score (0-100) |
| plagiarism_detected | boolean |  |
| metadata_issues | boolean |  |
| anomalies_found | boolean |  |
| analysis_metadata | object | Additional analysis metadata (language, typing patterns, etc.) |


### SubmissionEvidence
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| evidence_number | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| submission_title | string |  |
| submission_type | string | e.g., PDF, DOCX, Video |
| file_path | string |  |
| file_size_bytes | integer |  |
| extracted_text | string | Full text extracted from submission |
| text_length | integer |  |
| extraction_status | ExtractionStatusEnum |  |
| extraction_method | string | e.g., OCR, PDF parser, Speech-to-text |
| text_embedding | object | Vector embedding for semantic search |
| embedding_model | string | e.g., sentence-transformers |
| embedding_dimension | integer |  |
| metadata | object | Additional submission metadata (language, readability, keywords, etc.) |
| total_tags | integer |  |
| criteria_covered | object | List of criterion IDs with evidence |
| submitted_at | string |  |
| extracted_at | string |  |
| created_at | string |  |
| mapping | integer |  |


### SubmissionEvidenceDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tags | string |  |
| evidence_number | string |  |
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| submission_title | string |  |
| submission_type | string | e.g., PDF, DOCX, Video |
| file_path | string |  |
| file_size_bytes | integer |  |
| extracted_text | string | Full text extracted from submission |
| text_length | integer |  |
| extraction_status | ExtractionStatusEnum |  |
| extraction_method | string | e.g., OCR, PDF parser, Speech-to-text |
| text_embedding | object | Vector embedding for semantic search |
| embedding_model | string | e.g., sentence-transformers |
| embedding_dimension | integer |  |
| metadata | object | Additional submission metadata (language, readability, keywords, etc.) |
| total_tags | integer |  |
| criteria_covered | object | List of criterion IDs with evidence |
| submitted_at | string |  |
| extracted_at | string |  |
| created_at | string |  |
| mapping | integer |  |


### SubmissionEvidenceRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| student_id | string |  |
| student_name | string |  |
| submission_id | string |  |
| submission_title | string |  |
| submission_type | string | e.g., PDF, DOCX, Video |
| file_path | string |  |
| file_size_bytes | integer |  |
| extracted_text | string | Full text extracted from submission |
| extraction_status | ExtractionStatusEnum |  |
| extraction_method | string | e.g., OCR, PDF parser, Speech-to-text |
| text_embedding | object | Vector embedding for semantic search |
| embedding_model | string | e.g., sentence-transformers |
| embedding_dimension | integer |  |
| metadata | object | Additional submission metadata (language, readability, keywords, etc.) |
| criteria_covered | object | List of criterion IDs with evidence |
| submitted_at | string |  |
| mapping | integer |  |


### SubscriptionTierEnum
Type: `string`


### TAS
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| title | string |  |
| code | string | Qualification code (e.g., BSB50120) |
| description | string |  |
| qualification_name | string |  |
| aqf_level | AqfLevelEnum |  |
| aqf_level_display | string |  |
| training_package | string |  |
| template | integer |  |
| template_details | object |  |
| sections | object | Document sections with content |
| status | Status204Enum |  |
| status_display | string |  |
| version | integer |  |
| is_current_version | boolean |  |
| gpt_generated | boolean |  |
| gpt_generation_date | string |  |
| gpt_model_used | string | GPT model version used |
| gpt_tokens_used | integer |  |
| generation_time_seconds | number | Time taken to generate |
| content | object | Full document content including all sections |
| metadata | object | Additional metadata (units, assessments, etc.) |
| submitted_for_review_at | string |  |
| submitted_by | integer |  |
| submitted_by_details | object |  |
| reviewed_at | string |  |
| reviewed_by | integer |  |
| reviewed_by_details | object |  |
| approved_at | string |  |
| approved_by | integer |  |
| approved_by_details | object |  |
| published_at | string |  |
| created_by | integer |  |
| created_by_details | object |  |
| created_at | string |  |
| updated_at | string |  |
| time_saved | string |  |
| version_count | string |  |


### TASRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| title | string |  |
| code | string | Qualification code (e.g., BSB50120) |
| description | string |  |
| qualification_name | string |  |
| aqf_level | AqfLevelEnum |  |
| training_package | string |  |
| template | integer |  |
| sections | object | Document sections with content |
| status | Status204Enum |  |
| is_current_version | boolean |  |
| gpt_generated | boolean |  |
| gpt_model_used | string | GPT model version used |
| gpt_tokens_used | integer |  |
| generation_time_seconds | number | Time taken to generate |
| content | object | Full document content including all sections |
| metadata | object | Additional metadata (units, assessments, etc.) |
| submitted_by | integer |  |
| reviewed_by | integer |  |
| approved_by | integer |  |
| created_by | integer |  |


### TASTemplate
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| name | string |  |
| description | string |  |
| template_type | TASTemplateTemplateTypeEnum |  |
| template_type_display | string |  |
| aqf_level | AqfLevelEnum |  |
| aqf_level_display | string |  |
| structure | object | Template structure with sections and GPT-4 prompts |
| default_sections | object | List of default sections to include |
| gpt_prompts | object | GPT-4 prompts for each section |
| is_active | boolean |  |
| is_system_template | boolean | System templates cannot be deleted |
| created_by | integer |  |
| created_by_details | object |  |
| created_at | string |  |
| updated_at | string |  |


### TASTemplateRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string |  |
| description | string |  |
| template_type | TASTemplateTemplateTypeEnum |  |
| aqf_level | AqfLevelEnum |  |
| structure | object | Template structure with sections and GPT-4 prompts |
| default_sections | object | List of default sections to include |
| gpt_prompts | object | GPT-4 prompts for each section |
| is_active | boolean |  |
| is_system_template | boolean | System templates cannot be deleted |


### TASTemplateTemplateTypeEnum
Type: `string`


### TagTypeEnum
Type: `string`


### TargetEnum
Type: `string`


### TaxonomyLabel
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| key | string | Label key (e.g., 'type:non-conformance') |
| name | string | Display name |
| description | string |  |
| color | string | Hex color code |
| icon | string | Icon identifier |
| category | string | Label category (type, origin, risk, etc.) |
| is_active | boolean |  |
| created_at | string |  |


### TaxonomyLabelRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| key | string | Label key (e.g., 'type:non-conformance') |
| name | string | Display name |
| description | string |  |
| color | string | Hex color code |
| icon | string | Icon identifier |
| category | string | Label category (type, origin, risk, etc.) |
| is_active | boolean |  |


### Tenant
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | string |  |
| name | string | Organization name |
| slug | string | URL-safe identifier |
| domain | string | Custom domain (optional) |
| status | TenantStatusEnum |  |
| subscription_tier | SubscriptionTierEnum |  |
| contact_email | string |  |
| contact_name | string |  |
| contact_phone | string |  |
| registered_business_name | string | ASIC-registered business name |
| trading_name | string | Trading name (if different from registered name) |
| abn | string | Australian Business Number (11 digits) |
| acn | string | Australian Company Number (9 digits, required for companies) |
| business_structure | object | Legal structure of the business  * `sole_trader` - Sole Trader * `partnership` - Partnership * `company` - Company (Pty Ltd) * `trust` - Trust * `incorporated_association` - Incorporated Association |
| registered_address | string | Registered business address |
| postal_address | string | Postal address (if different from registered address) |
| billing_email | string |  |
| created_at | string |  |
| updated_at | string |  |
| activated_at | string |  |
| suspended_at | string |  |
| suspension_reason | string |  |
| settings | any |  |
| quota | object |  |
| user_count | string |  |


### TenantAPIKey
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | string |  |
| name | string | Key description |
| description | string | Optional description of key usage |
| key | string | Full API key (only returned on creation) |
| key_prefix | string |  |
| is_active | boolean |  |
| created_at | string |  |
| last_used_at | string |  |
| expires_at | string |  |
| scopes | object | List of allowed scopes |


### TenantAPIKeyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string | Key description |
| description | string | Optional description of key usage |
| is_active | boolean |  |
| expires_at | string |  |
| scopes | object | List of allowed scopes |


### TenantCreate
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string | Organization name |
| slug | string | URL-safe identifier |
| domain | string | Custom domain (optional) |
| subscription_tier | SubscriptionTierEnum |  |
| contact_email | string |  |
| contact_name | string |  |
| contact_phone | string |  |
| registered_business_name | string | ASIC-registered business name |
| trading_name | string | Trading name (if different from registered name) |
| abn | string | Australian Business Number (11 digits) |
| acn | string | Australian Company Number (9 digits, required for companies) |
| business_structure | object | Legal structure of the business  * `sole_trader` - Sole Trader * `partnership` - Partnership * `company` - Company (Pty Ltd) * `trust` - Trust * `incorporated_association` - Incorporated Association |
| gst_registered | boolean | Is the business registered for GST? |
| registered_address | string | Registered business address |
| postal_address | string | Postal address (if different from registered address) |
| billing_email | string |  |


### TenantCreateRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string | Organization name |
| slug | string | URL-safe identifier |
| domain | string | Custom domain (optional) |
| subscription_tier | SubscriptionTierEnum |  |
| contact_email | string |  |
| contact_name | string |  |
| contact_phone | string |  |
| registered_business_name | string | ASIC-registered business name |
| trading_name | string | Trading name (if different from registered name) |
| abn | string | Australian Business Number (11 digits) |
| acn | string | Australian Company Number (9 digits, required for companies) |
| business_structure | object | Legal structure of the business  * `sole_trader` - Sole Trader * `partnership` - Partnership * `company` - Company (Pty Ltd) * `trust` - Trust * `incorporated_association` - Incorporated Association |
| gst_registered | boolean | Is the business registered for GST? |
| registered_address | string | Registered business address |
| postal_address | string | Postal address (if different from registered address) |
| billing_email | string |  |


### TenantQuota
Type: `object`

| Property | Type | Description |
|---|---|---|
| api_calls_limit | integer | API calls per month |
| api_calls_used | integer |  |
| api_calls_percentage | string |  |
| ai_tokens_limit | integer | AI tokens per month |
| ai_tokens_used | integer |  |
| ai_tokens_percentage | string |  |
| storage_limit_gb | number | Storage limit in GB |
| storage_used_gb | number |  |
| storage_percentage | string |  |
| max_users | integer | Maximum number of users |
| current_users | integer |  |
| quota_reset_at | string |  |
| last_reset_at | string |  |


### TenantQuotaRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| api_calls_limit | integer | API calls per month |
| ai_tokens_limit | integer | AI tokens per month |
| storage_limit_gb | number | Storage limit in GB |
| max_users | integer | Maximum number of users |
| quota_reset_at | string |  |


### TenantRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| name | string | Organization name |
| slug | string | URL-safe identifier |
| domain | string | Custom domain (optional) |
| status | TenantStatusEnum |  |
| subscription_tier | SubscriptionTierEnum |  |
| contact_email | string |  |
| contact_name | string |  |
| contact_phone | string |  |
| registered_business_name | string | ASIC-registered business name |
| trading_name | string | Trading name (if different from registered name) |
| abn | string | Australian Business Number (11 digits) |
| acn | string | Australian Company Number (9 digits, required for companies) |
| business_structure | object | Legal structure of the business  * `sole_trader` - Sole Trader * `partnership` - Partnership * `company` - Company (Pty Ltd) * `trust` - Trust * `incorporated_association` - Incorporated Association |
| registered_address | string | Registered business address |
| postal_address | string | Postal address (if different from registered address) |
| billing_email | string |  |
| suspension_reason | string |  |
| settings | any |  |


### TenantStatusEnum
Type: `string`


### TenantUser
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | string |  |
| tenant | string |  |
| tenant_name | string |  |
| user | integer |  |
| user_email | string |  |
| user_username | string |  |
| role | RoleCadEnum |  |
| created_at | string |  |
| updated_at | string |  |


### TenantUserRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| user | integer |  |
| role | RoleCadEnum |  |


### TimePeriodEnum
Type: `string`


### ToneEnum
Type: `string`


### ToneProfile
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| profile_number | string |  |
| tenant | string |  |
| name | string |  |
| description | string |  |
| tone_descriptor | string |  |
| formality_level | integer |  |
| empathy_level | integer |  |
| brevity_level | integer |  |
| use_contractions | boolean |  |
| use_emojis | boolean |  |
| greeting_style | string |  |
| closing_style | string |  |
| recommended_for | any |  |
| usage_count | integer |  |
| is_default | boolean |  |
| is_active | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### ToneProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| description | string |  |
| tone_descriptor | string |  |
| formality_level | integer |  |
| empathy_level | integer |  |
| brevity_level | integer |  |
| use_contractions | boolean |  |
| use_emojis | boolean |  |
| greeting_style | string |  |
| closing_style | string |  |
| recommended_for | any |  |
| usage_count | integer |  |
| is_default | boolean |  |
| is_active | boolean |  |


### TrainerAssignment
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| unit_details | object |  |
| gaps_count | string |  |
| assignment_id | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| assignment_status | AssignmentStatusEnum |  |
| assigned_date | string |  |
| approved_by | string |  |
| approved_date | string |  |
| meets_requirements | boolean |  |
| compliance_score | number |  |
| gaps_identified | any |  |
| matching_qualifications | any |  |
| assignment_notes | string |  |
| rejection_reason | string |  |
| created_at | string |  |
| updated_at | string |  |
| unit | integer |  |


### TrainerAssignmentRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| assignment_status | AssignmentStatusEnum |  |
| approved_by | string |  |
| approved_date | string |  |
| meets_requirements | boolean |  |
| compliance_score | number |  |
| gaps_identified | any |  |
| matching_qualifications | any |  |
| assignment_notes | string |  |
| rejection_reason | string |  |
| unit | integer |  |


### TrainerProfile
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| profile_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| email | string |  |
| linkedin_url | string |  |
| github_url | string |  |
| twitter_url | string |  |
| personal_website | string |  |
| primary_industry | string |  |
| specializations | any |  |
| years_experience | integer |  |
| last_verified_date | string |  |
| currency_status | CurrencyStatusEnum |  |
| currency_score | number |  |
| auto_verify_enabled | boolean |  |
| verification_frequency_days | integer |  |
| next_verification_date | string |  |
| created_at | string |  |
| updated_at | string |  |


### TrainerProfileDetail
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| vocational_currency_days_remaining | string |  |
| industry_currency_days_remaining | string |  |
| annual_progress_percentage | string |  |
| recent_activities_count | string |  |
| profile_number | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| email | string |  |
| role | string |  |
| department | string |  |
| employment_start_date | string |  |
| highest_qualification | string |  |
| teaching_qualifications | any |  |
| industry_qualifications | any |  |
| teaching_subjects | any |  |
| teaching_qualification_levels | any |  |
| industry_sectors | any |  |
| vocational_currency_required | boolean |  |
| industry_currency_required | boolean |  |
| teaching_currency_required | boolean |  |
| total_pd_hours | number |  |
| vocational_pd_hours | number |  |
| industry_pd_hours | number |  |
| teaching_pd_hours | number |  |
| last_vocational_pd | string |  |
| last_industry_pd | string |  |
| last_teaching_pd | string |  |
| vocational_currency_status | VocationalCurrencyStatusEnum |  |
| industry_currency_status | IndustryCurrencyStatusEnum |  |
| meets_asqa_requirements | boolean |  |
| last_compliance_check | string |  |
| compliance_issues | any |  |
| annual_pd_goal_hours | number |  |
| current_year_hours | number |  |
| pd_goals | any |  |
| created_at | string |  |
| updated_at | string |  |


### TrainerProfileDetailRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| email | string |  |
| role | string |  |
| department | string |  |
| employment_start_date | string |  |
| highest_qualification | string |  |
| teaching_qualifications | any |  |
| industry_qualifications | any |  |
| teaching_subjects | any |  |
| teaching_qualification_levels | any |  |
| industry_sectors | any |  |
| vocational_currency_required | boolean |  |
| industry_currency_required | boolean |  |
| teaching_currency_required | boolean |  |
| total_pd_hours | number |  |
| vocational_pd_hours | number |  |
| industry_pd_hours | number |  |
| teaching_pd_hours | number |  |
| last_vocational_pd | string |  |
| last_industry_pd | string |  |
| last_teaching_pd | string |  |
| vocational_currency_status | VocationalCurrencyStatusEnum |  |
| industry_currency_status | IndustryCurrencyStatusEnum |  |
| meets_asqa_requirements | boolean |  |
| last_compliance_check | string |  |
| compliance_issues | any |  |
| annual_pd_goal_hours | number |  |
| current_year_hours | number |  |
| pd_goals | any |  |


### TrainerProfileList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| profile_number | string |  |
| trainer_name | string |  |
| primary_industry | string |  |
| currency_status | CurrencyStatusEnum |  |
| currency_score | number |  |
| last_verified_date | string |  |
| scans_count | string |  |
| updated_at | string |  |


### TrainerProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| email | string |  |
| linkedin_url | string |  |
| github_url | string |  |
| twitter_url | string |  |
| personal_website | string |  |
| primary_industry | string |  |
| specializations | any |  |
| years_experience | integer |  |
| last_verified_date | string |  |
| currency_status | CurrencyStatusEnum |  |
| currency_score | number |  |
| auto_verify_enabled | boolean |  |
| verification_frequency_days | integer |  |
| next_verification_date | string |  |


### TrainerQualification
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| qualification_id | string |  |
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| qualification_type | QualificationTypeEnum |  |
| qualification_code | string |  |
| qualification_name | string |  |
| issuing_organization | string |  |
| date_obtained | string |  |
| expiry_date | string |  |
| verification_status | TrainerQualificationVerificationStatusEnum |  |
| verification_document | string |  |
| competency_areas | any |  |
| units_covered | any |  |
| industry_experience_years | integer |  |
| recent_industry_work | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### TrainerQualificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| trainer_id | string |  |
| trainer_name | string |  |
| qualification_type | QualificationTypeEnum |  |
| qualification_code | string |  |
| qualification_name | string |  |
| issuing_organization | string |  |
| date_obtained | string |  |
| expiry_date | string |  |
| verification_status | TrainerQualificationVerificationStatusEnum |  |
| verification_document | string |  |
| competency_areas | any |  |
| units_covered | any |  |
| industry_experience_years | integer |  |
| recent_industry_work | boolean |  |


### TrainerQualificationVerificationStatusEnum
Type: `string`


### TranscriptionEngineEnum
Type: `string`


### TranscriptionJob
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| job_number | string |  |
| job_status | JobStatusEnum |  |
| transcription_engine | TranscriptionEngineEnum |  |
| language | string |  |
| enable_speaker_diarization | boolean |  |
| enable_punctuation | boolean |  |
| transcript_result | string |  |
| confidence_score | number |  |
| processing_time_seconds | number |  |
| error_message | string |  |
| retry_count | integer |  |
| max_retries | integer |  |
| created_at | string |  |
| started_at | string |  |
| completed_at | string |  |
| audio_recording | integer |  |


### TranscriptionJobRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| job_status | JobStatusEnum |  |
| transcription_engine | TranscriptionEngineEnum |  |
| language | string |  |
| enable_speaker_diarization | boolean |  |
| enable_punctuation | boolean |  |
| transcript_result | string |  |
| confidence_score | number |  |
| processing_time_seconds | number |  |
| error_message | string |  |
| retry_count | integer |  |
| max_retries | integer |  |
| audio_recording | integer |  |


### TrendEnum
Type: `string`


### TriggerTypeEnum
Type: `string`


### UnitOfCompetency
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| assignments_count | string |  |
| unit_id | string |  |
| tenant | string |  |
| unit_code | string |  |
| unit_name | string |  |
| unit_type | UnitTypeEnum |  |
| qualification_code | string |  |
| required_qualifications | any |  |
| required_competency_areas | any |  |
| required_industry_experience | integer |  |
| requires_tae | boolean |  |
| requires_industry_currency | boolean |  |
| learning_outcomes | any |  |
| assessment_methods | any |  |
| technical_skills | any |  |
| prerequisite_units | any |  |
| related_units | any |  |
| created_at | string |  |
| updated_at | string |  |


### UnitOfCompetencyRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| unit_code | string |  |
| unit_name | string |  |
| unit_type | UnitTypeEnum |  |
| qualification_code | string |  |
| required_qualifications | any |  |
| required_competency_areas | any |  |
| required_industry_experience | integer |  |
| requires_tae | boolean |  |
| requires_industry_currency | boolean |  |
| learning_outcomes | any |  |
| assessment_methods | any |  |
| technical_skills | any |  |
| prerequisite_units | any |  |
| related_units | any |  |


### UnitTypeEnum
Type: `string`


### UpdateTypeEnum
Type: `string`


### User
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. |
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### UserInvitation
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | string |  |
| tenant | string |  |
| tenant_name | string |  |
| email | string |  |
| role | RoleCadEnum |  |
| message | string | Optional message to include in invitation email |
| status | object |  |
| token | string |  |
| invited_by_username | string |  |
| created_at | string |  |
| expires_at | string |  |
| can_accept | string |  |


### UserInvitationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| email | string |  |
| role | RoleCadEnum |  |
| message | string | Optional message to include in invitation email |
| expires_at | string |  |


### UserInvitationStatusEnum
Type: `string`


### UserMinimal
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### UserProfile
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. |
| email | string |  |
| email_verified | string |  |
| first_name | string |  |
| last_name | string |  |
| date_joined | string |  |


### UserProfileRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### UserRegistration
Type: `object`

| Property | Type | Description |
|---|---|---|
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. |
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### UserRegistrationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. |
| email | string |  |
| password | string |  |
| password_confirm | string |  |
| first_name | string |  |
| last_name | string |  |
| invitation_token | string |  |


### UserRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. |
| email | string |  |
| first_name | string |  |
| last_name | string |  |


### Verification
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| improvement_action | integer |  |
| outcome | VerificationOutcomeEnum |  |
| outcome_display | string |  |
| notes | string | Verification findings and observations |
| evidence_reviewed | object | List of evidence items reviewed |
| effectiveness_score | integer | Effectiveness rating 1-5 |
| requires_followup | boolean |  |
| followup_actions | string |  |
| followup_due_date | string |  |
| verifier | integer |  |
| verifier_name | string |  |
| verified_at | string |  |
| created_at | string |  |
| updated_at | string |  |


### VerificationOutcomeEnum
Type: `string`


### VerificationRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| improvement_action | integer |  |
| outcome | VerificationOutcomeEnum |  |
| notes | string | Verification findings and observations |
| evidence_reviewed | object | List of evidence items reviewed |
| effectiveness_score | integer | Effectiveness rating 1-5 |
| requires_followup | boolean |  |
| followup_actions | string |  |
| followup_due_date | string |  |


### VerificationScan
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| linkedin_activities | [LinkedInActivity] |  |
| github_activities | [GitHubActivity] |  |
| scan_number | string |  |
| scan_type | ScanTypeEnum |  |
| sources_to_scan | any |  |
| scan_status | ScanStatusEnum |  |
| total_items_found | integer |  |
| relevant_items_count | integer |  |
| currency_score | number |  |
| scan_duration_seconds | number |  |
| error_message | string |  |
| started_at | string |  |
| completed_at | string |  |
| created_at | string |  |
| trainer_profile | integer |  |


### VerificationScanList
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| scan_number | string |  |
| scan_type | ScanTypeEnum |  |
| scan_status | ScanStatusEnum |  |
| currency_score | number |  |
| linkedin_count | string |  |
| github_count | string |  |
| created_at | string |  |
| completed_at | string |  |


### VerificationScanRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| scan_type | ScanTypeEnum |  |
| sources_to_scan | any |  |
| scan_status | ScanStatusEnum |  |
| total_items_found | integer |  |
| relevant_items_count | integer |  |
| currency_score | number |  |
| scan_duration_seconds | number |  |
| error_message | string |  |
| trainer_profile | integer |  |


### VerificationStatus901Enum
Type: `string`


### VersionEnum
Type: `string`


### Visibility757Enum
Type: `string`


### VocationalCurrencyStatusEnum
Type: `string`


### WebhookEndpoint
Type: `object`

| Property | Type | Description |
|---|---|---|
| id | integer |  |
| tenant | string |  |
| name | string |  |
| target | TargetEnum |  |
| url | string |  |
| events | object | Event types to send (e.g., ['decision.finalized', 'override.approved']) |
| active | boolean |  |
| created_at | string |  |
| updated_at | string |  |


### WebhookEndpointRequest
Type: `object`

| Property | Type | Description |
|---|---|---|
| tenant | string |  |
| name | string |  |
| target | TargetEnum |  |
| url | string |  |
| secret | string | HMAC secret for signing |
| events | object | Event types to send (e.g., ['decision.finalized', 'override.approved']) |
| active | boolean |  |

