import random

from models.element_infor import Story


def define_stories(sap_model, stories: list[Story], base_elevation: float):
    """
    Defines ETABS stories from a list of Story objects with a specified base elevation.

    Args:
        sap_model: The active ETABS model object.
        stories: A list of Story dataclass objects (ordered from bottom to top).
        base_elevation: The elevation of the base level [ft].
    """
    if not stories:
        print("⚠️ Warning: No stories provided to define.")
        return

    # Convert the list of dataclasses into the separate lists required by the ETABS API
    story_names = [s.level for s in stories]
    story_heights = [s.height*1000 for s in stories]
    is_master_story = [s.is_master for s in stories]
    similar_to_story = [s.similar_to for s in stories]
    splice_above = [s.splice_above for s in stories]
    splice_height = [s.splice_height*1000 for s in stories]
    colors = [s.color for s in stories]

    # Call the ETABS API function with the new base_elevation parameter
    returned_values = sap_model.Story.SetStories_2(
        base_elevation*1000,
        len(stories),
        story_names,
        story_heights,
        is_master_story,
        similar_to_story,
        splice_above,
        splice_height,
        generate_color_list(len(stories))
    )

    ret = returned_values[-1]  # Extract the actual return code (last element)

    if ret != 0:
        raise Exception(f"❌ ETABS API failed to define stories. Error code: {ret}")
    else:
        print(f"✅ Successfully defined {len(stories)} stories with base elevation at {base_elevation} ft.")


def generate_color_list(length: int) -> list[int]:
    """
    Generate a list of random color integers.

    Each color is represented as an integer in the range 0 to 16777215 (0xFFFFFF),
    which encodes RGB values (Red << 16 | Green << 8 | Blue).

    Args:
        length (int): The number of colors to generate.

    Returns:
        list[int]: A list of random color integers.
    """
    if length < 0:
        raise ValueError("Length must be non-negative.")

    return [random.randint(0, 16777215) for _ in range(length)]
