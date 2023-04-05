# SPDX-FileCopyrightText: 2022-2023 VMware Inc
#
# SPDX-License-Identifier: MIT

import logging
from fastapi import APIRouter, Depends, Security

from repository_service_tuf_api import SCOPES_NAMES, tasks, settings
from repository_service_tuf_api.token import validate_token

if settings.get("AUTH", True) is True:
    logging.debug("RSTUF build in auth is enabled")
    auth =  validate_token
else:
    logging.debug("RSTUF build in auth is disabled")
    auth = None

router = APIRouter(
    prefix="/task",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    summary=("Get task state. " f"Scope: {SCOPES_NAMES.read_tasks.value}"),
    description=(
        "Get Repository Metadata task state. "
        "The state is according with Celery tasks: "
        "`PENDING` the task still not processed or unknown/inexistent task. "
        "`RECEIVED` task is reveived by the broker server. "
        "`PRE_RUN` the task will start by repository-service-tuf-worker. "
        "`RUNNING` the task is in execution. "
        "`FAILURE` the task failed to executed. "
        "`SUCCESS` the task execution is finished. "
    ),
    response_model=tasks.Response,
    response_model_exclude_none=True,
)
def get(
    params: tasks.GetParameters = Depends(),
    _user=Security(validate_token, scopes=[SCOPES_NAMES.read_tasks.value]),
):
    return tasks.get(params.task_id)
