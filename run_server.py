"""
Entry point for the app
@author Niranjan Balasubramani
@email nibalasu@akamai.com
@date 2018-06-19
"""

from blockchain_app import app

if __name__ == '__main__':
    app.run(host=app.config.get('APP_HOST'),
            port=app.config.get('APP_PORT'),
            debug=app.config.get('APP_DEBUG'))
