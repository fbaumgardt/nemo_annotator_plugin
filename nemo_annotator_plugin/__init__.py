from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
"""from nemo_oauth_plugin import NemoOauthPlugin"""


class AnnotatorPlugin(PluginPrototype):
    HAS_AUGMENT_RENDER = True
    TEMPLATES = {
        "annotator": resource_filename("nemo_annotator_plugin", "data/templates")
    }

    ROUTES = PluginPrototype.ROUTES

    def __init__(self, *args, **kwargs):
        super(AnnotatorPlugin, self).__init__(*args, **kwargs)

    def render(self, **kwargs):
        update = kwargs
        if "template" in kwargs and kwargs["template"] == "main::text.html":
            update["template"] = "annotator::text.html"
        return update