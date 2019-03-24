import os
from pathlib import Path
from loguru import logger
import re
import utils
import shutil

root = Path(".")

member_level = logger.level("MEMBER", no=38, color="<green>", icon="💦")
era_level = logger.level("ERA", no=38, color="<yellow>", icon="📀")
event_level = logger.level("EVENT", no=38, color="<blue>", icon="🎥")
sub_event_level = logger.level("SUB-EVENT", no = 38, color = "<magenta>")
setup_level = logger.level("SETUP", no=38, color="<white>", icon="🔨")

ACCEPTABLE_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
ACCEPTABLE_VIDEO_EXTENSIONS = [".mov", ".mp4"]
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
    """Gets all the subdirectories of a certain folder
    
    Arguments:
        dir_path {pathlib Path} -- The path of a directory to get the subdirectories from
    
    Keyword Arguments:
        level {loguru logger level} -- The loguru logger level to output the logs at (default: {"debug"})
    """
    logger.log(level, "Getting subdirs from {}", dir_path)
    directories = [] # a list to append to
    
    # For this directory, look through and find all the children
    for entity in os.listdir(dir_path.resolve()):
        logger.log(level, "Found entity: {entity}",  entity = entity )
        entity = Path(dir_path / entity) # Re add the path to the entity
        # if a child is found that is a directory, add it to the list. Otherwise, do nothing.
        if os.path.isdir(entity) :
            logger.log(level, "Found directory: {entity}", entity = str(entity))
            directories.append(entity)

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





def find_category(path):
    """Given a path, it finds what category the picture should be in
    
    Arguments:
        path {pathlib's Path} -- The path to an event folder
    """


    # Possible categories:
    # Concert (includes awards ceremonies), 
    # fansign (basically if the directory name includes the word "fan" in it, it's probabl, y a fansign), 
    # other (includes keywords FOR SURE that are other e.g. names of variety shows, airports)
    # manual => if the directory name doesn't contain any keywords, then it will get moved to the manual folder for human review
    # All keywords are case-insensitive
    KEYWORDS = [["concert", "sbs", "gayo", "award", "showcase", "exhibition", 
                    "mcountdown", "music core", "festival", "music bank", "kcon", 
                    "show champion",  "university"], # Concert: Not sure if "university" should belong here
                ["fan" ], # Fansign
                ["airport", "jtbc", "twicetagram", "sns", "instagram", "idol star athletics"]] # Other: Not sure if "jtbc" belongs here
    # Search through everything because why the hell not
    # n^2 for the win
    for i in range(0, 3):
        for j in range(0, len(KEYWORDS[i])):
            #TODO Reimplement with proper switches/make actual good code.
            if(KEYWORDS[i][j] in path.resolve()): 
                if j == 0:
                    return "concert"
                elif j == 1:
                    return "fan"
                elif j == 2:
                    return "other"

    return "unknown"

def setup():
    """Makes sure everything is set up and ready to be run (e.g. folders).

    Returns nothing.
    """
    # make sure manual,group directories are there
    req_dirs = ["manual", "group"]

    for req_dir in req_dirs:
        if not (root / ".." / Path(req_dir)).is_dir():
            logger.log("SETUP", "Could not find {} folder. Creating now...", req_dir)
            (root / ".." / Path(req_dir)).mkdir()
            logger.log("SETUP", "Done!")
        else:
            logger.log("SETUP", "Found {} folder sucessfully.", req_dir)


# THE STORY BEGINS
def main():
    # run the setup to make sure required folders are in place.
    setup()

    logger.info("Looking through era level")
    eras = get_subdirs(root, level="ERA")

    #usually the directory names comes in the format of "YYMMDD Title and words here"
    logger.info("Looking through event level")
    for era in eras:
        logger.log("ERA", "Doing era: {}", era)
        events = get_subdirs(era, level="EVENT")

        # get the event info to rename the folder
        for event in events:
            # Look through the subfolders in an event and extract any folders that contain "press" to 
            subdirs = get_subdirs(event, level="SUB-EVENT") # look for any subdirectories and move them to the correct location
            
            for subdir in subdirs:
                abs_path = str(subdir.resolve())

                if utils.compare_in_nocase("_press", abs_path):
                    #if the folder is a press folder, extract it to the event folder
                    logger.log("SUB-EVENT", "Moving press subdir {abs_path} to {event_dir}", abs_path = abs_path, event_dir= str(event.resolve()))
                    pass
                elif utils.compare_in_nocase("_group", abs_path):
                    logger.log("SUB-EVENT", "Moving group subdir {abs_path} to {group_dir}", abs_path = abs_path, group_dir = Path("../group/").resolve())
                    pass
                else:
                    # if it's not a group folder nor a press folder, then just remove it
                    logger.log("SUB-EVENT", "Removing event subdir {abs_path}", abs_path = abs_path) #use absolute path here because "LQ" as a folder name isn't very identifiable
                    shutil.rmtree(subdir)
                    logger.log("SUB-EVENT", "Finished removing event subdir." )

            # Move "Group" pictures to group folder
            logger.info("Doing event: {}", event)
            abs_path = str(event.resolve())
            date = re.search(r"(\d{6})", abs_path) #folders usually have the date in them in the form of YYMMDD
            logger.log("EVENT", "Date={}", date.group(1))
            


    #rename all the files inside the folders here



if __name__ == "__main__":
    main()
   