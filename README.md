# Documentação da API

## Autenticação

### Login

**Endpoint**

```http
POST /api/token/
```

**Body**

```json
{
    "username": "admin",
    "password": "123456"
}
```

**Resposta**

```json
{
    "token": "10f85925085e0893b9345a12e59e02afcccafde1"
}
```

### Uso do Token

Enviar em todas as requisições protegidas:

```http
Authorization: Token 10f85925085e0893b9345a12e59e02afcccafde1
```

---

# Endpoints Disponíveis

Todos os recursos possuem os seguintes métodos:

| Método | Endpoint       | Ação                   |
| ------ | -------------- | ---------------------- |
| GET    | /recurso/      | Listar registros       |
| POST   | /recurso/      | Criar registro         |
| GET    | /recurso/{id}/ | Buscar registro        |
| PUT    | /recurso/{id}/ | Atualizar registro     |
| PATCH  | /recurso/{id}/ | Atualizar parcialmente |
| DELETE | /recurso/{id}/ | Excluir registro       |

---

# Veículos

## Endpoint

```http
/veiculos/
```

## Criação

```json
{
    "placa": "ABC1234",
    "marca": "Fiat",
    "modelo": "Ducato",
    "categoria": "AMBULANCIA",
    "cnh_necessaria": "D",
    "ano": 2022,
    "km": 10000,
    "disponibilidade": 1
}
```

---

# Funcionários

## Endpoint

```http
/funcionarios/
```

## Criação

```json
{
    "cpf": "12345678900",
    "nome": "João Silva",
    "data_nascimento": "1990-01-01",
    "telefone": "14999999999",
    "email": "joao@email.com",
    "disponibilidade": 1
}
```

---

# CNHs

## Endpoint

```http
/cnhs/
```

## Criação

```json
{
    "funcionario": 1,
    "numero": "123456789",
    "categoria": "D",
    "validade": "2028-12-31"
}
```

---

# Profissionais de Saúde

## Endpoint

```http
/profissionais-saude/
```

## Criação

```json
{
    "funcionario": 1,
    "cargo": 2,
    "numero_registro": "12345"
}
```

## Regras

* Se o cargo exigir registro profissional, `numero_registro` é obrigatório.
* Se o cargo não exigir registro profissional, `numero_registro` não deve ser enviado.

---

# Equipes

## Endpoint

```http
/equipes/
```

## Criação

```json
{
    "nome_equipe": "Equipe Alfa",
    "condutor": 1,
    "profissionais": [1, 2],
    "veiculo": 1,
    "disponibilidade": 1
}
```

## Regras

* Deve existir pelo menos um profissional na equipe.
* O condutor deve estar presente na lista de profissionais.
* O condutor deve possuir CNH válida.
* A categoria da CNH deve ser compatível com a exigida pelo veículo.
* Um veículo não pode pertencer a mais de uma equipe.
* Um profissional não pode pertencer a mais de uma equipe.

---

# Pacientes

## Endpoint

```http
/pacientes/
```

## Criação

```json
{
    "nome": "Maria Souza",
    "cpf": "11122233344",
    "telefone": "14999999999",
    "data_nascimento": "1980-05-20"
}
```

---

# Ocorrências

## Endpoint

```http
/ocorrencias/
```

## Criação

```json
{
    "titulo": "Acidente de trânsito",
    "observacoes": "Colisão frontal",
    "prioridade": 1,
    "status": 1,
    "local_informado": "Av. Central",
    "destino": "Hospital Municipal",
    "horario_chamado": "2026-05-31T10:00:00Z",
    "paciente": 1
}
```

## Regras de Validação

* `horario_atendimento` não pode ser anterior a `horario_chamado`.
* `horario_chegada_hospital` não pode ser anterior a `horario_atendimento`.

## Regras de Atualização

* Ocorrências finalizadas não podem ser alteradas.
* Não é permitido trocar a equipe após sua atribuição.
* Apenas equipes disponíveis podem ser atribuídas.
* Ao finalizar uma ocorrência, a equipe e o veículo retornam para o estado disponível.

---

# Cargos

## Endpoint

```http
/cargos/
```

## Criação

```json
{
    "nome": "Médico",
    "tipo_registro": 1
}
```

---

# Tipos de Registro

## Endpoint

```http
/tipos-registro/
```

## Criação

```json
{
    "sigla": "CRM"
}
```

---

# Prioridades

## Endpoint

```http
/prioridades/
```

## Criação

```json
{
    "nome": "Alta",
    "codigo": "ALTA"
}
```

---

# Status

## Endpoint

```http
/status/
```

## Criação

```json
{
    "nome": "ABERTA",
    "codigo": "ABERTA"
}
```

---

# Disponibilidades

## Endpoint

```http
/disponibilidades/
```

## Criação

```json
{
    "nome": "DISPONIVEL",
    "codigo": "DISP"
}
```

---

# Observação Importante

O sistema possui o model `Atendente`, porém atualmente não existe endpoint para criação ou gerenciamento de atendentes.

O backend possui:

* Model `Atendente`
* Serializer `AtendenteSerializer`
* ViewSet `AtendenteViewSet`

Mas a rota não está registrada no router.

Para disponibilizar a funcionalidade será necessário adicionar:

```python
router.register(r'atendentes', AtendenteViewSet)
```

Após isso serão criados automaticamente os endpoints:

```http
GET    /atendentes/
POST   /atendentes/
GET    /atendentes/{id}/
PUT    /atendentes/{id}/
PATCH  /atendentes/{id}/
DELETE /atendentes/{id}/
```
