from rest_framework import serializers
from .models import (
    Motorista, Veiculo, Profissional, Equipe,
    Ocorrencia, TipoRegistro, Cargo,
    Prioridade, Status, Paciente, Disponibilidade
)

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = '__all__'


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class TipoRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRegistro
        fields = '__all__'


class PrioridadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridade
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
        

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'

    def validate(self, data):
        tipo = data.get('tipo_registro')
        numero = data.get('numero_registro')

        if tipo and not numero:
            raise serializers.ValidationError("numero de registro obrigatório")

        if numero and not tipo:
            raise serializers.ValidationError("tipo de registro obrigatório")

        return data
    
    
class EquipeSerializer(serializers.ModelSerializer):
    profissionais = serializers.PrimaryKeyRelatedField(
        queryset=Profissional.objects.all(),
        many=True
    )

    class Meta:
        model = Equipe
        fields = '__all__'

    def validate(self, data):
        motorista = data.get('motorista')
        profissionais = data.get('profissionais', [])
        veiculo = data.get('veiculo')

        if len(profissionais) == 0:
            raise serializers.ValidationError("equipe precisa de pelo menos 1 profissional")

        equipes = Equipe.objects.filter(motorista=motorista, veiculo=veiculo)

        if self.instance:
            equipes = equipes.exclude(id=self.instance.id)

        for equipe in equipes:
            if set(equipe.profissionais.values_list('id', flat=True)) == set([p.id for p in profissionais]):
                raise serializers.ValidationError("essa equipe ja existe")

        if Equipe.objects.filter(
            motorista=motorista,
            disponibilidade__codigo__in=["DISPONIVEL", "ATENDENDO"]
        ).exists():
            raise serializers.ValidationError("motorista ja esta em outra equipe ativa")

        for prof in profissionais:
            if Equipe.objects.filter(
                profissionais=prof,
                disponibilidade__codigo__in=["DISPONIVEL", "ATENDENDO"]
            ).exists():
                raise serializers.ValidationError(f"profissional '{prof.nome}' ocupado")

        return data
    
    
class OcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocorrencia
        fields = '__all__'

    def validate(self, data):
        hc = data.get('horario_chamado')
        ha = data.get('horario_atendimento')
        hh = data.get('horario_chegada_hospital')

        if ha and hc and ha < hc:
            raise serializers.ValidationError("atendimento antes do chamado")

        if hh and ha and hh < ha:
            raise serializers.ValidationError("chegada antes do atendimento")

        return data
    
    def update(self, instance, validated_data):
        novo_status = validated_data.get('status', instance.status)
        nova_equipe = validated_data.get('equipe', instance.equipe)

        disp_atendendo = Disponibilidade.objects.get(codigo="ATENDENDO")
        disp_disponivel = Disponibilidade.objects.get(codigo="DISPONIVEL")

        if instance.status.codigo == "FINALIZADO":
            raise serializers.ValidationError("ocorrencia finalizada nao pode ser alterada")

        if instance.status.codigo == "EM_ATENDIMENTO":
            allowed = {'paciente', 'horario_atendimento', 'horario_chegada_hospital', 'status'}
            for campo in validated_data.keys():
                if campo not in allowed:
                    raise serializers.ValidationError("em atendimento só permite alterações específicas")

        atribuindo_equipe = instance.equipe is None and nova_equipe is not None

        if atribuindo_equipe:
            if instance.status.codigo != "ABERTO":
                raise serializers.ValidationError("so pode atribuir equipe quando aberto")

            if nova_equipe.disponibilidade.codigo != "DISPONIVEL":
                raise serializers.ValidationError("equipe nao disponivel")

            nova_equipe.disponibilidade = disp_atendendo
            nova_equipe.save()

        if instance.equipe and nova_equipe and instance.equipe != nova_equipe:
            raise serializers.ValidationError("nao pode trocar equipe")

        instance = super().update(instance, validated_data)

        if atribuindo_equipe:
            instance.motorista = nova_equipe.motorista
            instance.veiculo = nova_equipe.veiculo
            instance.save()

            instance.profissionais.set(nova_equipe.profissionais.all())

        if instance.status.codigo != "FINALIZADO" and novo_status.codigo == "FINALIZADO":
            if instance.equipe:
                equipe = instance.equipe
                equipe.disponibilidade = disp_disponivel
                equipe.save()

        return instance