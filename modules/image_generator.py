import os
from PIL import Image
from modules.base import Pinterest
from modules.settings import Template1Settings, Template2Settings


class BaseImageGenerator(Pinterest):

    TEMPLATES = ['template_1', 'template_2']
    SUBFOLDERS = ['fonts']


    def __init__(self, project_folder, template, width=1000, height =1500, save=True, show=True, write_uploading_data=False):
        super().__init__(project_folder)
        self.template = template
        self.width = width
        self.height = height
        self.save = save
        self.show = show
        self.write_uploading_data = write_uploading_data

        self.project_assets_path = os.path.join(self.project_path, 'assets')
        self.backgrounds_path = os.path.join(self.project_assets_path, 'backgrounds')
        self.save_image_path = os.path.join(self.project_path, 'images')

        os.makedirs(self.save_image_path, exist_ok=True)
        os.makedirs(self.backgrounds_path, exist_ok=True)

        self.assets_path = os.path.join(self.data_path, 'image_assets')

        for template in self.TEMPLATES:
            template_path = os.path.join(self.assets_path, template)
            setattr(self, template, template_path)

            for subfolder in self.SUBFOLDERS:
                subfolder_path = os.path.join(template_path, subfolder)
                setattr(self, f'{template}_{subfolder}_path', subfolder_path)
                os.makedirs(subfolder_path, exist_ok=True)

        self.settings = self._get_template_settings()

        self.canvas = Image.new("RGBA", (self.width, self.height))
    
    def _get_template_settings(self):
        if self.template == self.GENERATOR_MODE_1:
            return Template1Settings()
        elif self.template == self.GENERATOR_MODE_2:
            return Template2Settings()
        else:
            raise ValueError(f"Invalid template mode: {self.template}")
        
    def _fill_background(self, color):
        # Create a drawing object to draw in the canvas
        draw = Image.Draw(self.canvas)

        #jGet the width and height of the canvas
        width, height = self.canvas.size

        # Draw a filled rectangle covering the entire canvas with specified color
        draw.rectangle((0, 0, width, height), fill=color)

    def _draw_background(self):
        if self.settings.overlay_bg:
            # Overlay an image on the background
            pass
        else:
            # or fill the background with a color
            self._fill_background(self.settings.bg_color)

    def generate_image(self, data):
        raise NotImplementedError("Subclasses must implement generate_image method")

class Template1ImageGenerator(BaseImageGenerator):
    def __init__(self, project_folder, width=1000, height =1500, save=True, show=True, write_uploading_data=False):
        template = self.GENERATOR_MODE_1
        super().__init__(project_folder, template, width, height, save, show, write_uploading_data)
    # Design the 1st template
    def generate_image(self, data):
        self._draw_background()

        self.canvas.show()

class Template2ImageGenerator(BaseImageGenerator):
    def __init__(self, project_folder, width=1000, height =1500, save=True, show=True, write_uploading_data=False):
        template = self.GENERATOR_MODE_2
        super().__init__(project_folder, template, width, height, save, show, write_uploading_data)

    # Design the 2nd template
    def generate_image(self, data):
        pass