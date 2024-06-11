import csv
import os


class Pinterest:
    UPLOADING_DATA_FILE = 'uploading_data.csv'
    GENERATOR_DATA_FILE = 'generator_data.csv'
    IMAGE_PROMPTS_FILE = 'image_prompts.csv'
    VIDEO_PROMPTS_FILE = 'video_prompts.csv'

    WRITER_MODE_1 = 'video'
    WRITER_MODE_2 = 'image'

    GENERATOR_MODE_1 = 'template_1'
    GENERATOR_MODE_2 = 'template_2'

    def __init__(self, project_folder):
        self.project_path = os.path.join(os.path.abspath('projects'), project_folder)
        self.prompts_path = os.path.join(self.project_path, 'prompts')
        self.data_path = os.path.abspath('data')

        # Ensure that folder exists
        os.makedirs(self.project_path, exist_ok=True)
        os.makedirs(self.prompts_path, exist_ok=True)
        os.makedirs(self.data_path, exist_ok=True)

    def open_csv(self, file_name):
        # get the path to the file
        data_file_path = self._get_data_file_path(file_name)

        # Check if file exist and raise error if not found
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"File {file_name} not found in: {data_file_path}")
        
        # Check the delimiter of csv file
        delimiter = self._check_csv_delimiter(data_file_path)

        # Save results to the list
        result = []

        # Open CSV file for reading
        with open(data_file_path, 'r', encoding='utf-8', newline='') as data:
            # Read the heading 1st row from csv file
            heading = next(data)

            # Create a CSV reader object with the specified delimiter
            reader = csv.reader(data, delimiter=delimiter)

            # Iterate over each row in CSV file
            for row in reader:
                if file_name == self.VIDEO_PROMPTS_FILE:
                    row_dict = {
                        'keyword': row[0],
                        'title_prompt': row[1],
                        'description_prompt': row[2]
                    }
                    
                    result.append(row_dict)

                elif file_name == self.IMAGE_PROMPTS_FILE:
                    row_dict = {
                        'keyword': row[0],
                        'title_prompt': row[1],
                        'description_prompt': row[2],
                        'tips_prompt': row[3]
                    }
                    
                    result.append(row_dict)

                elif file_name == self.GENERATOR_DATA_FILE:
                    row_dict = {
                        'mode': row[0],
                        'keyword': row[1],
                        'title': row[2],
                        'description': row[3],
                        'tips': row[4]
                    }

                    result.append(row_dict)

                else: 
                    raise ValueError(f'Invalid filename: {file_name}. Check the available file names in the base class')
        return result

    def write_csv(self, data, file_name):
    
        # Get the full path to the data file
        data_file_path = self._get_data_file_path(file_name)

        file_exits = os.path.isfile(data_file_path)
        file_empty = os.path.exists(data_file_path) and os.stat(data_file_path).st_size == 0
        # Define the header for uploading data
        uploading_data_header = ['mode', 'keyword', 'title', 'description', 'file_path', 'board_name', 'pin_link']

        # Write the header if the file is empty
        # if os.path.isfile(data_file_path) and os.stat(data_file_path).st_size == 0:
        if not file_exits or file_empty:
            self._write_header(data_file_path, uploading_data_header)

        # Define the order of the fields for writing 
        order = ['mode', 'keyword', 'title', 'description', 'file_path', 'board_name', 'pin_link']

        # Insert tips field for the generator_data.csv
        if file_name == self.GENERATOR_DATA_FILE:
            order.insert(4, 'tips')

        # Open the data file for appending and write the data
        with open(data_file_path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=order, delimiter=';')
            writer.writerow(data)

        # Log a success message after writting the data 
        self._log_method(f'Data has been successfully written to {file_name}.\n')    



    def _check_csv_delimiter(self, file_path):
        # Open the file in read mode
        with open(file_path, "r") as file:
            # read 1st line and remove white spaces
            first_line = file.readline().strip()

            # check for commas as delimiter
            if ',' in first_line:
                return ','
            # Check for semicolon delimiter
            elif ';' in first_line:
                return ','
            else:
                return ','


    def _get_data_file_path(self, file_name):
        if file_name in [self.VIDEO_PROMPTS_FILE, self.IMAGE_PROMPTS_FILE]:
            # If file name correcponds to prompts, return the path within the prompts dir
            return os.path.join(self.project_path, self.prompts_path, file_name)
        else: 
            # Otherwise return the path from project directory
            return os.path.join(self.project_path, file_name)

    @staticmethod
    def _write_header(file_path, header):
        with open(file_path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(header)

    # Static methods for logging errors and messages
    @staticmethod
    def _log_method(message):
        print(message)


    @staticmethod
    def _log_error(message, error):
        # ANSI escape codes for red color and reset
        red_color = "\033[91m"
        reset_color = "\033[0m"

        # Print the error message in red color
        print(f'{red_color}{message}{reset_color}\n{error}\n')    