import requests
import csv
from datetime import datetime
from matplotlib import pyplot as plt

TIME = 0
BASE = 1
COUNTY = 2
ROAD = 3
PLACE = 4
MOTOR_VEHICLE = 5
BRIEF_DESC = 6
VICTIM_NAME = 7
VICTIM_GENDER = 8
VICTIM_AGE = 9
CAUSE_CODE = 10
ROAD_USER_CAT = 11
NUMBER_OF_VICTIMS = 12
DATE = 13

times = []
bases = []
counties = []
roads = []
places = []
vehicles = []
descriptions = []
victim_names = []
victim_ages = []
causes = []
road_user_cats = []
nums_of_victims = []
dates = []
days_of_the_week = []
months = []


# Fill blanks
def fill_blank(any_string):
    if any_string == None or any_string.strip() == "":
        any_string = "UNKNOWN"
    
    return any_string


# Un-reusable, custom function designed to specifically format 'road string' from 
# source data
def format_road_string(raw_string, category=False):
    if category == "road":
        raw_string = raw_string.upper().strip()
        if raw_string[-2:] == "RD":
            raw_string = raw_string.replace(raw_string[-2:], "ROAD")
        elif raw_string[-3:] == "RDD":
            raw_string = raw_string.replace(raw_string[-3:], "ROAD")
        
        if raw_string[-4:] == "ROAD":
            raw_string = raw_string.replace(raw_string[-4:], "").strip()

        if "'" in raw_string:
            raw_string = raw_string.replace("'", "")
        if "/" in raw_string:
            raw_string = raw_string.replace("/", "")
        if "SERVICE LANE" in raw_string:
            raw_string = raw_string.replace("SERVICE LANE", "").strip()
        if raw_string[0:5] == "ALONG":
            raw_string = raw_string.replace("ALONG", "").strip()
        if raw_string[0:6] == "WITHIN":
            raw_string = raw_string.replace("WITHIN", "").strip()

        if "-" in raw_string:
            raw_string = raw_string.replace("-", " ")
        if "  " in raw_string:
            raw_string = raw_string.replace("  ", " ")
        if "   " in raw_string:
            raw_string = raw_string.replace("   ", " ")
        '''
        # Alternative code
        if " - " in raw_string:
            raw_string = raw_string.replace(" - ", "-")
        if " -" in raw_string:
            raw_string = raw_string.replace(" -", "-")
        if "- " in raw_string:
            raw_string = raw_string.replace("- ", "-")
        ''' 
        if "BY PASS" in raw_string:
            raw_string = raw_string.replace("BY PASS", "BYPASS")    
        if " BAY" in raw_string:
            raw_string = raw_string.replace(" BAY", "BAY")
        if "HIGH " in raw_string:
            raw_string = raw_string.replace("HIGH ", "HIGH")
        if "HIGHSCHOOL" in raw_string:
            raw_string = raw_string.replace("HIGHSCHOOL", "HIGH SCHOOL")
        if "TOWN " in raw_string:
            raw_string = raw_string.replace("TOWN ", "TOWN")
        if "SUPER" in raw_string:
            raw_string = raw_string.replace("SUPER ", "SUPER")
            raw_string = raw_string.replace("SUPERHIGHWAY", "").strip()
        if "OLD " in raw_string:
            raw_string = raw_string.replace("OLD ", "OLD")
        if "MSA-" in raw_string:
            raw_string = raw_string.replace("MSA-", "MOMBASA-")
        if "NRB" in raw_string:
            raw_string = raw_string.replace("NRB", "NAIROBI")
        if " " in raw_string:
            raw_string = raw_string.replace(" ", " ")
        
        words = ["STREET", "AVENUE", "DRIVE", "WAY", "HIGHWAY", "BYPASS", 
                 "ACCESS", "COURSE", "SCHOOL", "CHURCH", "TOWN", "FERRY", 
                 "BEACH", "CENTRE"]
        '''
        # Alternative code
        res = [word for word in words if (word in raw_string)]
        if bool(res):
            raw_string = raw_string
        # or
        if (any(word == (element for element in words) for word in raw_string.
            split(" "))):
            raw_string = raw_string
        '''
        if any(word in raw_string for word in words):
            raw_string = raw_string
        else:
            if raw_string.find(" ") != -1:
                i = raw_string.find(" ")
                raw_string = raw_string.replace(raw_string[i:i+1], "-")
            raw_string = raw_string + " ROAD"
      
        if "--" in raw_string:
            raw_string = raw_string.replace("--", "-")

        hyphen_words = ["-MURRAM"]
        for word in hyphen_words:
            if word in raw_string:
                raw_string = raw_string.replace(word, word.replace("-"," "))
        
        if "BAY" in raw_string:
            raw_string = raw_string.replace("BAY", " BAY")
        if "OLD" in raw_string:
            raw_string = raw_string.replace("OLD", "OLD ")
        
        if "HAILE" in raw_string:
            raw_string = " HAILE SELASIE AVENUE"
        
        final_string = raw_string.upper().strip()

        return final_string


