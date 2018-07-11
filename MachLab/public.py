# Type choices of model type #
model_type_choices = (
    (0, 'default'),
    (1, 'tensorflow'),
    (2, 'keras'),
    (3, 'pytorch'),
)

# Type choices of model file type #
model_file_choices = (
    (0, 'default'),
    (1, '.txt'),
    (2, '.py'),
    (3, '.r'),
)

# Icon colors for each model type #
icon_colors = ['#563d7c', '#555555', '#f34b7d', '#f1e05a', '#DA5B0B', '#b07219']

# List of search type #
search_type_list = ['Models', 'Modelfiles', 'Commits', 'Users']

# Number of models to display on culling page #
n_top = 2