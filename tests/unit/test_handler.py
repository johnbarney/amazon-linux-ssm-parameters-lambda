import pytest

from amazon_linux_ssm_parameters import app


@pytest.fixture()
def cw_cron_event():
    return {}


def test_lambda_handler(cw_cron_event, mocker):
    ret = app.lambda_handler(cw_cron_event, "")
    assert ret is True