# Incomplete code: missing deinitios for cause codes
def convert_cause_code(code):
    pass

# Fill blanks
def fill_blank_time(time_string):
    if (time_string == None or 
        time_string.strip() == "" or 
        not(any(char.isdigit() for char in time_string)) or 
        "UNKNOWN" in time_string):

        time_string = "UNKNOWN"
    
    return time_string


# Un-reusable, custom function designed to format time string specific to 
# source data
def format_time_date(time_string, f):
    date_time = ""
    time_string = time_string.strip()

    if f == 'time':
        time_string = time_string.upper()
        if "HRS" in time_string:
            time_string = time_string.replace("HRS", "").strip()
        if ":" in time_string:
            time_string = time_string.replace(":","").strip()
        
        if len(time_string) == 1:
            time_string = "00:0" + time_string
        elif len(time_string) == 2:
            time_string = "00:" + time_string
        elif len(time_string) == 3:
            time_string = "0" + time_string[0] + ":" + time_string[1:]
        elif len(time_string) == 4:
            time_string = time_string[0:1] + ":" + time_string[2:]

        try:
            date_time = datetime.strptime(time_string, '%H:%M').time()
        
        except ValueError as value_err:
            print(value_err.__class__.__name__, value_err, sep=": ")
        
        #Unable to plot values as datetime.time data type. Convert to string
        date_time = str(date_time)

        return date_time
    
    elif f == 'date':
        try:
            date_time = datetime.strptime(time_string, '%d/%m/%Y').date()
        
        except ValueError as value_err:
            print(value_err.__class__.__name__, value_err, sep=": ")

        return date_time

    elif f == 'A':
        try:
            day_of_the_week = (datetime.strptime(time_string, '%d/%m/%Y').
                               weekday())
        
        except ValueError as value_err:
            print(value_err.__class__.__name__, value_err, sep=": ")

        if day_of_the_week == 0:
            date_time = "Monday"
        elif day_of_the_week == 1:
            date_time = "Tuesday"
        elif day_of_the_week == 2:
            date_time = "Wednesday"
        elif day_of_the_week == 3:
            date_time = "Thursday"
        elif day_of_the_week == 4:
            date_time = "Friday"
        elif day_of_the_week == 5:
            date_time = "Saturday"
        elif day_of_the_week == 6:
            date_time = "Sunday"

        return date_time
    
    elif f == 'm':
        month = datetime.strptime(time_string, '%d/%m/%Y').month
        if month == 1:
            date_time = "January"
        elif month == 2:
            date_time = "February"
        elif month == 3:
            date_time = "March"
        elif month == 4:
            date_time = "April"
        elif month == 5:
            date_time = "May"
        elif month == 6:
            date_time = "June"
        elif month == 7:
            date_time = "July"
        elif month == 8:
            date_time = "August"
        elif month == 9:
            date_time = "September"
        elif month == 10:
            date_time = "October"
        elif month == 11:
            date_time = "November"
        elif month == 12:
            date_time = "December"

        return date_time
    
