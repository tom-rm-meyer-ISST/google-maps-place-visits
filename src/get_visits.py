#
# Copyright (c) 2024 Tom Meyer
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#

import json
import datetime as dt
# import datetime, timedelta, date from datetime
from datetime import datetime, timedelta, date
from dateutil import parser
from enum import Enum
from typing import List

#######################################
# TODO: SET ACCORDING TO YOUR NEEDS
#######################################

# Create a folder data and put downloaded Timeline.json in it
json_file : str = "data/Sample-Timeline.json"
# Get first and last timestamps of interest (year, month, day)
begin_ts : datetime = dt.datetime(2024,1,1,)
end_ts : datetime = dt.datetime(2024,12,31)

# Define either place ID or lat/ long
# place ID to identify the times visited, preferred.
place_id : str = "ChIJG2DC5DnJvkcRMYiHOUw4vrQ"
#######################################
# END OF USER INPUT
#######################################

# Build arrays of basic data
print("Extracting relevant data...")

"""
Class represents the minimal data needed to classify a visit. A visit can take place over multiple days.
"""
class Visit:

    start_ts: datetime
    end_ts: datetime
    location_place_id: str
    probability: float
    semanticType: str

    def __init__(self, start_ts, end_ts, location_place_id, probability, semanticType):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.location_place_id = location_place_id
        self.probability = probability
        self.semanticType = semanticType

    
    def __repr__ (self):
        return f"Visit(start_ts={self.start_ts}, end_ts={self.end_ts}, location_place_id={self.location_place_id}, probability={self.probability})"
    

    """
    Read a single Visit entity from the corresponding json structure
    
    Returns single Visit
    """
    @staticmethod
    def getVisitFromJson(json: dict) -> 'Visit':

        assert 'topCandidate' in json['visit'], f"Error: Expected structure to contain visit.topCandidate. Not found in {json}."

        visitObject = Visit(
            start_ts = parser.isoparse(json['startTime']),
            end_ts = parser.isoparse(json['endTime']),
            location_place_id = json['visit']['topCandidate']['placeId'],
            probability = json['visit']['topCandidate']['probability'],
            semanticType = json['visit']['topCandidate']['semanticType']
        )
        return visitObject


    """
    Read all Visit entities from the read Timeline.json exported from Google Maps
    
    Returns List of Visits
    """
    @staticmethod
    def readListfromJson(json_file: str) -> List['Visit']:
        print("Loading '%s' ..."%json_file)
        main_dict = json.load(open(json_file, 'r', encoding='utf-8'))   # This can take a bit of time
        print("JSON file loaded")
        # data is a big list of dicts.

        # list comprehension to do the following
        # 1. Get visit array for semanticSegments if they have a visit (they seperated activity, timelinePath and visit in new format)
        data = [ segment for segment in main_dict['semanticSegments'] if 'visit' in segment ]

        visits: List[Visit] = [Visit.getVisitFromJson(visitJson) for visitJson in data]          

        print(f"Total number of visits: {len(visits)}.")

        return visits
    

    """
    Filters given Visits to match the place, and time period.
    
    Returns filtered visits
    """
    @staticmethod
    def getVisitsByPlaceId(visits: List['Visit'], place_id: str, begin_ts: datetime, end_ts: date) -> List['Visit']:

        visits = [
            visit for visit in visits
            if visit.start_ts.replace(tzinfo=None) >= begin_ts and 
                visit.end_ts.replace(tzinfo=None) <= end_ts and
                visit.location_place_id == place_id
        ]

        print(f"Filtered to {len(visits)} matching place {place_id} and time period {begin_ts.date()} - {end_ts.date()}")

        return visits
    

    """"
    Returns the dates without duplicates present in the given visits.
    """
    @staticmethod
    def getNonDuplicateDaysAtPlace(visits: List['Visit']) -> List[date]:
        days_on_site: int = 0
        dates = []

        # Check positions only after the specified date.
        for visit in visits:

            # get dates out of start and end date
            difference = (visit.end_ts - visit.start_ts).days
            
            if difference > 0:
                print(f"Difference > 0 for {visit.start_ts.date()} and {visit.end_ts.date()}, difference {difference} on place {visit.location_place_id}")
                current_date = visit.start_ts.date()
                end_date = visit.end_ts.date()
                while current_date <= end_date:
                    if current_date in dates:
                        print(f"Date {current_date} already in dates. Not adding it again.")
                    else:
                        dates.append(current_date)
                        days_on_site += 1
                    current_date += timedelta(days=1)

            else:
                if visit.start_ts.date() in dates:
                    print(f"Date {visit.start_ts.date()} already in dates. Not adding it again.")
                else:
                    dates.append(visit.start_ts.date())
                    days_on_site += 1

            assert days_on_site == len(dates), f"Error: days_on_site ({days_on_site}) does not match the number of days in dates ({len(dates)})."

            print(f"Evaluation of amount of visits of place with id {place_id} done for the time period {begin_ts.date()} - {end_ts.date()}.")
            print(f"Number of Visits: {days_on_site}")
            print("Days visited:")
            [ print (f"{day}") for day in dates ]

        return dates


def main():
    visits: List[Visit] = Visit.readListfromJson(json_file)
    visits = Visit.getVisitsByPlaceId(visits=visits, place_id=place_id, begin_ts=begin_ts, end_ts=end_ts)
    Visit.getNonDuplicateDaysAtPlace(visits=visits)


if __name__ == "__main__":
    main()
