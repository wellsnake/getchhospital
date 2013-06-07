#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

import sae
from code import app

application = sae.create_wsgi_app(app.wsgifunc())
