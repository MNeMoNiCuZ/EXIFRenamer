# Check for required packages and install if necessary
required_packages = {'PIL': 'Pillow', 'configparser': 'configparser'}

for package, install_name in required_packages.items():
    try:
        __import__(package)
    except ImportError:
        print(f"Package {package} is not installed.")
        install_prompt = input(f"Do you want to install {package}? (y/n): ")
        if install_prompt.lower() == 'y':
            import subprocess
            subprocess.run(["pip", "install", install_name])
        else:
            print(f"Exiting. {package} is required to run this program.")
            exit()

from PIL import Image
import os
import sys
import re
import configparser

# Mapping from full technical names to user-friendly names
name_mapping = {
    'Positive': 'Positive',
    'Negative': 'Negative',
    'Steps': 'Steps',
    'Sampler': 'Sampler',
    'CFG scale': 'CFG',
    'Seed': 'Seed',
    'Size': 'Size',
    'Model': 'Model',
    'Denoising strength': 'Denoise',
    'Clip skip': 'Clip',
    'Hires upscale': 'Hires',
    'Hires steps': 'HiresSteps',
    'Hires upscaler': 'HiresUpscaler',
    'Lora hashes': 'Loras'
}

# Initialize or clear the log file
def initialize_log():
    with open("rename_log.txt", "w") as log_file:
        log_file.write("Rename Log\n")
        log_file.write("="*50 + "\n")

# Function to log activity
def log_activity(message):
    with open("rename_log.txt", "a") as log_file:
        log_file.write(message + "\n")

# Read settings file
def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    settings = {}
    try:
        settings['delimiter'] = config.get('Settings', 'delimiter').strip('"')
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("Failed to read delimiter from settings.ini, using default delimiter '_'")
        settings['delimiter'] = '_'

    try:
        settings['keep_original_name'] = config.getboolean('Settings', 'KeepOriginalName')
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("Failed to read KeepOriginalName from settings.ini, using default True")
        settings['keep_original_name'] = True

    return settings



def get_dragged_items():
    return sys.argv[1:]

def check_file_count(files):
    return len(files) > 0

