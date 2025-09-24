from models.element_infor import Story


def define_stories(sap_model, stories: list[Story], typical_story_height: float = 3.0):
    """
    Define ETABS stories from a list of Story dataclasses.
    """
    # Convert to arrays required by ETABS API
    inStoryNames = [s.level for s in stories]
    inStoryHeights = [s.height for s in stories]
    inIsMasterStory = [s.is_master for s in stories]
    inSimilarToStory = [s.similar_to for s in stories]
    inSpliceAbove = [s.splice_above for s in stories]
    inSpliceHeight = [s.splice_height for s in stories]
    inColor = [s.color for s in stories]

    # Call ETABS API
    ret = sap_model.Story.SetStories_2(
        typical_story_height,
        len(stories),
        inStoryNames,
        inStoryHeights,
        inIsMasterStory,
        inSimilarToStory,
        inSpliceAbove,
        inSpliceHeight,
        inColor
    )

    if ret != 0:
        raise Exception(f"ETABS failed to define stories. Error code: {ret}")
    else:
        print(f"Successfully defined {len(stories)} stories in ETABS.")
