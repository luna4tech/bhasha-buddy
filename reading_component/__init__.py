import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "reading_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("reading_component", path=build_dir)

def reading_component(audio_src, words, story_title, language='en-US', key=None):
    component_value = _component_func(audio_src=audio_src, words=words, storyTitle=story_title, language=language, key=key)
    return component_value