from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import date, timedelta, datetime

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'lojas.json')


def load_data():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({'lojas': []}, f)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_business_days(start_date, days):
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current


def business_days_remaining(today, target):
    count = 0
    current = today
    while current < target:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


def compute_payment_info(loja):
    start_str = loja.get('data_ciclo_inicio') or loja.get('data_inicio')
    if not start_str:
        return None, None
    start = datetime.strptime(start_str, '%Y-%m-%d').date()
    ciclo = int(loja.get('ciclo_pagamento_dias_uteis', 7))
    today = date.today()
    next_pay = add_business_days(start, ciclo)
    while next_pay <= today:
        next_pay = add_business_days(next_pay, ciclo)
    remaining = business_days_remaining(today, next_pay)
    return next_pay, remaining


def enrich_loja(loja):
    loja['_suspenso'] = loja.get('gateway_status') == 'suspenso'

    if loja['_suspenso']:
        loja['_next_payment'] = None
        loja['_days_remaining'] = None
        loja['_alert'] = 'red'
    else:
        next_pay, remaining = compute_payment_info(loja)
        loja['_next_payment'] = next_pay.strftime('%d/%m/%Y') if next_pay else None
        loja['_days_remaining'] = remaining
        if remaining is None:
            loja['_alert'] = 'gray'
        elif remaining <= 0:
            loja['_alert'] = 'red'
        elif remaining <= 2:
            loja['_alert'] = 'yellow'
        else:
            loja['_alert'] = 'green'
    return loja


def default_funil():
    return [
        {'etapa': 1, 'nome': 'Criar loja e domínio', 'dia': 'Dia 1', 'status': 'pendente', 'data': None, 'observacao': ''},
        {'etapa': 2, 'nome': 'Criar Shopify Payments', 'dia': 'Dia 2', 'status': 'pendente', 'data': None, 'observacao': ''},
        {'etapa': 3, 'nome': 'Compra teste', 'dia': 'Dia 3', 'status': 'pendente', 'data': None, 'observacao': ''},
        {'etapa': 4, 'nome': 'Subir produtos', 'dia': 'Dia 7', 'status': 'pendente', 'data': None, 'observacao': ''},
        {'etapa': 5, 'nome': 'Iniciar pixel (5 dias)', 'dia': 'Dia 8', 'status': 'pendente', 'data': None, 'observacao': ''},
        {'etapa': 6, 'nome': 'Iniciar conversão com orçamento alto', 'dia': 'Dia 12', 'status': 'pendente', 'data': None, 'observacao': ''},
    ]


# ── Pages ──────────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    data = load_data()
    lojas = [enrich_loja(l) for l in data.get('lojas', [])]
    return render_template('index.html', lojas=lojas)


