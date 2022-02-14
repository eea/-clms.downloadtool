# -*- coding: utf-8 -*-
"""
For HTTP GET operations we can use standard HTTP parameter passing
(through the URL)

"""
from datetime import datetime
from logging import getLogger
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.component import getUtility
from clms.downloadtool.utility import IDownloadToolUtility
from clms.downloadtool.utils import STATUS_LIST


log = getLogger(__name__)


class datarequest_status_patch(Service):
    """Nuts & BBox not at the same time"""

    def reply(self):
        """ JSON response """
        body = json_body(self.request)

        if not body.get("TaskID", None):
            self.request.response.setStatus(400)
            return {"status": "error", "msg": "Error, TaskID is not defined"}

        task_id = str(body.get("TaskID"))
        status = body.get("Status")
        download_url = body.get("DownloadURL")
        filesize = body.get("FileSize")

        response_json = {}

        utility = getUtility(IDownloadToolUtility)

        if not status:
            self.request.response.setStatus(400)
            return {"status": "error", "msg": "Error, Status is not defined"}

        if status not in STATUS_LIST:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Error, defined Status is not in the list",
            }
        response_json = {"TaskID": task_id, "Status": status}

        if filesize:
            response_json.update({"FileSize": filesize})

        if download_url:
            response_json.update({"DownloadURL": download_url})

        if status != "In_progress":
            # pylint: disable=line-too-long
            response_json[
                "FinalizationDateTime"
            ] = datetime.utcnow().isoformat()  # noqa: E501

        response_json = utility.datarequest_status_patch(
            response_json, task_id
        )

        if "Error, task_id not registered" in response_json:
            self.request.response.setStatus(404)
            return {"status": "error", "msg": response_json}

        self.request.response.setStatus(201)

        return response_json
