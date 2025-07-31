from helpers.application import app, api
from helpers.CORS import cors

from resources.InstituicaoResouce import InstituicoesResouce, NovaInstituicaoResouce, InstituicaoResouce
from resources.IndexResouce import IndexResource

from resources.CensoResource import CensosEscolaresResource, CensoEscolarEstadoResource

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(NovaInstituicaoResouce, '/instituicoes')
api.add_resource(InstituicoesResouce, '/instituicoes/<int:ano_censo>')
api.add_resource(InstituicaoResouce, '/instituicoes/<int:ano_censo>/<int:cod_entidade>')
api.add_resource(CensosEscolaresResource, '/censoescolar/<int:ano_censo>')
api.add_resource(CensoEscolarEstadoResource, '/censoescolar/<int:ano_censo>/<int:cod_estado>')