# Populate lists
def populate_lists(filename):
    try:
        with open(filename, mode="rt") as accidents_database:
            """
            [TIME 24 HOURS,BASE/SUB BASE,COUNTY,ROAD,PLACE,MV INVOLVED,
            BRIEF ACCIDENT DETAILS,NAME OF VICTIM,GENDER,AGE,CAUSE CODE,VICTIM,
            NO.,Date DD/MM/YYYY]
            """
            reader = csv.reader(accidents_database)
            next(reader)
            count = 0
            for accident_record in reader:
                
                count += 1
                # Populate times list                
                time = accident_record[TIME].upper()
                time = fill_blank_time(time)
                if time != "UNKNOWN":
                    time = format_time_date(time, 'time')
                times.append(time)
                
                # Populate bases list
                base = accident_record[BASE].upper()
                base = fill_blank(base)
                bases.append(base)

                # Populate counties list
                county = accident_record[COUNTY].upper()
                county = fill_blank(county)
                counties.append(county)
                
                # Populate roads list
                road = accident_record[ROAD].upper()
                road = fill_blank(road)
                road = format_road_string(road, "road")
                roads.append(road)
                
                # Populate places list
                place = accident_record[PLACE].upper()
                place = fill_blank(place)
                places.append(place)
                
                # Populate vehicles list
                vehicle = accident_record[MOTOR_VEHICLE].upper()
                vehicle = fill_blank(vehicle)
                vehicles.append(vehicle)
                
                # Populate descriptions list
                description = accident_record[BRIEF_DESC].upper()
                description = fill_blank(description)
                descriptions.append(description)
                
                # Populate victim names list
                victim_name = accident_record[VICTIM_NAME].upper()
                victim_name = fill_blank(victim_name)
                victim_names.append(victim_name)
                
                # Populate victim ages list
                victim_age = accident_record[VICTIM_AGE]
                victim_age = fill_blank(victim_age)
                if victim_age != "UNKNOWN":
                    victim_age = victim_age
                victim_ages.append(victim_age)
                
                # Populate causes list
                cause = accident_record[CAUSE_CODE]
                cause = fill_blank(cause)
                # cause = convert_cause_code(cause)
                causes.append(cause)
                
                # Populate road user cats list
                road_user_cat = accident_record[ROAD_USER_CAT].upper()
                road_user_cat = fill_blank(road_user_cat)
                road_user_cats.append(road_user_cat)
                
                # Populate nums of victims list
                num_of_victims = accident_record[NUMBER_OF_VICTIMS]
                num_of_victims = fill_blank(num_of_victims)
                if num_of_victims != "UNKNOWN":
                    num_of_victims = int(num_of_victims)
                nums_of_victims.append(num_of_victims)
                
                # Populate dates, days of the week and months lists
                unformatted_date = accident_record[DATE]
                unformatted_date = fill_blank_time(unformatted_date)
                if unformatted_date != "UNKNOWN":
                    date = format_time_date(unformatted_date, 'date')
                    dates.append(date)

                    day_of_the_week = format_time_date(unformatted_date, 'A')
                    days_of_the_week.append(day_of_the_week)

                    month = format_time_date(unformatted_date, 'm')
                    months.append(month)
    
    except FileNotFoundError as not_found_err:
        print(not_found_err)
        print("Source data file not available.")
    
    except PermissionError as perm_err:
        print(perm_err)
        print("Unable to read file. Access denied.")

    except ValueError as value_err:
        print(value_err.__class__.__name__, value_err, sep=": ")
    
    except csv.Error as csv_err:
        print(csv_err.__class__.__name__, csv_err, sep=": ")
        print(f"Source: filename '{filename}', line {count}")
    
    except StopIteration as stopit_err:
        print(stopit_err.__class__.__name__, stopit_err, sep=": ")


