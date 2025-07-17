from flasgger import Swagger

def setup_swagger(app):
    Swagger(app, template={
        'swagger': '2.0',
        'info': {
            'title': 'Python Hub API',
            'description': 'API documentation for Python Hub',
            'version': '1.0.0'
        },
        'basePath': '/',
        'schemes': ['http', 'https'],
    }) 