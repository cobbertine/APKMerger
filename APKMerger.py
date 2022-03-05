from io import SEEK_SET
import os
import shutil

BASE_APK_FOLDER_SUBSTRING = "base.apk"
SPLIT_APK_FOLDER_SUBSTRING = "split_config"
XML_RES_END_TAG = "</resources>"
LINE_FILTER_KEYWORD = "APKTOOL_DUMMY"
YAML_FILE_NAME = "apktool.yml"
YAML_FILE_DONOTCOMPRESS_TAG = "doNotCompress:"
YAML_FILE_DATA_PREFIX = "-"
ANDROID_MANIFEST_FILE_NAME = "AndroidManifest.xml"
ANDROID_MANIFEST_SPLIT_TAG = "android:isSplitRequired=\"true\""

def get_path_to_values_folder(parent_directory):
    PATH_TO_VALUES_FOLDER = ["res", "values"]
    return os.path.join(*([parent_directory] + PATH_TO_VALUES_FOLDER))

def skip_copy_decider(dir_path, list_of_files):
    dir_path_norm = os.path.normpath(dir_path)
    dir_path_split = dir_path_norm.split(os.sep)
    dir_path_split[0] = base_apk_folder_name
    base_apk_folder_path = os.path.join(*dir_path_split)
    ignore_file_list = []
    try:
        base_apk_files = os.listdir(base_apk_folder_path)
        for file in list_of_files:
            if file in base_apk_files and not os.path.isdir(os.path.join(dir_path, file)):
                ignore_file_list.append(file)
                print("Skipping {FILE_PATH}".format(FILE_PATH=os.path.join(base_apk_folder_path, file)))
    except:
        pass
    return ignore_file_list


print("Getting Base APK and Split APK directories...")

base_apk_folder_name = ""
split_apk_folder_names = []

apk_fragments = list(filter(lambda item : os.path.isdir(item), os.listdir()))

for fragment in apk_fragments:
    if BASE_APK_FOLDER_SUBSTRING in fragment:
        base_apk_folder_name = fragment
    elif SPLIT_APK_FOLDER_SUBSTRING in fragment:
        split_apk_folder_names.append(fragment)


print("Getting XML files under /res/values/ for the Base APK and Split APKs...")

base_apk_xml_files = list(filter(lambda item: ".xml" in os.path.splitext(item), os.listdir(get_path_to_values_folder(base_apk_folder_name))))

split_apks_xml_files = {}

for split_apk_folder_name in split_apk_folder_names:
    try:
        split_apks_xml_files[split_apk_folder_name] = list(filter(lambda item: ".xml" in os.path.splitext(item), os.listdir(get_path_to_values_folder(split_apk_folder_name))))
    except:
        pass

print("Updating Base APK's XML files with Split APKs' XML files if required (any required update will be printed)...")

for split_apk_folder_name in split_apk_folder_names:
    if split_apk_folder_name in split_apks_xml_files:
        for xml_file_name in split_apks_xml_files[split_apk_folder_name]:
            if xml_file_name in base_apk_xml_files:
                print("{SPLIT_APK_FOLDER_NAME} has {XML_FILE_NAME}. Will merge new lines with Base APK if required (any required update will be printed)...".format(SPLIT_APK_FOLDER_NAME=split_apk_folder_name, XML_FILE_NAME=xml_file_name))
                base_apk_xml_file_data = []
                with open(os.path.join(get_path_to_values_folder(base_apk_folder_name), xml_file_name)) as xml_file_pointer:
                    base_apk_xml_file_data = xml_file_pointer.readlines()
                split_apk_xml_file_data = []
                with open(os.path.join(get_path_to_values_folder(split_apk_folder_name), xml_file_name)) as xml_file_pointer:
                    split_apk_xml_file_data = xml_file_pointer.readlines()
                insert_index = list(filter(lambda index : index != -1, map(lambda item : base_apk_xml_file_data.index(item) if XML_RES_END_TAG in item else -1, base_apk_xml_file_data)))[0]
                for line in split_apk_xml_file_data:
                    if XML_RES_END_TAG not in line and LINE_FILTER_KEYWORD not in line and line not in base_apk_xml_file_data:
                        print("New line will be written to Base APK: {LINE}".format(LINE=line).rstrip())
                        base_apk_xml_file_data.insert(insert_index, line)
                        insert_index = insert_index + 1
                filtered_base_apk_xml_file_data = list(filter(lambda item : LINE_FILTER_KEYWORD not in item, base_apk_xml_file_data))
                print("Writing changes (if any) to disk...")
                with open(os.path.join(get_path_to_values_folder(base_apk_folder_name), xml_file_name), "w") as xml_file_pointer:
                    xml_file_pointer.writelines(filtered_base_apk_xml_file_data)