def count_accidents(accident_data_list):
    # Create an accident dictionary to be populated and returned by the 
    # function
    accidents_dict = {}
    # Create key(s) for the accident dictionary
    keys = set(accident_data_list)
    # Assign values for each dictionary key
    for key in keys:
        num_of_accidents = list(accident_data_list).count(key)
        accidents_dict[key] = num_of_accidents
    
    # Return the outer dictionary to the calling function
    return accidents_dict


def unpack_plot_values(x_list, y_list):
    # Compare length of both (parallel) list arguments
    if len(x_list) == len(y_list):
        # Create an outer dictionary to be populated and returned by the 
        # function
        outer_dict = {}

        y_sub_list = []
        # Create keys for the outer dictionary
        keys = frozenset(x_list)
        for key in keys:
            # Create a sub-list derived from a larger list 
            y_sub_list = []
            # Using indices, append values to the sub-list when values inside 
            # the parallel list match a given key/value
            for i in range(len(x_list)):
                if x_list[i] == key:
                    y_sub_list.append(y_list[i])

            # Create an inner dictionary to act as a value(s) for the outer 
            # dictionary
            inner_dict = {}
            # Create inner key(s) for the inner dictionary
            inner_keys = frozenset(y_sub_list)
            # Using inner keys, populate the inner dictionary values by getting 
            # the count of the inner keys within the sub-list
            for inner_key in inner_keys:
                values = y_sub_list.count(inner_key)
                inner_dict.update({inner_key: values})
            
            # Build the outer dictionary with the inner dicionaries nested 
            # inside as values
            outer_dict[key] = inner_dict

        # Return the outer dictionary to the calling function
        return outer_dict
    
    else:
        raise TypeError(f"Length of x_list ({len(x_list)}) is not equal to "
                        f"length of y_list ({len(y_list)})")
    

def plot_graph(x_list, y_list, chart_type, label):
    if x_list and y_list==False:
        # Create a dictionary of from a list with the dictionary values 
        # representing the count of dictionary keys within the given list i.e. 
        # the number of accidents
        accidents_dict = count_accidents(x_list)
        x_values = accidents_dict.keys()
        y_values = accidents_dict.values()

        # Pie chart
        if chart_type == "pie":
            plt.pie(y_values, labels = x_values, autopct='%1.1f%%')
            plt.title(f"{label} v. Number of Accidents")
        
        # Bar graph
        if chart_type == "bar":
            plt.bar(x_values, y_values, color = "maroon", width = 0.4)
            y_label = "Number of Accidents"
            plt.xlabel(label)
            plt.ylabel(y_label)
            if len(x_values) > 7:
                plt.xticks(rotation = 90)
            plt.title(f"{label} v. Number of Accidents")
        
        # Line (default)) graph
        if chart_type == "":
            plt.plot(x_values, y_values)
            y_label = "Number of Accidents"
            plt.xlabel(label)
            plt.ylabel(y_label)
            if len(x_values) > 7:
                plt.xticks(rotation = 90)
            plt.title(f"{label} v. Number of Accidents")
    
    else:
        try:
            dict2  = unpack_plot_values(x_list, y_list)
            # Get list of x-values for plotting
            x_values = dict2.keys()
            # Populate several lists of y-values for plotting in a stacked bar 
            # graph
            # Loop through and stack the different lists (layers) of y-values
            for inner_key in frozenset(y_list):
                # Reset y list  with each loop
                y = []
                for key in dict2.keys():
                    try: 
                        # Check if inner dictionery contains inner key and 
                        # append inner value to list. Otherwise append 0 as 
                        # placeholder value in order to maintain shape of the 
                        # graph i.e. length of x-values v. length of y-values 
                        y.append(dict2[key][inner_key])
                    except KeyError:
                        y.append(0)

                plt.bar(x_values, y)

            '''
            # Prototype
            for key, val in dict2.items():
                x_values = val.keys()
                y_values = val.values()
                plt.bar(x_values, y_values)

            '''
            plt.xticks(rotation = 90)

            if label.find(" v. ") != -1:
                i = label.find(" v. ")
                x_label = label[:i]
                y_label = label[i+3:]

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend(frozenset(y_list), ncol=4)
            plt.title(label)            
        
        except KeyError as key_err:
            print(key_err.__class__.__name__, key_err, sep=": ")
    
    plt.show()


