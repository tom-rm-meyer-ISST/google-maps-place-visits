# google-maps-place-visits

This repository allows you to determine the times and dates you visited a place based on a json dump of your google maps timeline data.

## Prerequisites

1. Python (I used python `3.12`)
2. Download your `Timeline.json` via the google maps app and place it in the folder data.

Setup your environment (optional, because commonly packages are already given)

Linux: 

```shell
pip install --upgrade virtualenv
# outputs where your virtualenv script lies or adds it to path
#  WARNING: The script virtualenv is installed in '/home/user/.local/bin' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

python -m virtualenv venv

# activate venv
source venv/bin/activate
# shell is prefixed with '(venv)'

# install dependencies
pip install -r requirements.txt
```

Windows: 

```shell
pip install --upgrade virtualenv
# outputs where your virtualenv script lies or adds it to path
#  WARNING: The script virtualenv is installed in '/home/user/.local/bin' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

python -m virtualenv venv

# activate venv
venv/Scripts/activate
# shell is prefixed with '(venv)'

# install dependencies
pip install -r requirements.txt
```

## Running

> [!NOTE]
> You should have already placed the gogle maps exports to `data/Timeline.json`. 

1. Identify the Place ID you would like to get the visits to. Use the [Google Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder).
2. Go to [`src/get_visits.py`](./src/get_visits.py) and update the following fields (search for section `"TODO"`):
   - `json_file`: set to file location (relative path)
   - `begin_ts`:  set to start day
   - `end_ts`: set to end day
   - `place_id`: set to id identified in step 1
3. Run with following command

```shell
python3 src/get_visits.py
```

> [!NOTE]
> The Sample-Timeline.json allows you to see how the structure should look like. The data has been faked to another place and does not really make sense.

## Development

Remember to keep the virtualenv up to date:

Remember to update the DEPENDENCIES via [DashTool](https://github.com/eclipse-dash/dash-licenses)

Download DashTool and put into your home directory (for windows this can be found via `%UserProfile%` into your folder bar). For example as `dashtool-1.1.1.-SNAPSHOT.jar`. Or just use this snippet to download and create an alias:

```shell
# install dashtool
curl -L "https://repo.eclipse.org/service/local/artifact/maven/redirect?r=dash-licenses&g=org.eclipse.dash&a=org.eclipse.dash.licenses&v=LATEST" > dashtool.jar
chmod +x dashtool.jar
echo "alias dashTool='java -jar ~/dashtool.jar'" >> .bashrc
source ~/.bashrc
```

Run as follows with the alias:

```shell
cat requirements.txt | grep -v \# \
| sed -E -e 's|([^= ]+)==([^= ]+)|pypi/pypi/-/\1/\2|' -e 's| ||g' \
| sort | uniq \
| eclipseDashTool -summary ./DEPENDENCIES -
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://spdx.org/licenses/CC-BY-4.0.html)

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Tom Meyer