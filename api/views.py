from rest_framework import viewsets
from .models import (
    Motorista, Veiculo, Profissional, Equipe,
    Ocorrencia, Cargo, TipoRegistro,
    Prioridade, Status, Paciente, Disponibilidade
)

from .serializers import (
    MotoristaSerializer, VeiculoSerializer, ProfissionalSerializer,
    EquipeSerializer, OcorrenciaSerializer,
    CargoSerializer, TipoRegistroSerializer,
    PrioridadeSerializer, StatusSerializer,
    PacienteSerializer, DisponibilidadeSerializer
)

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer


class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class TipoRegistroViewSet(viewsets.ModelViewSet):
    queryset = TipoRegistro.objects.all()
    serializer_class = TipoRegistroSerializer


class PrioridadeViewSet(viewsets.ModelViewSet):
    queryset = Prioridade.objects.all()
    serializer_class = PrioridadeSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class DisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer
    
    
