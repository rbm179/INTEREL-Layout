import requests 
import csv, time, sys, json
from configparser import ConfigParser
# Calling Logging package
import logging_package as logstream
logger = logstream.GetLogger().get_logger()
from colorama import Fore, Style, init
import helpers
from pathlib import Path

# Purpose:
# This tool fetch property layout details using INTEREL IIO API and writes unit location details into CSV file.
# it stores records i.e: Building_name, Floor_Name, Unit_Name, Building_ID, Floor_ID, Unit_ID, UnitTypeId, UnitTypeName into Master csv file.
# It also create two different JSON files for PMS room mapping. One is compatible with Mews PMS and other is OHIP compatible room mapping json.


### Functions

def property_layout(method, endpoint, **kwargs): # Generic function
    try:
        resp = requests.request(method, endpoint, **kwargs)
        resp.raise_for_status
        return resp.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API request: {e}")
        sys.exit(1)


def get_unit_locations(property_data):
    unit_locations = []
    for building in property_data["buildings"]:
        # print (f"\nBuilding ID: {building['buildingId']}")
        for floor in building["floors"]:
            # print (f"  Floor ID: {floor['floorId']}")
            for unit in floor["units"]:
                unit_locations.append({
                    "Building_Name": building['name'].replace("'", ' '),
                    "Floor_Name": floor['name'],
                    "Unit_No": unit['name'],
                    "Building_ID": building['buildingId'],
                    "FloorID": floor['floorId'],
                    "Unit_ID": unit['unitId'],
                    "UnitTypeId": unit["unitTypeId"]
                })
    return unit_locations


def get_unit_types(property_data):
    unit_types = []
    for unit_type in property_data["unitTypes"]:
        unit_types.append({
            "UnitTypeId": unit_type['unitTypeId'],
            "UnitTypeName": unit_type['name']
        })  
    return unit_types

def get_pms_room_mapping_01(unit_location_details, propertyId):    # Room Mapping json used in mews, or Marriott PMS, PMS over API
    pms_room_mapping = []
    for item in unit_location_details:
        pms_room_mapping_dict = {"pmsRoomNumber": f'{item["Unit_No"]}', "location": f'{propertyId}/{item["Building_ID"]}/{item["FloorID"]}/{item["Unit_ID"]}'}
        pms_room_mapping.append(pms_room_mapping_dict)
    # print(pms_room_mapping)
    data_all = {"mapping": pms_room_mapping}
    return data_all

def get_pms_room_mapping_02(unit_location_details, propertyId):    # For OHIP compatible room mamping json
    # pms_room_mapping = {"base": f'{propertyId}/001'} # Hardcoded Building_ID 
    pms_room_mapping = {"base": f'{propertyId}/{unit_location_details[0]["Building_ID"]}'}
    for item in unit_location_details:
        pms_room_mapping_dict = {f'{item["Unit_No"]}': f'{propertyId}/{item["Building_ID"]}/{item["FloorID"]}/{item["Unit_ID"]}'}
        pms_room_mapping.update(pms_room_mapping_dict)
    # print(pms_room_mapping)
    return pms_room_mapping
    # data_all = {pms_room_mapping}
    # return data_all

def write_to_json(data, filename, **kwargs):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


##############################################################################

config = ConfigParser()
config.read('./IIOAPIClient_layout.config')

propertyId = config.get('settings', 'propertyId')
base_url = config.get('settings', 'base_url')
respect_timeout = config.getint('settings', 'request_timeout_seconds')
is_bearer = config.getboolean('authorization', 'is_bearer')
bearer_token = config.get('authorization', 'bearer_token')
is_interel_api_key = config.getboolean('authorization', 'is_interel_api_key')
interel_api_key = config.get('authorization', 'interel_api_key')

out_unit_locations_csv = f"{propertyId}_Master.csv"

params = {'size': '1000'}

global is_enable_api_key
global token
if is_bearer is True and is_interel_api_key is False:
    is_enable_api_key = False
    token = bearer_token
elif is_bearer is False and is_interel_api_key is True:
    is_enable_api_key = True
    token = interel_api_key

