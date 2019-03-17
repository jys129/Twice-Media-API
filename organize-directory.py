import os
from pathlib import Path
from loguru import logger
import re

root = Path(os.getcwd())

member_level = logger.level("MEMBER", no=38, color="<green>", icon="🐍")
era_level = logger.level("ERA", no=38, color="<yellow>", icon="🐍")
event_level = logger.level("EVENT", no=38, color="<blue>", icon="🐍")

# # all of the available eras
# eras = ["yes-or-yes", 
#         'ooh-ahh', 
#         'cheer-up', 
#         'tt', 
#         'knock-knock', 
#         'signal', 
#         'likey', 
#         'heart-shaker', 
#         'what-is-love',
#         'dance-the-night-away',
#         'bdz',
#         'yes-or-yes']

eras = []

# Finds all the subdirectories (on the current level!)
# and returns it in a python list
def get_subdirs(dir_path, level="debug"):
    logger.log(level, "Getting subdirs from {}", dir_path)
    directories = [] # a list to append to
    
    # For this directory, look through and find all the children
    for entity in os.listdir(dir_path.resolve()):
        logger.log(level, "Found entity: {entity}",  entity = entity )
        
        # if a child is found that is a directory, add it to the list. Otherwise, do nothing.
        if os.path.isdir((dir_path / entity).resolve()) :
            
            logger.log(level, "Found directory: {entity}", entity = entity)
            directories.append(Path(entity))
    

    logger.log(level, "In total, found the directories {}", str(directories))
    
    # return the built up list
    return directories

# Finds all the images in a folder. Not recursive, and will only work on one level.
# # TODO: Extract all the files from the _press (case insensitive) folder, and delete 
# # (or should the folders be moved instead?) all other subfolders.
# def get_images(dir_path, level="debug"):
#     logger.log(level, "Getting subdirs from {}", dir_path)
#     directories = [] # an empty list to append to
    
#     # For this directory, look through and find all the children
#     for entity in os.listdir(dir_path.resolve()):
#         logger.log(level, "Found entity: {entity}",  entity = entity )
        
        
#         # if a child is found that is an image (acceptable extension), add it to the list. Otherwise, do nothing.
#         if (dir_path / entity).is_dir :
#             logger.log(level, "Found directory: {entity}", entity = entity)
#             directories.append(Path(entity))
      
#     logger.log(level, "In total, found the directories {}", str(directories))
    
#     # return the built up list
#     return directories



# THE STORY BEGINS
def main():
    logger.info("Looking through era level")
    eras = get_subdirs(root, level="ERA")

    #usually the directory names comes in the format of YYMMDD
    logger.info("Looking through event level")
    for era in eras:
        logger.log("ERA", "Doing era: {}", era)
        events = get_subdirs(era, level="EVENT")

        # get the event info to rename the folder
        for event in events:
            # abs_path = str(event.absolute)
            # date = re.search(r"*(\d){6}*", abs_path) #folders usually have the date in them in the form of YYMMDD
            logger.info("Doing event: {}", event)


    #rename all the files inside the folders here
            


if __name__ == "__main__":
    main()