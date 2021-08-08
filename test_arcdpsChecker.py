import pytest
from requests.models import HTTPError

import arcdpsChecker


class TestArcdpsChecker:
    def test_getHTMLText(self, mocker):
        mockedGet = mocker.patch("arcdpsChecker.requests.get")
        mockedGet.return_value.status_code = 200
        mockedGet.return_value.ok = True
        mockedGet.return_value.text = "random text"
        assert arcdpsChecker.getHTMLText() == "random text"

        mockedGet.return_value.status_code = 404
        mockedGet.return_value.ok = False
        with pytest.raises(HTTPError):
            arcdpsChecker.getHTMLText()


if __name__ == "__main__":
    pytest.main()
