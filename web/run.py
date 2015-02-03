# -*- coding: utf-8 -*-
"""Application specification for urlz api."""

from urlz.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)