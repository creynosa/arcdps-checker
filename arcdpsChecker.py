import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
import yaml
from bs4 import BeautifulSoup
from requests.models import HTTPError


def getHTMLText() -> str:
    """Returns the HTML of the arcdps site as text."""
    arcdpsSite = "https://www.deltaconnected.com/arcdps/x64/"
    r = requests.get(arcdpsSite)
    if r.ok:
        return r.text
    else:
        raise HTTPError(f"Code: {r.status_code}.")


def getSoup() -> BeautifulSoup:
    """Returns the BeautifulSoup object made from the arcdps website html."""
    htmlText = getHTMLText()
    soup = BeautifulSoup(htmlText, "html.parser")
    return soup


def getCurrentUploadTime() -> datetime:
    """Finds and returns the datetime corresponding to the last time the arcdps file was updated."""
    soup = getSoup()
    uploadTimeText = (
        soup.find(href="d3d9.dll").parent.find_next_sibling("td").text.strip()
    )
    if not uploadTimeText:
        print("No upload time found for current arcdps d3d9.dll file.")
        sys.exit()
    uploadTime = datetime.strptime(uploadTimeText, "%Y-%m-%d %H:%M")

    return uploadTime


def getLastUploadTime() -> Optional[datetime]:
    """Returns the last datetime that the arcdps file was updated previously."""
    configPath = Path.cwd() / "config" / "settings.yaml"
    with open(configPath, "r") as f:
        config = yaml.safe_load(f)
    lastUploadTime = config["lastUploadTime"]

    return lastUploadTime


def writeUploadTime() -> None:
    """Writes the current arcdps upload datetime to a configuration file."""
    configPath = Path.cwd() / "config" / "settings.yaml"
    currentUploadTime = getCurrentUploadTime()
    config = {"lastUploadTime": currentUploadTime}
    with open(configPath, "w") as f:
        yaml.dump(config, f)


def checkForUpdate() -> bool:
    """Determines if there is an update to arcdps."""
    currentUploadTime = getCurrentUploadTime()
    lastUploadTime = getLastUploadTime()
    if lastUploadTime:
        if currentUploadTime > lastUploadTime:
            writeUploadTime()
            return True
        else:
            return False
    else:
        writeUploadTime()
        return False


def alert() -> None:
    """Simple print statement alerting of an update to arcdps."""
    update = checkForUpdate()
    if update:
        print(
            'There is an update for arcdps! Download here: "https://www.deltaconnected.com/arcdps/x64/"'
        )
    else:
        print("No update found.")


if __name__ == "__main__":
    alert()
