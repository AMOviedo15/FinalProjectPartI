#1990958 Aaron Oviedo 

import csv
from datetime import datetime

# class that contains methods to generate inventory files



class ProcessReports:
    def __init__(self, items):
        #add combined list
        self.items = items

    # FullInventory.csv. The items
    # should be sorted alphabetically by manufacturer. Each row should contain item
    # ID, manufacturer name, item type, price, service date, and list if it is damaged.
    # The item attributes must appear in this order.
    def full_inventory(self):
        with open('FullInventory.csv', 'w') as file:
            all_items = self.items
            #sort by keys so they can be organized by manufacturer..
            key_list = sorted(all_items.keys(), key= lambda x: all_items[x]['Manufacturer Name'])
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                file.write('{},{},{},{},{},{}\n'.format(item_id, manu_name, item_type,
                                                        item_price, service_date, item_damaged))



    #Item Type Inventory.csv. there should be a file for each item type and the item type
    # needs to be in the file name. Each row of the file should contain item ID,
    # manufacturer name, price,
    # service date, and list if it is damaged. The items should be sorted by their item ID.
    def item_type_list(self):
        all_items = self.items
        all_types  = []
        key_list =  sorted(all_items.keys())
        for item in all_items:
            item_type = all_items[item]['Item Type']
            # add new types to list for report generation if a file is added with different types
            if item_type not in all_types:
                all_types.append(item_type)
        for type in all_types:
             #assign new file name for each type
            file_name_type = type + 'Inventory.csv'
            with open(file_name_type, 'w') as file:
                for item in key_list:
                    item_id = item
                    manu_name = all_items[item]['Manufacturer Name']
                    item_price = all_items[item]['Price']
                    service_date = all_items[item]['Service Date']
                    item_damaged = all_items[item]['Damaged']
                    item_type = all_items[item]['Item Type']
                    # verify each row that is written matches file
                    if type == item_type:
                        file.write('{},{},{},{},{}\n'.format(item_id, manu_name,
                                                             item_price, service_date, item_damaged))


    #PastServiceDateInventory.csv  all the items that are past the service date
    # on the day the program is actually executed. Each row should contain: item ID,
    # manufacturer name, item type, price, service date, and list if it is damaged.
    # The items must appear in the order of service date from oldest to most recent
    def past_service_date(self):
        all_items = self.items
        # reverse = true makes dates go from oldest to most recent
        key_list = sorted(all_items.keys(), key = lambda x: datetime.strptime(all_items[x]['Service Date'],
                                                                "%m/%d/%y").date(), reverse = True)
        with open('PastServiceDateInventory.csv', 'w') as file:
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                # compute todays date to verify expired items.
                current_date = datetime.now().date()
                expiration_date = datetime.strptime(service_date, "%m/%d/%y").date()
                if expiration_date < current_date:
                    file.write('{},{},{},{},{},{}\n'.format(item_id, manu_name, item_type,
                                                            item_price, service_date, item_damaged))


    #DamagedInventory.csv all items that are damaged. Each row should contain :
    # item ID, manufacturer name, item type, price, and service date.
    # The items must appear in the order of most expensive to least expensive.
    def damaged_inventory(self):
        all_items = self.items
        #order from most expensive to least expensive by reverse = true.
        key_list = sorted(all_items.keys(), key=lambda x: all_items[x]['Price'], reverse = True)
        with open('DamagedInventory.csv', 'w') as file:
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                if item_damaged:
                    file.write('{},{},{},{},{}\n').format(item_id, manu_name,
                                                          item_type, item_price, service_date)





# read in files and parse through the rows to assign the values.
if __name__ == "__main__":
    items_dict = {}
    files_list = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']

    for file in files_list:
        with open(file, 'r') as input_csv:

            parse_csv = csv.reader(input_csv, delimiter = ',')

            for row in parse_csv:
                #set item id immediately because its the common value
                item_ID = row [0]
                #separate commands based on what type of input file is entered (order of input)
                if file == files_list[0]:
                    # make 2 dimensional dict to organize by id as well and assign variables to each
                    items_dict[item_ID] = {}
                    manufact_name = row[1]
                    item_type = row[2]
                    damage_ind = row[3]
                    items_dict[item_ID]['Manufacturer Name'] = manufact_name.strip()
                    items_dict[item_ID]['Item Type'] = item_type.strip()
                    items_dict[item_ID]['Damaged'] = damage_ind.strip()
                elif file == files_list[1]:
                    item_price = row[1]
                    items_dict[item_ID]['Price'] = item_price
                elif file == files_list[2]:
                    service_date = row[1]
                    items_dict[item_ID]['Service Date'] = service_date

    # assign output to the class that will generate all of the reports
    inventory = ProcessReports(items_dict)
    # generate files from the methods defined above
    inventory.full_inventory()
    inventory.item_type_list()
    inventory.past_service_date()
    inventory.damaged_inventory()








