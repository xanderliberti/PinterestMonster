import os
from google.oauth2.service_account import Credentials
import gspread
from openai import OpenAI
from modules.base import Pinterest
# 16im6AB70bfjb-rg4k3y71XQYKn-aRd-71xB13pK7p00
# sk-proj-iKUf8W3dIMhZisoID5MXT3BlbkFJJtdvY043jjPk5CEaKesR

class Writer(Pinterest):
    def __init__(self, project_folder):
        super().__init__(project_folder)
        # self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.client = OpenAI(api_key="sk-proj-iKUf8W3dIMhZisoID5MXT3BlbkFJJtdvY043jjPk5CEaKesR")

    def open_data(self, mode, google_sheet=True, table_id=None):
        if google_sheet: 
            # If the value is true read data from google sheets API

            # Obtain Google Sheets credentials
            creds =  self._get_google_creds()

            # Authorize connection using gspread
            client = gspread.authorize(creds)

            # Open  google sheets table  using its key
            table = client.open_by_key(table_id)
            print('TABLE ', table)    
            # Choose the appropriete work sheet based on the mode (image or video)
            if mode == self.WRITER_MODE_2:
                worksheet = table.get_worksheet(2)
                print('TABLE ', worksheet)
            elif mode == self.WRITER_MODE_1:
                worksheet = table.get_worksheet(1)
                print('TABLE ', worksheet)
            else: 
                raise ValueError(f'Invalid mode: {mode}. Please set the mode to "image" or "video"')

            # Retrieve all values from the chosen worksheet
            all_values = worksheet.get_all_values()

            # Parse  the  rows and obtain the data based on the mode
            data = self._parse_rows(all_values, mode)

        else: 
            # Read data from CSV file
            if mode == self.WRITER_MODE_2:
                filename = self.IMAGE_PROMPTS_FILE
            elif mode == self.WRITER_MODE_1:
                filename = self.VIDEO_PROMPTS_FILE 
            else:
                raise ValueError(f'Invalid mode: {mode}. Please set mode to video or image')


            # Open csv file with the specific file name
            data = self.open_csv(filename)

        return data
    
    @staticmethod
    def _parse_rows(rows, mode):
        data = []

        for index, row in enumerate(rows):
            
            if index == 0:
                continue
            
            row_dict = {
                'keyword': row[0],
                'title_prompt': row[1],
                'description_prompt': row[2]
            }

            # Add 'tips_prompt; to the dictionaty if mode is 'image'
            if mode == 'image':
                row_dict['tips_prompt'] = row[3]
            
            # print(row_dict)
            data.append(row_dict)

        return data

    def _get_google_creds(self):
        # Specify the path to the JSON key file
        json_key_path = os.path.join(self.data_path, 'keyfile.json')

        # Define the rewquired OAuth2.0 scopes for Google Sheets API
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Create the credentials object based on the JSON file
        creadentials = Credentials.from_service_account_file(json_key_path, scopes=scopes)

        return creadentials

    def write_single_prompt(self, prompt):
        # Create ChatComplition instance from g4t module using openAI 
        # Generates content based on the provided prompt
        # The prompt is set as a user message in the 'messages' parameter
        # response = g4f.ChatCompletion.create(
        #     model = g4f.models.gpt_35_turbo,
        #     messages=[{'role': 'user', 'content': prompt}]
        # )
        
        completion = self.client.chat.completions.create(
            # model="gpt-4o",
            model='gpt-3.5-turbo',
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content.strip('"')


    def write(self, row, mode):
        # Check if the mode is valid
        print('Write methodv =>> Mode:', mode)
        print('Row >>>>', row)
        if mode not in [self.WRITER_MODE_1, self.WRITER_MODE_2]:
            raise ValueError(f'Invalid mode: {mode}. Please set the mode to "image" or "video"')
        
        # Initialize the results dictionary with default values
        results = {
            'mode': mode,
            'keyword': '',
            'title': '',
            'description': '',
            'tips': '', 
        }

        try:
            # Extract keyword from the row or set it to an empty string if not present
            results['keyword'] = row.get('keyword', '')

            # write title and log the process
            self._log_method('Writing title...')

            # Extract title prompt
            title_prompt = row.get('title_prompt', '')
            title = self.write_single_prompt(title_prompt)
            # results['title'] = title.strip('"') if title else ''
            results['title'] = title if title else ''

            # write description and log the process
            self._log_method("Writting description...")
            # replace 'SELECTED TITLE' in the description prompt with generated title
            description_prompt = row.get('description_prompt', '') \
                .replace('SELECTED TITLE', title if title else row.get('keyword', ''))
            
            description = self.write_single_prompt(description_prompt)
            # results['description'] = description.strip('"') if description else ''
            results['description'] = description if description else ''


            # # Write tips for image mode and log the process
            # self._log_message('Writting tips...')
            if mode == self.WRITER_MODE_2:
                # Write tips for image mode and log the process
                self._log_method('Writting tips...')

                # Replace 'SELECTED TITLE' in the tips prompt with generated title
                tips_prompt = row.get('tips_prompt', '')\
                    .replace('SELECTED TITLE', title if title else row.get('keyword', ''))
                
                tips = self.write_single_prompt(tips_prompt)
                # results['tips'] = tips.strip('"') if tips else ''
                results['tips'] = tips if tips else ''

        except Exception as e:
            self._log_error(f'Error while writting: ', e)

        # Determine file name based on the mode and wrote the results to the corresponding file
        filename = self.GENERATOR_DATA_FILE if mode == self.WRITER_MODE_2 else self.UPLOADING_DATA_FILE
        self.write_csv(results, filename)