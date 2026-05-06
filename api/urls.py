from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'motoristas', MotoristaViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'profissionais', ProfissionalViewSet)
router.register(r'equipes', EquipeViewSet)
router.register(r'ocorrencias', OcorrenciaViewSet)

router.register(r'pacientes', PacienteViewSet)

router.register(r'cargos', CargoViewSet)
router.register(r'tipos-registro', TipoRegistroViewSet)
router.register(r'prioridades', PrioridadeViewSet)
router.register(r'status', StatusViewSet)
router.register(r'disponibilidades', DisponibilidadeViewSet)

urlpatterns = router.urls