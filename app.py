from helpers.application import app, api
from helpers.CORS import cors

from resources.InstituicaoResouce import InstituicoesResouce, NovaInstituicaoResouce, InstituicaoResouce
from resources.IndexResouce import IndexResource

from resources.UfResource import UfsResouce, UfResource
from resources.MesorregiaoResource import MesorregioesResouce, MesorregiaoResource
from resources.MicrorregiaoResouce import MicrorregioesResouce, MicrorregiaoResource
from resources.MunicipioResource import MunicipiosResouce, MunicipioResource

from resources.CensoResource import CensosEscolaresResource, CensoEscolarEstadoResource

cors.init_app(app)

api.add_resource(IndexResource, '/')

api.add_resource(UfsResouce, '/ufs')
api.add_resource(UfResource, '/uf/<int:cod_uf>')

api.add_resource(MesorregioesResouce, '/mesorregioes')
api.add_resource(MesorregiaoResource, '/mesorregiao/<int:cod_mesorregiao>')

api.add_resource(MicrorregioesResouce, '/microrregioes')
api.add_resource(MicrorregiaoResource, '/microrregiao/<int:cod_microrregiao>')

api.add_resource(MunicipiosResouce, '/municipios')
api.add_resource(MunicipioResource, '/municipio/<int:cod_municipio>')

api.add_resource(NovaInstituicaoResouce, '/instituicoes')
api.add_resource(InstituicoesResouce, '/instituicoes/<int:ano_censo>')
api.add_resource(InstituicaoResouce, '/instituicoes/<int:ano_censo>/<int:cod_entidade>')

api.add_resource(CensosEscolaresResource, '/censoescolar/<int:ano_censo>')
api.add_resource(CensoEscolarEstadoResource, '/censoescolar/<int:ano_censo>/<int:cod_estado>')