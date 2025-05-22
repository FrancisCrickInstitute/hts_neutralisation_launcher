import json
import logging.handlers
import os
from datetime import datetime
from typing import Optional

import urllib3


class HTTPHandler(logging.handlers.HTTPHandler):
    def __init__(self, app: str, host="", url: Optional[str] = None, *args, **kwargs):
        if url is None:
            url = os.environ.get("FLANNEL_SERVER")
            if url is None:
                raise ValueError(
                    "url not supplied and FLANNEL_SERVER environment variable is not defined"
                )
        logging.handlers.HTTPHandler.__init__(self, host, url=url, *args, **kwargs)
        self.app = app
        try:
            self.http = urllib3.PoolManager(retries=2, timeout=0.5)
        except:
            self.http = None

    def emit(self, record):
        if self.http is None:
            return None
        data = {
            "app": self.app,
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": str(datetime.fromtimestamp(record.created)),
        }
        try:
            r = self.http.request(
                "POST",
                self.url,
                headers={"Content-Type": "application/json"},
                body=json.dumps(data),
            )
        except:
            pass
