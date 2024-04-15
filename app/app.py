# Import the necessary libraries
import seaborn as sns  # Seaborn for data visualization
from faicons import icon_svg  # FontAwesome icons for visual elements
from shiny import reactive  # Shiny for interactive components
from shiny.express import input, render, ui  # Shiny components for UI design
import palmerpenguins  # Palmer Penguins dataset for sample data

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Set up the page options for the dashboard
ui.page_opts(title="Penguins dashboard", fillable=True)

# Define the sidebar with filter controls
with ui.sidebar(title="Filter controls"):
    # Input slider for penguin mass filter
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox group for penguin species filter
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Links section
    ui.hr()  # Horizontal rule for visual separation
    ui.h6("Links")  # Heading for links
    # GitHub links
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    # External links
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Define layout columns for displaying data
with ui.layout_column_wrap(fill=False):
    # Value boxes for displaying statistics
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout columns for displaying charts and dataframes
with ui.layout_columns():
    # Card for scatter plot of bill length and depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Card for displaying summary statistics
    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


# Define a reactive function to filter the dataset based on user input
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]  # Filter by species
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]  # Filter by mass
    return filt_df
