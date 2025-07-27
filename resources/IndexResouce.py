from flask_restful import Resource

class IndexResource(Resource):
    def get(self):
        versao = {"versao": "1.5.0"}
        return versao, 200