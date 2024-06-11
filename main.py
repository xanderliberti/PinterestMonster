
def image_generation(project_folder, mode):
    from modules.base import Pinterest
    from modules.image_generator import Template1ImageGenerator, Template2ImageGenerator

    base = Pinterest(project_folder)

    data = base.open_csv(base.GENERATOR_DATA_FILE)

    # Common parameters for all image generators
    common_params = {
        'width': 1000,
        'height': 1500,
        'save': False,
        'show': True,
        'write_uploading_data': False
    }
    # Dictionary mapping generation mode to image generator class
    generators = {
        base.GENERATOR_MODE_1: Template1ImageGenerator,
        base.GENERATOR_MODE_2: Template2ImageGenerator
    }

    # Check if the specifoed mode is in the generators dictionary
    if mode in generators:
        # Get generators class for the specified mode
        generator_class = generators[mode]

        # Create an instance of the generator
        generator = generator_class(project_folder, **common_params)
        for row in data:
            # Generate image for each data row
            generator.generate_image(row)
    else:
        # raise an exception if the mode is invalid
        raise ValueError(f"Invalid mode: {mode}. Check available modes in the basse class")

def writing(project_folder, mode):
    from modules.writer import Writer
    
    table_id = '16im6AB70bfjb-rg4k3y71XQYKn-aRd-71xB13pK7p00'

    writer = Writer(project_folder)
    data = writer.open_data(mode, google_sheet=True, table_id=table_id)

    for row in data:
        writer.write(row, mode)
        # print("PRINT ROW IN wirtting ", row)

if __name__ == '__main__':
    project_name = 'keto'

    writer_mode = ['video', 'image']
    writing(project_name, writer_mode[1])

    # generator_modes = ['template_1', 'template_2']
    # image_generation(project_name, generator_modes[1])