else:
    logger.critical("Invalid INTEREL API / Bearer token configurations !")
    logger.critical("Please check INTEREL API Key and Bearer token settings in configuration")
    logger.critical("Exit in 60 seconds ...")
    time.sleep(60)
    sys.exit()

## authorization header setup
if is_enable_api_key is True:
    headers = {'Authorization': f'InterelApiKey {token}', "Content-Type": "application/json"}
else:
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}

#############################################################################

def main():
    
    url_layout = f"{base_url}/properties/{propertyId}/layout"

    data = property_layout("GET", url_layout, headers=headers, params=params) # storing json respnose in variable. 

    property_layout_data = data["data"] # Extracting "data" section from json response and storing in variable.

    unit_location_details = get_unit_locations(property_layout_data) # Getting unit location details [building, Floor, Room along with their id] and storing in variable.

    unit_type_details = get_unit_types(property_layout_data)    # Extracting unit types details and storing in variable.

    # Combining unit location details and unit type details based on UnitTypeId.
    for unit in unit_location_details: # Looping through unit location details to map UnitTypeName and add into unit location details.
        for unit_type in unit_type_details:
            if unit['UnitTypeId'] == unit_type['UnitTypeId']:
                # print(f"UnitTypeId from Unit_Details: {unit['UnitTypeId']} and UnitTypeId from Unit_Types: {unit_type['UnitTypeId']} and Unit Type Name: {unit_type['UnitTypeName']}")
                unit['UnitTypeName'] =  unit_type['UnitTypeName']
                break
            else:
                unit['UnitTypeName'] = "N/A"
    # print(unit_details)

    # print(unit_location_details[0].keys())
    if Path(out_unit_locations_csv).exists():
        # Remove file if already exists.
        logger.info(f"Removing existing output csv file: {out_unit_locations_csv}")
        helpers.WriteCSVFile(out_unit_locations_csv, []).remove_file()

    
    headerrow =  unit_location_details[0].keys()
    helpers.WriteCSVFile(out_unit_locations_csv, headerrow).write_into_csv_file() # Writing header row into output csv file.
    for item in unit_location_details: # Looping through unit location details to write each row into output csv file.
        helpers.WriteCSVFile(out_unit_locations_csv, item.values()).write_into_csv_file()
        # print(item)
        # logger.info(f"Wrote unit details for Unit_No: {item['Unit_No']} into output csv file.")
        # logger.info(f"Unit location are: {unit_location_details}")
        logger.info(f"{item}\n")
    logger.info(f"Writing results in CSV file: {out_unit_locations_csv} \n") 

    # else: 
    #     pass
    # print(unit_location_details[1].values())

############ Working on JSON data creation of Room Mapping for PMS integration ####################    
    
    # Except OHIP PMS integration:
    get_pms_room_mapping_json01 = get_pms_room_mapping_01(unit_location_details, propertyId)   
    output_json_file01 = f"{propertyId}_PMS_Room_Mapping01.json"
    if Path(output_json_file01).exists(): # Remove file if already exists.
        logger.info(f"Removing existing output csv file: {output_json_file01}")
        helpers.WriteCSVFile(output_json_file01, []).remove_file()
    # Writing result in JSON file
    logger.info(f"Writing results in JSON file: {output_json_file01} \n") 
    write_to_json(get_pms_room_mapping_json01, output_json_file01)
    
    # Room Mapping json used in OHIP PMS integration
    get_pms_room_mapping_json02 = get_pms_room_mapping_02(unit_location_details, propertyId)   
    # print(get_pms_room_mapping_json02)
    output_json_file02 = f"{propertyId}_PMS_Room_Mapping02.json"

    if Path(output_json_file02).exists():  # Remove file if already exists.
        logger.info(f"Removing existing output csv file: {output_json_file02}")
        helpers.WriteCSVFile(output_json_file02, []).remove_file()
    # Writing result in JSON file
    logger.info(f"Writing results in JSON file: {output_json_file02} \n")
    write_to_json(get_pms_room_mapping_json02, output_json_file02)
    
    # print(data_all)
    # print(type(data_all))
    # print(pms_room_mapping)


if __name__ == "__main__":
    main()


