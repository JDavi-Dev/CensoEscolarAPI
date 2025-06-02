from helpers.application import app, api
from helpers.CORS import cors

from resources.InstituicaoResouce import InstituicoesResouce, InstituicaoResouce
from resources.IndexResouce import IndexResource

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResouce, '/instituicoes')
api.add_resource(InstituicaoResouce, '/instituicoes/<int:cod_entidade>')