import itertools
import shutil
from datetime import datetime
import os
from glob import glob

import settings
import core


# -----------------------------------------------------------------------------


def _hook(item: str) -> str:
    """
    Hook for sorting and groupby functions according to file extension

    :param item: Full file path
    :return: File extension
    """

    return os.path.splitext(item)[-1][1:]


# Hierarchy functions ---------------------------------------------------------


def _create_file_template(context: core.Context, directory: str) -> list:
    """
    Create a file template according to the file extension

    Example:
        {
            'name': 'DPX',
            'type': 'folder',
            'children': [
                {
                    'name': 'PROJECT_X_SHOT_A_TASK_A.0000.dpx',
                    'type': 'file',
                    'input': 'D:\\Work\\PROJECT_X_SHOT_A_TASK_A.0000.dpx'
                }
            ]
        }

    :param context: Current context
    :param directory: Input directory (Where delivery files exists)
    :return: <type 'list'>
    """

    template = []
    glob_template = os.path.join(
        directory,
        settings.FILE_FORMAT.format(context=context)
    )

    for key, grouper in itertools.groupby(
            sorted(glob(glob_template), key=_hook), key=_hook
    ):
        children = []

        for item in grouper:
            children.append(
                {
                    "name": os.path.basename(item),
                    "type": "file",
                    "input": item
                }
            )

        template.append(
            {
                "name": key.upper(),
                "type": "folder",
                "children": children
            }
        )

    return template


# -----------------------------------------------------------------------------


# Main directory hierarchy
BASE_HIERARCHY = {
    "name": lambda context, directory:
        f"{context.project}",
    "type": "folder",
    "children": [
        {
            "name": lambda context, directory:
                datetime.now().strftime(settings.DATE_FORMAT),
            "type": "folder",
            "children": [
                {
                    "name": lambda context, directory:
                        f"{context.project}_{context.shot}",
                    "type": "folder",
                    "children": [
                        {
                            "name": lambda context, directory:
                                f"{context.task}",
                            "type": "folder",
                            "children": lambda context, directory:
                                _create_file_template(context, directory)
                        }
                    ]
                }
            ]
        }
    ]
}


# -----------------------------------------------------------------------------


def _resolve(d: dict, context: core.Context, directory: str) -> dict:
    """
    Resolve the input dictionary by looping over the items are replace the
    callable values with callable return value

    :param d: Input dictionary
    :param context: Current context
    :param directory: Input directory
    :return: <type 'dict'>
    """

    new_d = {}

    for key, value in d.items():
        if isinstance(value, dict):
            new_d.update({key: _resolve(value, context, directory)})

        if isinstance(value, list):
            new_l = []

            for item in value:
                new_l.append(_resolve(item, context, directory))

            new_d.update({key: new_l})

        else:
            new_d.update(
                {key: value(context, directory) if callable(value) else value})

    return new_d


# Dynamically name the directories and files
def get(context: core.Context, directory: str) -> dict:
    """
    Create the base hierarchy by resolving all values

    :param context: Current context
    :param directory: Input directory
    :return: <type 'dict'>
    """

    return _resolve(BASE_HIERARCHY, context, directory)


def create(template: dict, directory: str) -> dict:
    """
    Create the file, folder structure in template

    :param template: Template file
    :param directory: Root directory
    :return: <type 'dict'>
    """

    result = {
        "status": True,
        "message": ""
    }

    for item in template if isinstance(template, list) else [template]:
        if item["type"] == "file":
            # Copy the input file to  directory
            shutil.copy(item["input"], directory)

        elif item["type"] == "folder":
            folder = os.path.join(directory, item["name"])

            # Create the folder in current directory
            if not os.path.exists(folder):
                os.mkdir(folder)

            if "children" in item:
                create(item["children"], os.path.join(directory, item["name"]))

        else:
            pass

    return result
