// ── Modal helpers ──────────────────────────────────────────────────────────

function openModal(id) {
  document.getElementById(id).classList.add('active');
}

function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
  }
});

function lojaId() {
  return document.getElementById('loja-id').value;
}

async function post(url, payload) {
  return fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
}

// ── Funnel step edit ──────────────────────────────────────────────────────

function editStep(etapa, status, data, obs) {
  document.getElementById('ms-etapa').value = etapa;
  document.getElementById('ms-status').value = status;
  document.getElementById('ms-data').value = data || '';
  document.getElementById('ms-obs').value = obs || '';
  openModal('modal-step');
}

async function saveStep() {
  const etapa = document.getElementById('ms-etapa').value;
  const r = await post(`/loja/${lojaId()}/funil/${etapa}`, {
    status:    document.getElementById('ms-status').value,
    data:      document.getElementById('ms-data').value || null,
    observacao: document.getElementById('ms-obs').value,
  });
  if (r.ok) location.reload();
}

// ── Add event ─────────────────────────────────────────────────────────────

function openAddEvento() {
  document.getElementById('me-data').value = today();
  document.getElementById('me-desc').value = '';
  openModal('modal-evento');
}

async function saveEvento() {
  const desc = document.getElementById('me-desc').value.trim();
  if (!desc) { alert('Informe a descrição do evento.'); return; }
  const r = await post(`/loja/${lojaId()}/evento`, {
    data: document.getElementById('me-data').value,
    descricao: desc,
  });
  if (r.ok) location.reload();
}

// ── Edit event ────────────────────────────────────────────────────────────

function editEvento(btn) {
  document.getElementById('ee-idx').value  = btn.dataset.idx;
  document.getElementById('ee-data').value = btn.dataset.date;
  document.getElementById('ee-desc').value = btn.dataset.desc;
  openModal('modal-edit-evento');
}

async function saveEditEvento() {
  const idx = document.getElementById('ee-idx').value;
  const desc = document.getElementById('ee-desc').value.trim();
  if (!desc) { alert('Informe a descrição.'); return; }
  const r = await post(`/loja/${lojaId()}/evento/${idx}`, {
    data:      document.getElementById('ee-data').value,
    descricao: desc,
  });
  if (r.ok) location.reload();
}

// ── Delete event ──────────────────────────────────────────────────────────

async function deleteEvento(btn) {
  if (!confirm('Excluir este evento?')) return;
  const idx = btn.dataset.idx;
  const r = await post(`/loja/${lojaId()}/evento/${idx}/excluir`, {});
  if (r.ok) location.reload();
}

// ── Register payment ──────────────────────────────────────────────────────

function openRegistrarPagamento() {
  document.getElementById('rp-data').value  = today();
  document.getElementById('rp-valor').value = '';
  openModal('modal-pagamento');
}

async function saveRegistrarPagamento() {
  const r = await post(`/loja/${lojaId()}/registrar-pagamento`, {
    data:  document.getElementById('rp-data').value,
    valor: document.getElementById('rp-valor').value.trim(),
  });
  if (r.ok) location.reload();
}

// ── Gateway suspension ────────────────────────────────────────────────────

function openSuspenderGateway() {
  document.getElementById('sg-data').value = '';
  openModal('modal-suspender');
}

async function saveSuspenderGateway() {
  const dataLib = document.getElementById('sg-data').value;
  const r = await post(`/loja/${lojaId()}/gateway-status`, {
    status: 'suspenso',
    data_liberacao: dataLib,
    log: true,
  });
  if (r.ok) location.reload();
}

async function reabilitarGateway() {
  if (!confirm('Confirmar reabilitação do gateway Shopify Payments?')) return;
  const r = await post(`/loja/${lojaId()}/gateway-status`, {
    status: 'normal',
    log: true,
  });
  if (r.ok) location.reload();
}

async function salvarDataLiberacao() {
  const dataLib = document.getElementById('data-liberacao-inline').value;
  const r = await post(`/loja/${lojaId()}/gateway-status`, {
    status: 'suspenso',
    data_liberacao: dataLib,
    log: false,
  });
  if (r.ok) location.reload();
}

// ── Status update ─────────────────────────────────────────────────────────

async function setStatus(val) {
  const r = await post(`/loja/${lojaId()}/status`, {status: val});
  if (r.ok) location.reload();
}

document.addEventListener('DOMContentLoaded', function() {
  const current = document.getElementById('current-status');
  if (!current) return;
  const val = current.value;
  document.querySelectorAll('.status-opt').forEach(btn => {
    if (btn.dataset.val === val) btn.classList.add('active');
    btn.addEventListener('click', () => setStatus(btn.dataset.val));
  });
});

// ── Helpers ───────────────────────────────────────────────────────────────

function today() {
  return new Date().toISOString().split('T')[0];
}
