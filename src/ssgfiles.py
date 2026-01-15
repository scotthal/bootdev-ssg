import os
import os.path
import shutil


def recursive_delete(path):
    if not os.path.exists(path):
        return
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a directory.")
    if os.path.samefile(os.getcwd(), path):
        raise ValueError("Refusing to delete the current directory.")

    traverse(path,
             visit_file_function=delete_file,
             post_directory_function=delete_directory)


def recursive_copy(source_path, destination_path):
    if not os.path.exists(source_path):
        raise ValueError(f"{source_path} does not exist")
    if not os.path.isdir(source_path):
        raise ValueError(f"{source_path} is not a directory")

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)

    traverse(source_path,
             visit_file_function=copy_file,
             pre_directory_function=create_directory,
             data={"destination_root_path": destination_path})


def copy_file(root_path, rest_path, data):
    source_path = os.path.join(root_path, rest_path)
    destination_path = os.path.join(data["destination_root_path"], rest_path)
    print(f"Copy file {source_path} to {destination_path}")
    shutil.copy(source_path, destination_path)


def create_directory(root_path, rest_path, data):
    destination_path = os.path.join(data["destination_root_path"], rest_path)
    print(f"Create directory {destination_path}")
    os.mkdir(destination_path)


def delete_file(root_path, rest_path, data):
    full_path = os.path.join(root_path, rest_path)
    print(f"Delete file: {full_path}")
    os.unlink(full_path)


def delete_directory(root_path, rest_path, data):
    full_path = os.path.join(root_path, rest_path)
    print(f"Delete directory: {full_path}")
    os.rmdir(full_path)


def pass_function(root_path, rest_path, data):
    pass


def traverse(root_path,
             rest_path="",
             data=None,
             visit_file_function=pass_function,
             pre_directory_function=pass_function,
             post_directory_function=pass_function):
    current_directory = os.path.join(root_path, rest_path)
    contents = os.listdir(current_directory)
    for entry in contents:
        entry_rest_path = os.path.join(rest_path, entry)
        entry_full_path = os.path.join(current_directory, entry)
        if os.path.isdir(entry_full_path):
            pre_directory_function(root_path, entry_rest_path, data)
            traverse(root_path, entry_rest_path, data, visit_file_function,
                     pre_directory_function, post_directory_function)
            post_directory_function(root_path, entry_rest_path, data)
        else:
            visit_file_function(root_path, entry_rest_path, data)
