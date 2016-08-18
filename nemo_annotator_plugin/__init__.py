from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from flask import url_for, send_from_directory, Markup, request, jsonify, Response
import requests
from nemo_oauth_plugin import NemoOauthPlugin


class AnnotatorPlugin(PluginPrototype):
    """ Perseids Annotator Plugin for Nemo

    :param annotation_store
    :type URL of the annotation store's update endpoint

    :ivar interface: QueryInterface used to retrieve annotations
    :cvar HAS_AUGMENT_RENDER: (True) Adds a stack of render

    """
    HAS_AUGMENT_RENDER = True
    TEMPLATES = {
        "annotator": resource_filename("nemo_annotator_plugin", "data/templates")
    }

    ROUTES = PluginPrototype.ROUTES + [
        ("/annotator/assets/<path:filename>", "r_annotator_assets", ["GET"]),
        ("/annotator/proxy", "r_annotator_proxy", ["GET","POST"])
    ]

    def __init__(self, annotation_store, *args, **kwargs):
        super(AnnotatorPlugin, self).__init__(*args, **kwargs)
        self.__annotation_store__ = annotation_store

    @property
    def annotation_store(self):
        return self.__annotation_store__

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

    @NemoOauthPlugin.oauth_required
    def r_annotator_proxy(self):
        """ Proxy to write to the annotation store

        :return: response from the remote query store
        :rtype: {str: Any}
        """

        query = request.data

        if self.is_authorized(query):
            try:
                resp = requests.post(self.annotation_store, data=query, json=None,
                                     headers={"content-type": "application/sparql-update",
                                              "accept": "application/sparql-results+json"})
                resp.raise_for_status()
                return resp.content, resp.status_code
            except requests.exceptions.HTTPError as err:
                return str(err), resp.status_code
        else:
            return "Unauthorized request", 403


    def is_authorized(self,query):
        """
            Verify AuthZ conditions for an annotation query

            :param the query
            :type str

            :return: True or false
            :rtype bool
        """
        # TODO here we want to check the content of the query against the user_uri that's stored
        # in the session to make sure they match
        return True

