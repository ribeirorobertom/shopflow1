# ShopFlow - Contexto do Sistema

## O que é
Sistema de gestão de esteira de lojas Shopify rodando localmente em localhost:5000.
Desenvolvido para Roberto, empreendedor brasileiro com operações de e-commerce na Europa.

## Stack
- Backend: Python Flask
- Dados: data/lojas.json
- Frontend: HTML + CSS + JS (templates Flask)
- Inicialização: iniciar.bat

## Estrutura de pastas
shopflow/
  app.py
  iniciar.bat
  data/
    lojas.json
  templates/
  static/

## Regras de negócio

### Ciclo de pagamento
- Calculado em dias ÚTEIS (segunda a sexta, excluindo feriados)
- Campo ultimo_pagamento + ciclo_dias_uteis = proximo_pagamento
- Alerta verde: mais de 3 dias uteis restantes
- Alerta amarelo: 2 a 3 dias uteis restantes
- Alerta vermelho: 1 dia util ou vencido

### Status da loja
- Aquecendo: loja em fase de warm-up, ainda nao rodando trafego pago
- Rodando: trafego pago ativo
- Problema: alguma etapa com falha, gateway suspenso, etc
- Pausada: loja parada temporariamente

### Gateway suspenso
- Quando Shopify Payments e suspensa, congela o countdown de pagamento
- Exibe alerta vermelho com data estimada de liberacao dos fundos
- Registrar data de suspensao e data estimada de liberacao (padrao 120 dias)
- Ao reabilitar, retoma o ciclo normal a partir da data de reabilitacao

### Funil de aquecimento (padrao)
- Dia 1: Criar loja e conectar dominio
- Dia 2: Criar Shopify Payments
- Dia 3: Fazer compra teste e verificar prazo de recebimento
- Dia 7: Subir produtos
- Dia 8: Iniciar funil de pixel (5 dias)
- Dia 12: Iniciar funil de conversao com orcamento alto
- Cada etapa tem: status (pendente/concluida/problema), data, observacao

## Campos de cada loja
- nome
- dominio
- email
- entidade: LTD ou LLC + nome do titular
- pais_entidade: pais onde a empresa e registrada
- pais_operacao: pais onde a loja opera (pode ser Global)
- nicho
- banco: onde recebe os pagamentos (ex: Payoneer)
- gateways: lista de gateways ativos (ex: Shopify Payments, Stripe)
- gateway_status: ativo ou suspenso
- ciclo_dias_uteis: numero de dias uteis do ciclo de pagamento
- data_criacao: data de criacao da loja
- ultimo_pagamento: data do ultimo pagamento recebido
- proximo_pagamento: calculado automaticamente
- status: Aquecendo, Rodando, Problema, Pausada
- funil: lista de etapas com status, data e observacao
- eventos: log cronologico de tudo que aconteceu na loja
- observacoes: campo livre

## Como o Claude Code deve se comportar
- Sempre ler este arquivo antes de qualquer modificacao no sistema
- Ao adicionar campos novos, atualizar tambem o lojas.json com valor padrao
- Manter consistencia entre o frontend e o JSON
- Gerar o iniciar.bat atualizado sempre que houver mudanca de dependencias
- Nao quebrar dados existentes ao fazer melhorias
- Comentar o codigo em portugues