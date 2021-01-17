import os

FRAME_PADDING = 4
FILE_FORMAT = f"{{context.project}}_{{context.shot}}_{{context.task}}." \
              f"{'?' * FRAME_PADDING}.*"
DATE_FORMAT = "%Y%m%d%H%M"
RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "resources")