def main():
    print(f"\nThis program attempts to graphically visualize road accident "
          "data based on Kenyan road accident report between the years 2016 and "
          "2017 obtained from the Humanitarian Data Exchange website. You can "
          "view the original report at "
          "https://data.humdata.org/dataset/kenya-road-accidents-database/resource/bcd9ef77-cf9f-4dc0-b3f8-75ad238fb433")
    '''
    # Alternative method of retrieving data file directly from the internet
    # Incomplete code: call for collaboration
    r = requests.get('https://data.humdata.org/dataset/8288bf4a-1ec3-454d-a201-3b7e4c623063/resource/bcd9ef77-cf9f-4dc0-b3f8-75ad238fb433/download/kenya-accidents-database.xlsx')
    #print(r.status_code)
    '''
    populate_lists("kenya-accidents-database.csv")
    
    query_again = "yes"
    while query_again == "yes":

        print("\nWhat would you like to know?")
        responses = {}
        
        responses["Road"] = [input(f"What is the deadliest road in Kenya? "
                                   "[yes/no/blank]: ").lower(), roads, False, ""]
        responses["Place"] = [input(f"What is the most dangerous place? "
                                    "[yes/no/blank]: ").lower(), places, False,
                                      ""]
        responses["County"] = [input(f"What is the most dangerous county? "
                                     "[yes/no/blank]: ").lower(), counties, 
                                     False, "bar"]
        responses["Time of Day"] = [input(f"What is the deadliest hour on "
                                          "Kenyan roads? [yes/no/blank]: ").
                                          lower(), times, False, "bar"]
        responses["Day of the Week"] = [input(f"What is the deadliest day of "
                                              "the week? [yes/no/blank]: ").
                                              lower(), days_of_the_week, False,
                                                "pie"]
        responses["Month"] = [input(f"What is the deadliest month of the year?"
                                    " [yes/no/blank]: ").lower(), months, 
                                    False, "bar"]
        responses["Road User Category"] = [input(f"Which road users face the "
                                                 "most risk on Kenyan roads? "
                                                 "[yes/no/blank]: ").lower(), 
                                                 road_user_cats, False, "bar"]
        responses["Cause of Accident"] = [input(f"What is the most common cause"
                                                " of road accidents overall? "
                                                "[yes/no/blank]: ").lower(), 
                                                causes, False, "bar"]
        responses["Victim Age"] = [input(f"How old are most accident victims? "
                                         "[yes/no/blank]: ").lower(), 
                                         victim_ages, False, ""]
        responses["Number of Victims"] = [input(f"How many people have lost "
                                                "their lives on Kenyan roads? "
                                                "[yes/no/blank]: ").lower(), 
                                                nums_of_victims, False, ""]
        responses["Road v. Cause of Accident"] = [input(f"What is the most "
                                                        "common cause of road "
                                                        "accidents on each "
                                                        "road? "
                                                        "[yes/no/blank]: ").
                                                        lower(), roads, causes,
                                                          "bar"]
        '''
        responses["Place v. Time of Accident"] = [input(f"What time do "
                                                        "accidents happen at "
                                                        "each place? "
                                                        "[yes/no/blank]: ").
                                                        lower(), places, times,
                                                          "bar"]
        '''

        for key, value in responses.items():
            if value[0] == "yes":
                plot_graph(x_list=value[1], y_list=value[2], 
                           chart_type=value[3], label=key)

        query_again = input(f"\nWould you like to make another query? "
                            "[yes/no]: ")
        


if __name__ == "__main__":
    main()