@app.route('/loja/<loja_id>')
def detalhe(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return redirect(url_for('dashboard'))
    return render_template('loja.html', loja=enrich_loja(loja))


@app.route('/loja/nova')
def nova():
    return render_template('form.html', loja=None)


@app.route('/loja/<loja_id>/editar')
def editar(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return redirect(url_for('dashboard'))
    return render_template('form.html', loja=loja)


@app.route('/loja/salvar', methods=['POST'])
def salvar():
    data = load_data()
    f = request.form
    raw_id = f.get('id', '').strip()
    loja_id = raw_id.lower().replace(' ', '-') if raw_id else f.get('nome', '').lower().replace(' ', '-')
    gateways = request.form.getlist('gateways')
    existing = next((l for l in data['lojas'] if l['id'] == loja_id), None)

    nova_loja = {
        'id': loja_id,
        'nome': f.get('nome', ''),
        'dominio': f.get('dominio', ''),
        'email': f.get('email', ''),
        'entidade': {'tipo': f.get('entidade_tipo', 'LTD'), 'titular': f.get('entidade_titular', '')},
        'pais_entidade': f.get('pais_entidade', ''),
        'pais_operacao': f.get('pais_operacao', ''),
        'nicho': f.get('nicho', ''),
        'banco': f.get('banco', ''),
        'gateways': gateways,
        'ciclo_pagamento_dias_uteis': int(f.get('ciclo', 7) or 7),
        'data_criacao': f.get('data_criacao', ''),
        'data_ciclo_inicio': f.get('data_ciclo_inicio', ''),
        'ultimo_pagamento': existing.get('ultimo_pagamento') if existing else None,
        'status': f.get('status', 'Aquecendo'),
        'gateway_status': existing.get('gateway_status', 'normal') if existing else 'normal',
        'data_liberacao_estimada': existing.get('data_liberacao_estimada') if existing else None,
        'funil': existing['funil'] if existing else default_funil(),
        'eventos': existing['eventos'] if existing else [],
    }

    if existing:
        data['lojas'] = [nova_loja if l['id'] == loja_id else l for l in data['lojas']]
    else:
        data['lojas'].append(nova_loja)

    save_data(data)
    return redirect(url_for('detalhe', loja_id=loja_id))


# ── Funil ──────────────────────────────────────────────────────────────────

@app.route('/loja/<loja_id>/funil/<int:etapa>', methods=['POST'])
def atualizar_funil(loja_id, etapa):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    for step in loja['funil']:
        if step['etapa'] == etapa:
            step['status'] = body.get('status', step['status'])
            step['data'] = body.get('data') or step['data']
            step['observacao'] = body.get('observacao', step['observacao'])
            break
    save_data(data)
    return jsonify({'ok': True})


# ── Eventos ────────────────────────────────────────────────────────────────

@app.route('/loja/<loja_id>/evento', methods=['POST'])
def adicionar_evento(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    evento = {'data': body.get('data', str(date.today())), 'descricao': body.get('descricao', '')}
    loja['eventos'].insert(0, evento)
    save_data(data)
    return jsonify({'ok': True})


@app.route('/loja/<loja_id>/evento/<int:idx>', methods=['POST'])
def editar_evento(loja_id, idx):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja or idx >= len(loja['eventos']):
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    ev = loja['eventos'][idx]
    ev['data'] = body.get('data', ev['data'])
    ev['descricao'] = body.get('descricao', ev['descricao'])
    save_data(data)
    return jsonify({'ok': True})


@app.route('/loja/<loja_id>/evento/<int:idx>/excluir', methods=['POST'])
def excluir_evento(loja_id, idx):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja or idx >= len(loja['eventos']):
        return jsonify({'error': 'not found'}), 404
    loja['eventos'].pop(idx)
    save_data(data)
    return jsonify({'ok': True})


# ── Pagamentos ─────────────────────────────────────────────────────────────

@app.route('/loja/<loja_id>/registrar-pagamento', methods=['POST'])
def registrar_pagamento(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    pay_date = body.get('data', str(date.today()))
    valor = (body.get('valor') or '').strip()
    loja['ultimo_pagamento'] = pay_date
    loja['data_ciclo_inicio'] = pay_date
    desc = 'Pagamento recebido' + (f' — {valor}' if valor else '')
    loja['eventos'].insert(0, {'data': pay_date, 'descricao': desc})
    save_data(data)
    return jsonify({'ok': True})


# ── Status ─────────────────────────────────────────────────────────────────

@app.route('/loja/<loja_id>/status', methods=['POST'])
def atualizar_status(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    loja['status'] = body.get('status', loja['status'])
    save_data(data)
    return jsonify({'ok': True})


@app.route('/loja/<loja_id>/gateway-status', methods=['POST'])
def gateway_status_route(loja_id):
    data = load_data()
    loja = next((l for l in data['lojas'] if l['id'] == loja_id), None)
    if not loja:
        return jsonify({'error': 'not found'}), 404
    body = request.json or {}
    new_status = body.get('status', 'normal')
    old_status = loja.get('gateway_status', 'normal')
    loja['gateway_status'] = new_status
    loja['data_liberacao_estimada'] = body.get('data_liberacao') or None

    if body.get('log', True):
        today = str(date.today())
        if new_status == 'suspenso' and old_status != 'suspenso':
            lib = body.get('data_liberacao') or '—'
            loja['eventos'].insert(0, {
                'data': today,
                'descricao': f'Shopify Payments suspenso. Liberação estimada: {lib}'
            })
        elif new_status == 'normal' and old_status == 'suspenso':
            loja['eventos'].insert(0, {
                'data': today,
                'descricao': 'Shopify Payments reabilitado. Operação normalizada.'
            })

    save_data(data)
    return jsonify({'ok': True})


# ── Excluir loja ───────────────────────────────────────────────────────────

@app.route('/loja/<loja_id>/excluir', methods=['POST'])
def excluir(loja_id):
    data = load_data()
    data['lojas'] = [l for l in data['lojas'] if l['id'] != loja_id]
    save_data(data)
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
