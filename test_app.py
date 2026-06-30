# test_app.py
"""
Test suite for the Pink Morsel Sales Dashboard.
Verifies that the three required UI elements render:
    1. Header        (id="header")
    2. Visualisation (id="sales-graph")
    3. Region picker (id="region-picker")
"""
from dash.testing.application_runners import import_app


def test_header_is_present(dash_duo):
    """The H1 header should render with the expected text."""
    app = import_app("main")
    dash_duo.start_server(app)

    # Wait up to 10s for the header to appear in the DOM
    dash_duo.wait_for_element("#header", timeout=10)

    header = dash_duo.find_element("#header")
    assert header is not None
    assert "Pink Morsel Sales Dashboard" in header.text


def test_visualisation_is_present(dash_duo):
    """The dcc.Graph used for the sales chart should render."""
    app = import_app("main")
    dash_duo.start_server(app)

    # The graph takes a moment to render because the callback runs on load
    dash_duo.wait_for_element("#sales-graph", timeout=15)

    graph = dash_duo.find_element("#sales-graph")
    assert graph is not None


def test_region_picker_is_present(dash_duo):
    """The region radio picker should render with all expected options."""
    app = import_app("main")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-picker", timeout=10)

    region_picker = dash_duo.find_element("#region-picker")
    assert region_picker is not None

    # Sanity check: all five region labels should be visible inside the picker
    picker_text = region_picker.text.lower()
    for label in ["north", "east", "south", "west", "all"]:
        assert label in picker_text, f"Expected '{label}' in region picker"