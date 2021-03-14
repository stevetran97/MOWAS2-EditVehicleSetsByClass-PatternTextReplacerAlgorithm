# # Imports
import fileinput
import re
import os

# ----------------------------------------------------------------------------
# Input Variables

# Replacement pattern order must match the order of replacement text below
replacementPatterns = [r'c\([0-9]+\)', r'cp\([0-9]+\)']

# Matches up the comment trigger with a state attached to an array of replacement text
# Add comment states to this hash table for more divisions
# Add ';' followed by the hash string in the txt document on a separate line as a trigger for state change
# Note: The last hash and replacement pattern sets the state from that comment to the end of the set file
vehicleClassHash = {
    'lightmgcar': ["c(15)", "cp(0)"],
    'transport': ["c(5)", "cp(0)"],
    'logi': ["c(15)", "cp(0)"],
    'emplacements': ["c(5)", "cp(5)"],
    'light_mortar_spg': ["c(15)", "cp(10)"],
    'lightspgarty': ["c(20)", "cp(15)"],
    'heavyspgarty': ["c(30)", "cp(20)"],
    'lightrocketarty': ["c(30)", "cp(15)"],
    'heavyrocketarty': ["c(30)", "cp(20)"],
    'light_apc': ["c(5)", "cp(0)"],
    'medium_wheeled_apc': ["c(10)", "cp(5)"],
    'heavy_apc': ["c(20)", "cp(10)"],
    'spg_aa': ["c(15)", "cp(10)"],
    'medium_tank': ["c(15)", "cp(15)"],
    'cold_war_tank': ["c(25)", "cp(15)"],
    'heavy_cold_war_tank': ["c(30)", "cp(20)"],
    'heavy_modern_war_tank': ["c(35)", "cp(25)"],
    'very_heavy_modern_war_tank': ["c(40)", "cp(30)"],
    'tank_destroyer': ["c(15)", "cp(10)"],
    'aircraft': ["c(60)", "cp(20)"],
    'light_robot_mech': ["c(40)", "cp(10)"],
}

# This SINGLE string entry is when enables a state Change check
commentTrigger = ';'
# ----------------------------------------------------------------------------
# Variables
fileToEditDirectory = r'.\FilesToEdit'

# Helpers

# Formatting Helper: Gets filePath from file Name and Directory


def getFilePath(fileDirectory, fileName):
    return r'{filePath}\{fileName}'.format(filePath=fileDirectory, fileName=fileName)

# State Selection Helper: Gets appropriate replacement according to comment system


def stateSelection(line, vehicleClassHash):
    # Loop through keys in vehicleClassHash
    for key in vehicleClassHash:
        # If key is found in line
        # return value of key as state
        if re.search(key, line):
            return vehicleClassHash[key]
    # If can't find a state, return DISABLING NONE default state
    return None

# search and Replace Helper: replaces text_to_search with replacement_text


def searchAndReplace(text_to_search, replacement_text):
    # Find pattern in the current line
    pattern_match = re.findall(text_to_search, line)
    # Replace with desired if pattern matches
    if pattern_match:
        print(line.replace(pattern_match[0], replacement_text), end='')
    else:
        # else rewrite unchanged line
        print(line, end='')


# Main Algorithm: Editting Logic

# Loop through pattern base for patterns to replace
for index in range(len(replacementPatterns)):
    # Loop through files in Edit Folder
    for fileName in os.listdir(fileToEditDirectory):
        # Open one of the files
        filePath = getFilePath(fileToEditDirectory, fileName)
        print('Editting: ', filePath)

        with fileinput.FileInput(filePath, inplace=True) as file:
            # For each line
            for line in file:
                # Trigger state change while searching through lines
                if line[0] == commentTrigger:
                    state = stateSelection(line, vehicleClassHash)

                # What to search for vs what to replace it with
                if state != None:
                    searchAndReplace(replacementPatterns[index], state[index])
                else:
                    # else rewrite unchanged line
                    print(line, end='')
