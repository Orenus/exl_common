import os

from exl_base_app.exl_logger import ExlLogger


def rotate_folder(rotate_dir_path, max_kept_files):
    """
    This function gets a folder path and a maximum number of files that should be kept in the
    folder. It deletes the older files when the number of the files are bigger than
    'num_of_kept_files'.
    :param logger: Log object to report when XML was deleted.
    :param rotate_dir_path: The path to the rotated folder.
    :param max_kept_files: Max number of files in the rotated folder.
    :return: 0 On success and 1 otherwise.
    """

    logger = ExlLogger.instance()

    def get_folder_details():
        list_of_files = os.listdir(rotate_dir_path)
        full_path_files_list = [
            "{}/{}".format(rotate_dir_path, x) for x in list_of_files]
        return full_path_files_list

    folder_files = get_folder_details()

    while len(folder_files) > max_kept_files:
        oldest_file = min(folder_files, key=os.path.getctime)
        logger.info("Removed old XML from:" + str(oldest_file))

        try:
            os.remove(oldest_file)

        except OSError as e:
            msg = "{} {}".format(str(e), " - Please delete this file "
                                 "manually")
            logger.error(msg)
            return

        folder_files = get_folder_details()
