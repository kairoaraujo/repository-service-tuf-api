# SPDX-FileCopyrightText: 2022-2023 VMware Inc
#
# SPDX-License-Identifier: MIT

import logging
from fastapi import APIRouter, Security, status

from repository_service_tuf_api import SCOPES_NAMES, targets, settings
from repository_service_tuf_api.token import validate_token

if settings.get("AUTH", True) is True:
    logging.debug("RSTUF build in auth is enabled")
    auth =  validate_token
else:
    logging.debug("RSTUF build in auth is disabled")
    auth = None

router = APIRouter(
    prefix="/targets",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    summary=(
        "Add targets files to Metadata. "
        f"Scope: {SCOPES_NAMES.write_targets.value}"
    ),
    description="Add targets files to Metadata.",
    response_model=targets.Response,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
)
def post(
    payload: targets.AddPayload,
    _user=Security(auth, scopes=[SCOPES_NAMES.write_targets.value]),
):
    return targets.post(payload)


@router.delete(
    "/",
    summary=(
        "Remove targets files from Metadata. "
        f"Scope: {SCOPES_NAMES.delete_targets.value}"
    ),
    description="Remove targets files from Metadata.",
    response_model=targets.Response,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
)
def delete(
    payload: targets.DeletePayload,
    _user=Security(auth, scopes=[SCOPES_NAMES.delete_targets.value]),
):
    return targets.delete(payload)


@router.post(
    "/publish/",
    summary=(
        "Submit a task to publish targets."
        f"Scope: {SCOPES_NAMES.write_targets.value}"
    ),
    description=(
        "Trigger a task to publish targets not yet published from the "
        "RSTUF Database"
    ),
    response_model=targets.Response,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
)
def post_publish_targets(
    _user=Security(auth, scopes=[SCOPES_NAMES.write_targets.value]),
):
    return targets.post_publish_targets()