print("APKTOOL_DUMMY placeholder values removed from the Base APK's updated XML files")
print("Retrieving doNotCompress data from Split APKs' apktool.yml file...")

split_apks_yaml_donotcompress_data = []

for split_apk_folder_name in split_apk_folder_names:
    with open(os.path.join(split_apk_folder_name, YAML_FILE_NAME)) as yaml_file_pointer:
        yaml_file_data = yaml_file_pointer.readlines()
        start_index = list(filter(lambda index : index != -1, map(lambda item : yaml_file_data.index(item) if YAML_FILE_DONOTCOMPRESS_TAG in item else -1, yaml_file_data)))[0] + 1
        end_index = list(filter(lambda index : index != -1, map(lambda item : yaml_file_data.index(item) if YAML_FILE_DATA_PREFIX not in item else -1, yaml_file_data[start_index:])))[0]
        split_apks_yaml_donotcompress_data = split_apks_yaml_donotcompress_data + yaml_file_data[start_index : end_index]

print("Updating Base APK's apktool.yml file with Split APKs' if required (any required update will be printed)...")

base_apk_updated_yaml_file_data = []

with open(os.path.join(base_apk_folder_name, YAML_FILE_NAME), "r") as yaml_file_pointer:
    yaml_file_data = yaml_file_pointer.readlines()
    yaml_file_pointer.seek(SEEK_SET)
    start_index = list(filter(lambda index : index != -1, map(lambda item : yaml_file_data.index(item) if YAML_FILE_DONOTCOMPRESS_TAG in item else -1, yaml_file_data)))[0] + 1
    end_index = list(filter(lambda index : index != -1, map(lambda item : yaml_file_data.index(item) if YAML_FILE_DATA_PREFIX not in item else -1, yaml_file_data[start_index:])))[0]    
    base_apk_donotcompress_data = yaml_file_data[start_index : end_index]
    split_apks_yaml_donotcompress_data_uniqued = list(set(list(filter(lambda data : data not in base_apk_donotcompress_data, split_apks_yaml_donotcompress_data))))
    print("Will write the following doNotCompress data to Base APK: {DONOTCOMPRESS_DATA}".format(DONOTCOMPRESS_DATA=split_apks_yaml_donotcompress_data_uniqued).rstrip())
    base_apk_updated_yaml_file_data = yaml_file_data[:start_index] + split_apks_yaml_donotcompress_data_uniqued + yaml_file_data[start_index:]

print("Writing changes (if any) to disk...")

with open(os.path.join(base_apk_folder_name, YAML_FILE_NAME), "w") as yaml_file_pointer:
    yaml_file_pointer.writelines(base_apk_updated_yaml_file_data)

print("Copying all files from Split APKs into Base APK folder. No overwriting will occur...")

for split_apk_folder_name in split_apk_folder_names:
    shutil.copytree(split_apk_folder_name, base_apk_folder_name, ignore=skip_copy_decider, dirs_exist_ok=True)

print("Updating Base APK's AndroidManifest.xml file to remove {TAG}...".format(TAG=ANDROID_MANIFEST_SPLIT_TAG))

base_apk_updated_android_manifest_data = []

with open(os.path.join(base_apk_folder_name, ANDROID_MANIFEST_FILE_NAME), "r") as android_manifest_file:
    android_manifest_data = android_manifest_file.readlines()
    android_manifest_file.seek(SEEK_SET)
    base_apk_updated_android_manifest_data = list(map(lambda line : line.replace(ANDROID_MANIFEST_SPLIT_TAG, "") if ANDROID_MANIFEST_SPLIT_TAG in line else line, android_manifest_data))

with open(os.path.join(base_apk_folder_name, ANDROID_MANIFEST_FILE_NAME), "w") as android_manifest_file:
    android_manifest_file.writelines(base_apk_updated_android_manifest_data)

print("All tasks complete. Rebuild with APKTool when ready.")