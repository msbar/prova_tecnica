import os


class FilesHandler():
    _dirs_path = None
    _dirs = None
    _files = None
    _files_list = None

    def __init__(self, root_dir):
        self._root_dir = root_dir
        self._walk_root_dir()

    def _walk_root_dir(self):
        for (dirs_path, dirs, files) in os.walk(self._root_dir):
            self._dirs_path = dirs_path
            self._dirs = dirs
            self._files = files
            self._files_list = [os.path.join(dirs_path, file) for file in files]
            self._files_list.sort()

    def get_dirs_path(self):
        return self._dirs_path

    def get_dirs(self):
        return self._dirs

    def get_files(self):
        return self._files

    def get_files_list(self):
        return self._files_list

    def get_file_from_full_path(self, full_path):
        return os.path.split(full_path)[-1]
