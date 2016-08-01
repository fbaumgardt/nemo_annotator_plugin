from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from flask import url_for, send_from_directory, Markup
"""from nemo_oauth_plugin import NemoOauthPlugin"""


class AnnotatorPlugin(PluginPrototype):
    HAS_AUGMENT_RENDER = True
    TEMPLATES = {
        "annotator": resource_filename("nemo_annotator_plugin", "data/templates")
    }

    ROUTES = PluginPrototype.ROUTES + [
        ("/annotator-assets/<path:filename>", "r_annotator_assets", ["GET"]),
    ]

    def __init__(self, *args, **kwargs):
        super(AnnotatorPlugin, self).__init__(*args, **kwargs)

    def render(self, **kwargs):
        update = kwargs
        if "template" in kwargs and kwargs["template"] == "main::text.html":
            update["template"] = "annotator::text.html"
            update["text_passage"] = Markup(' '.join([ x.strip() for x in kwargs["text_passage"].splitlines() ]))
        return update

    def r_annotator_assets(self, filename):
        """ Routes for assets
        :param filename: Filename in data/assets to retrievee
        :return: Content of the file
        """
        return send_from_directory(resource_filename("nemo_annotator_plugin", "data/assets"), filename)