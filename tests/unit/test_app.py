# SPDX-FileCopyrightText: 2022 VMware Inc
#
# SPDX-License-Identifier: MIT
import logging

from dynaconf.utils import DynaconfDict
from fastapi.testclient import TestClient
from fastapi import status

class TestApp:

    def test_root(self, test_client):
        response = test_client.get("/")

        assert response.url == test_client.base_url + "/"
        assert response.status_code == status.HTTP_200_OK
        assert "Repository Service for TUF API" in response.text


    def test_default_notfound(self, test_client):
        response = test_client.get("/invalid_url")

        assert response.url == test_client.base_url + "/invalid_url"
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not Found"}

    def teste_rstuf_bootstrap_node_not_declared(self, token_headers, monkeypatch):
        monkeypatch.setenv("RSTUF_BOOTSTRAP_MODE", "false")
        monkeypatch.setattr(
            "repository_service_tuf_api.settings", DynaconfDict(
                {
                    "BOOTSTRAP_MODE": "true",
                    "TOKEN_KEY": "token",
                    "ADMIN_PASSWORD": "secret",
                    "DATA_DIR": "./data_test",
                    "BROKER_SERVER": "fakeserver",
                    "REDIS_SERVER": "redis://fakeredis"
                }
            )
        )
        monkeypatch.setattr("repository_service_tuf_api.sync_redis", lambda: None)
        import app
        client = TestClient(app.rstuf_app)
        response = client.get("/api/v1/bootstrap/", headers=token_headers)
        assert app.settings.get("BOOTSTRAP_MODE") is None
        assert response.status_code == 404


    # def teste_rstuf_bootstrap_node_is_true(self, test_client, monkeypatch):
    #     monkeypatch.setenv("RSTUF_BOOTSTRAP_MODE", "false")
    #     monkeypatch.setattr(
    #         "repository_service_tuf_api.settings", DynaconfDict(
    #             {
    #                 "BOOTSTRAP_MODE": "true",
    #                 "TOKEN_KEY": "token",
    #                 "ADMIN_PASSWORD": "secret",
    #                 "DATA_DIR": "./data_test",
    #                 "BROKER_SERVER": "fakeserver",
    #                 "REDIS_SERVER": "redis://fakeredis"
    #             }
    #         )
    #     )

    #     import app
    #     assert app.settings.get("BOOTSTRAP_MODE") is None