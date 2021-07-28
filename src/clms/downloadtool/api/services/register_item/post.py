# -*- coding: utf-8 -*-
"""
Each time we need to interact with the utility we need to get it and call the
relevant method.

In this example we call the "register_item" method.

It's Plone REST API's best practice to send all parameters as JSON in the
body, see Plone REST API's documentation regarding content-manipulation here:
https://plonerestapi.readthedocs.io/en/latest/content.html#content-manipulation

Thus as a first thing to retrieve the information is to convert that JSON
information in the body to a python dict, and we are using the
json_body(self.request) to achieve that.

After doing all the relevant operations we should set the HTTP status of the
response (by default it will be an HTTP 200 OK), and return the JSON
information needed by as a python dict. Plone REST API will handle that dict
and encode it as a proper JSON response.

"""

from plone.restapi.services import Service
from plone.restapi.deserializer import json_body

from zope.component import getUtility
from clms.downloadtool.utility import IDownloadToolUtility


class RegisterItemPost(Service):
    """ Register an item
    """
    def reply(self):
        """ JSON endpoint """
        body = json_body(self.request)

        user_id = body.get("UserID")
        status = body.get("Status")
        task_id = body.get("TaskID")

        utility = getUtility(IDownloadToolUtility)
        utility.register_item(status, task_id, user_id)

        self.request.response.setStatus(201)
        return {"TaskID": task_id, "Status": status, "UserID": user_id}
