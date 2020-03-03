#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint


class NestedBlueprint(Blueprint):
    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u'') + (options.get(
                'url_prefix', blueprint.url_prefix) or u'')
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(blueprint,
                                         url_prefix=url_prefix,
                                         **options)

        self.record(deferred)
