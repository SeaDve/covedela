import os
from typing import Optional, Tuple, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .task_list import TaskList

TOKEN_STORAGE_PATH = "./token_cache.json"
SCOPES = ["https://www.googleapis.com/auth/tasks"]


class Client:
    _service = None
    _task_lists = None

    def __init__(self):
        creds = None

        if os.path.exists(TOKEN_STORAGE_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_STORAGE_PATH, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(TOKEN_STORAGE_PATH, "w") as token:
                token.write(creds.to_json())

        self._service = build("tasks", "v1", credentials=creds)

    def get_task_lists(self, page_token: Optional[str] = None) -> List[TaskList]:
        """Returns a (List of TaskList, next page token)

        Can throw Http Error
        """
        results = (
            self._service.tasklists()
            .list(maxResults=100, pageToken=page_token)
            .execute()
        )

        task_lists: List[TaskList] = []
        for item in results.get("items", []):
            task_lists.append(TaskList(self, item))

        self._task_lisks = task_lists

        # , results.get("nextPageToken", [])

        return task_lists

    def service(self):
        return self._service

    def update(self) -> None:
        for task_list in self._task_lisks:
            task_list.update()
