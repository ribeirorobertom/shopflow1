# ShopFlow

Sistema de gestao de lojas Shopify rodando no seu proprio computador. Desenvolvido para quem opera multiplas lojas de e-commerce e precisa acompanhar pagamentos, status e progresso de aquecimento de cada loja em um unico lugar.

---

## O que e o ShopFlow

O ShopFlow e um painel de controle que roda localmente na sua maquina — sem mensalidade, sem nuvem, sem login. Voce abre pelo navegador igual a qualquer site, mas ele so funciona no seu computador.

Com ele voce consegue:

- Ver todas as suas lojas Shopify em um unico painel
- Acompanhar quando o proximo pagamento de cada loja vai cair
- Receber alertas de vencimento (verde, amarelo e vermelho)
- Monitorar o progresso de aquecimento de cada loja nova
- Registrar eventos e observacoes por loja
- Controlar situacoes de gateway suspenso

---

## Requisitos

Antes de instalar, voce precisa ter o seguinte no seu computador:

- **Python 3.8 ou superior** — o motor que faz o sistema rodar  
  Baixe em: [python.org/downloads](https://www.python.org/downloads/)  
  Durante a instalacao, marque a opcao **"Add Python to PATH"**

- **Windows 10 ou superior**

- Conexao com a internet (apenas na primeira instalacao, para baixar as dependencias)

---

## Como instalar

1. **Baixe o projeto do GitHub**  
   Clique em **Code > Download ZIP**, extraia a pasta em um lugar de facil acesso (ex: `Documentos\shopflow`)

2. **Abra a pasta shopflow**

3. **Clique duas vezes no arquivo `iniciar.bat`**  
   Na primeira vez, ele vai instalar as dependencias automaticamente. Aguarde alguns segundos.

4. **Abra o navegador** e acesse:  
   ```
   http://localhost:5000
   ```

Pronto. O ShopFlow esta rodando.

> Para fechar o sistema, basta fechar a janela preta que aparece quando voce clica no `iniciar.bat`.

---

## Como cadastrar a primeira loja

1. No painel principal, clique no botao **"Nova Loja"**
2. Preencha os campos:
   - **Nome da loja** — nome que voce vai usar para identificar (ex: "Loja UK Verao")
   - **Dominio** — endereco da loja (ex: `minhaloja.com`)
   - **Email** — email associado a conta Shopify
   - **Entidade** — tipo de empresa e nome do titular (ex: "LTD - Roberto Ribeiro")
   - **Pais da entidade** — onde a empresa esta registrada (ex: Reino Unido)
   - **Pais de operacao** — onde a loja vende (ex: Global, Reino Unido)
   - **Nicho** — segmento de produto (ex: fitness, pets, casa)
   - **Banco** — onde voce recebe os pagamentos (ex: Payoneer, Wise)
   - **Gateways** — meios de pagamento ativos (ex: Shopify Payments, Stripe)
   - **Ciclo de pagamento** — quantos dias uteis o gateway leva para pagar (ex: 5)
   - **Ultimo pagamento** — data do ultimo pagamento recebido
3. Clique em **Salvar**

A loja vai aparecer no painel com o countdown ate o proximo pagamento calculado automaticamente.

---

## Funil de aquecimento padrao

Toda loja nova passa por um processo de aquecimento antes de receber trafego pago. O ShopFlow acompanha esse progresso com 6 etapas:

| Etapa | Dia | O que fazer |
|-------|-----|-------------|
| 1 | Dia 1 | Criar a loja no Shopify e conectar o dominio proprio |
| 2 | Dia 2 | Criar e ativar o Shopify Payments |
| 3 | Dia 3 | Fazer uma compra teste e confirmar o prazo de recebimento |
| 4 | Dia 7 | Subir os produtos na loja |
| 5 | Dia 8 | Iniciar o funil de aquecimento de pixel (dura 5 dias) |
| 6 | Dia 12 | Iniciar o funil de conversao com orcamento alto |

Cada etapa pode estar em um de tres estados:

- **Pendente** — ainda nao foi feita
- **Concluida** — feita com sucesso
- **Problema** — houve alguma falha ou bloqueio

Voce pode adicionar uma observacao em qualquer etapa para registrar o que aconteceu, numeros relevantes ou proximos passos.

> O funil de aquecimento existe para preparar a conta do Shopify Payments antes de escalar os gastos com trafego pago. Queimar essa etapa pode resultar em suspensao do gateway ou limites baixos de processamento.
