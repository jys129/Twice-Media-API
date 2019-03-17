import os
from pathlib import Path
from loguru import logger


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

eras = ['']

# Finds all the subdirectories
# and returns it in a python list
def get_subdirs(dir_path, level="debug"):
    logger.log(level, "Getting subdirs from {}", dir_path)
    directories = [] # a list to append to

    for entity in os.listdir(dir_path):
        logger.log(level, "Found entity: {entity}",  entity = entity )
        if os.path.isdir(entity):
            logger.log(level, "Found directory: {entity} ", entity = entity)
            directories.append(Path(entity))

    logger.log(level, "In total, found the directories {}", directories)
    
    return directories



#
# MAIN program start (I should probably put this all into main...)
#


logger.info("Looking through era level")
eras = get_subdirs(root, level="ERA")

#usually the directory names comes in the format of YYMMDD
logger.log("EVENT", "Looking through event level")
for era in eras:
    logger.info("Doing era: {}", era)
    events = get_subdirs(era, level="EVENT")
    for event in events:
        logger.info("Doing event: {}", event)