def read_exif(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image.info
        image.close()
        return exif_data
    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return None


# Updated parse_exif function to correctly parse Positive and Negative
def parse_exif(exif_data):
    if exif_data is None:
        print("Warning: No EXIF data found.")
        return {}
    
    parsed_data = {}
    try:
        if 'parameters' in exif_data:
            params = exif_data['parameters']
            
            # Define all the full technical keys we are interested in, except Positive and Negative
            keys = ['Steps:', 'Sampler:', 'CFG scale:', 'Seed:', 'Size:', 'Model:',
                    'Denoising strength:', 'Clip skip:', 'Hires upscale:', 'Hires steps:',
                    'Hires upscaler:', 'Lora hashes:']
            
            # Initialize a dict to store starting index of each key in the params string
            key_indices = {}
            for key in keys:
                key_indices[key] = params.find(key)
            
            # Sort keys based on their index in the params string
            sorted_keys = sorted(keys, key=lambda k: key_indices[k])
            
            for i in range(len(sorted_keys)):
                start_key = sorted_keys[i]
                end_key = sorted_keys[i + 1] if i + 1 < len(sorted_keys) else None
                
                start_index = key_indices[start_key] + len(start_key)
                end_index = key_indices[end_key] if end_key else None
                
                value = params[start_index:end_index].strip().split(',')[0] if end_index else params[start_index:].strip()
                
                # Remove ':' from the key name and store the value in parsed_data
                parsed_data[start_key.rstrip(':')] = value

            # Tailored parsing for Positive and Negative
            positive_end_index = params.find('Negative prompt:')
            negative_start_index = positive_end_index + len('Negative prompt:')
            negative_end_index = params.find('Steps:')
            
            parsed_data['Positive'] = params[:positive_end_index].strip()
            parsed_data['Negative'] = params[negative_start_index:negative_end_index].strip()
            
    except Exception as e:
        print(f"Warning: Could not parse some EXIF data. Error: {e}")
    
    return parsed_data



# Updated get_user_choice function for cleaner display
def get_user_choice(parsed_data, keep_original_name): 
    available_keys = list(name_mapping.values())
    
    while True:
        print("Available EXIF data keys (Example values from the first file):\n")
        for i, key in enumerate(available_keys):
            technical_name = [tech_name for tech_name, user_name in name_mapping.items() if user_name == key][0]
            example_value = parsed_data.get(technical_name, "N/A")
            print(f"{i+1:2}. {key:15}: {example_value}")

        try:
            key_choice = int(input("\nWhich EXIF data would you like to add to the file name? (Enter the number) "))
            if 1 <= key_choice <= len(available_keys):
                chosen_key = available_keys[key_choice - 1]
                break
            else:
                print("\n\nInvalid choice. Please enter a number between 1 and {}.\n\n".format(len(available_keys)))
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if keep_original_name:
        while True:
            print("Choose the position:")
            print("1. Prefix")
            print("2. Suffix")
            try:
                position_choice = int(input("Enter your choice (1/2): "))
                if position_choice in [1, 2]:
                    position = "Prefix" if position_choice == 1 else "Suffix"
                    break
                else:
                    print("\n\nInvalid choice. Please enter either 1 or 2.\n\n")
            except ValueError:
                print("\n\nInvalid input. Please enter a number.\n\n")

        return chosen_key, position
    else:
        return chosen_key, None



def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def rename_files(directory, filenames, parsed_data, chosen_key, position, delimiter, keep_original_name, max_length=200):
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        new_key_value = sanitize_filename(str(parsed_data[chosen_key]))

        # Truncate the new_key_value if it's too long
        if len(new_key_value) > max_length:
            new_key_value = new_key_value[:max_length]

        if not keep_original_name:
            new_name = f"{new_key_value}{ext}"
        else:
            if position == "Prefix":
                new_name = f"{new_key_value}{delimiter}{name}{ext}"
            else:
                new_name = f"{name}{delimiter}{new_key_value}{ext}"

        # Check for file name collision and resolve
        counter = 1
        original_new_name = new_name
        while os.path.exists(os.path.join(directory, new_name)):
            new_name = f"{original_new_name.split('.')[0]}_{counter}.{original_new_name.split('.')[1]}"
            counter += 1

        try:
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
            print(f"\nFile {os.path.join(directory, filename)} renamed to {new_name}.")
            log_activity(f"File {os.path.join(directory, filename)} renamed to {new_name}.")
        except Exception as e:
            print(f"Could not rename {filename}. Error: {e}")
            log_activity(f"Could not rename {filename}. Error: {e}")


# Function to find all files in a directory recursively
def find_files_recursive(folder, file_ext):
    found_files = []
    for root, dirs, files in os.walk(folder):
        print(f"Searching in folder: {root}")  # Temporary print statement for debugging
        for file in files:
            if file.lower().endswith(file_ext):
                full_path = os.path.join(root, file)
                found_files.append(full_path)
                print(f"Found file: {full_path}")
    return found_files

#ask the user for a path
def get_user_input_path():
    path = input("You can also drag/drop files and folders to this script.\nPlease enter a file or folder path: ")
    return path.strip()


def main():
    print("Script started.")
    log_activity("Script started.")
    log_activity(f"Settings: {read_settings()}")
    failed_files = []  # List to hold paths of files that couldn't be renamed

    # Reading settings from settings.ini
    settings = read_settings()
    delimiter = settings['delimiter']
    keep_original_name = settings['keep_original_name']

    dragged_items = get_dragged_items()

    # If no files are dragged onto the script, ask the user for a directory or file path
    if not dragged_items:
        user_input = input("Please enter the path to a file or directory: ").strip()
        if os.path.exists(user_input):
            dragged_items = [user_input]
        else:
            print("Invalid path. Exiting.")
            return

    if not check_file_count(dragged_items):
        print("User chose not to proceed due to file count.")
        return

    # Get sample EXIF data for the user to choose from
    image_files = []
    for item in dragged_items:
        if os.path.isdir(item):
            image_files.extend(find_files_recursive(item, '.png'))
        else:
            image_files.append(item)
    
    if not image_files:
        print("No PNG files found. Exiting.")
        return

    sample_file = image_files[0]
    sample_exif_data = read_exif(sample_file)
    sample_parsed_data = parse_exif(sample_exif_data)

    chosen_key, position = get_user_choice(sample_parsed_data, keep_original_name)

    # Translate back to the full technical name
    chosen_technical_key = [tech_name for tech_name, user_name in name_mapping.items() if user_name == chosen_key][0]

    for item in dragged_items:
        if os.path.isdir(item):
            image_files = find_files_recursive(item, '.png')
        else:
            image_files = [item]

        for image_file in image_files:
            exif_data = read_exif(image_file)
            if exif_data is None:
                print(f"Skipping file {image_file} due to lack of EXIF data.")
                failed_files.append(image_file)
                continue

            parsed_data = parse_exif(exif_data)
            rename_files(os.path.dirname(image_file), [os.path.basename(image_file)], parsed_data, chosen_technical_key, position, delimiter, keep_original_name)

    print("Script finished.")
    if failed_files:
        print("\nThe following files could not be renamed due to lack of EXIF data:")
        for file in failed_files:
            print(file)
    log_activity("Script finished.")
    print("Press any key to exit.")
    input()



if __name__ == "__main__":
    main()