# -*- coding: utf-8 -*-

from flask_cors import CORS

cors = CORS(resources={r"/api/*": {"origins": "*"}})
