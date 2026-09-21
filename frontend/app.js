const API = window.location.origin;
let leads = [];

function showPage(page){
  document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
  document.getElementById(page).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(x=>x.classList.toggle('active',x.dataset.page===page));
  const titles={dashboard:'Dashboard',leads:'Lead Management',discovery:'Buyer Discovery',outreach:'Outreach',followups:'Follow-ups',analytics:'Analytics'};
  document.getElementById('pageTitle').textContent=titles[page]||'Dashboard';
  if(page==='leads') renderLeads();
  if(page==='followups') loadFollowups();
  if(page==='analytics') renderAnalytics();
}
document.querySelectorAll('.nav-item').forEach(x=>x.addEventListener('click',()=>showPage(x.dataset.page)));

async function api(path, options={}){
  const r=await fetch(API+path,options);
  let data={};
  try{data=await r.json()}catch(_){}
  if(!r.ok) throw new Error(data.detail||data.message||`Request failed (${r.status})`);
  return data;
}

function toast(msg){
  const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2600);
}
function esc(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
function badge(v){
  const c=(v||'').toLowerCase();
  let cls=c.includes('valid')?'valid':c.includes('sent')?'sent':c.includes('ready')?'ready':c.includes('pending')?'pending':'';
  return `<span class="badge ${cls}">${esc(v||'—')}</span>`;
}

async function loadAll(){
  try{
    const [summary, leadData] = await Promise.all([api('/outreach/summary'),api('/leads')]);
    leads=Array.isArray(leadData)?leadData:(leadData.leads||[]);
    setStats(summary);
    renderRecent();
    renderLeads();
    renderPipeline(summary);
    renderAnalytics();
    document.getElementById('apiStatus').textContent='API connected';
    document.querySelector('.status-dot').style.background='#39c981';
  }catch(e){
    document.getElementById('apiStatus').textContent='API unavailable';
    document.querySelector('.status-dot').style.background='#ef6b73';
    toast(e.message);
  }
  loadFollowups();
}
function setStats(s){
  document.getElementById('sTotal').textContent=s.total_leads??0;
  document.getElementById('sNotContacted').textContent=s.not_contacted??0;
  document.getElementById('sReady').textContent=s.ready_to_send??0;
  document.getElementById('sSent').textContent=s.sent??0;
  document.getElementById('sFollowups').textContent=s.follow_up_pending??0;
  document.getElementById('sResponses').textContent=s.responses_received??0;
}
function leadRows(items){
  if(!items.length)return '<div class="loading">No leads found.</div>';
  return `<table class="table"><thead><tr><th>Company</th><th>Country</th><th>Email</th><th>Validation</th><th>Outreach</th></tr></thead><tbody>${
    items.map(l=>`<tr><td><strong>${esc(l.company_name)}</strong><br><small>${esc(l.product_category||'')}</small></td><td>${esc(l.country)}</td><td>${esc(l.email||'—')}</td><td>${badge(l.validation_status)}</td><td>${badge(l.outreach_status)}</td></tr>`).join('')
  }</tbody></table>`;
}
function renderRecent(){document.getElementById('recentLeads').innerHTML=leadRows(leads.slice(-6).reverse());}
function renderLeads(){
  const q=(document.getElementById('leadSearch')?.value||'').toLowerCase();
  const sf=document.getElementById('statusFilter')?.value||'';
  const vf=document.getElementById('validationFilter')?.value||'';
  const filtered=leads.filter(l=>{
    const text=[l.company_name,l.country,l.email,l.website,l.product_category].join(' ').toLowerCase();
    return (!q||text.includes(q))&&(!sf||l.lead_status===sf)&&(!vf||l.validation_status===vf);
  });
  const box=document.getElementById('leadsTable'); if(box)box.innerHTML=leadRows(filtered);
}
function renderPipeline(s){
  const vals=[
    ['Not contacted',s.not_contacted||0],['Ready to send',s.ready_to_send||0],
    ['Sent',s.sent||0],['Responses',s.responses_received||0]
  ];
  const total=Math.max(s.total_leads||1,1);
  document.getElementById('pipeline').innerHTML=vals.map(([n,v])=>`<div class="pipeline-row"><div class="pipeline-label"><span>${n}</span><strong>${v}</strong></div><div class="bar"><span style="width:${Math.min(100,v/total*100)}%"></span></div></div>`).join('');
}
async function discoverBuyers(){
  const body={
    product_category:document.getElementById('dProduct').value.trim(),
    target_country:document.getElementById('dCountry').value.trim(),
    industry:document.getElementById('dIndustry').value.trim(),
    keywords:document.getElementById('dKeywords').value.trim()
  };
  if(!body.product_category||!body.target_country){toast('Product category and country are required');return;}
  const box=document.getElementById('discoveryResults');box.textContent='Searching...';
  try{
    const data=await api('/buyers/discover/import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    box.innerHTML=`<strong>${esc(data.message||'Discovery complete')}</strong>\n\nDiscovered: ${data.discovered_count??0}\nDuplicates: ${data.duplicate_count??0}\n\n${(data.candidates||[]).slice(0,10).map(x=>`• ${esc(x.company_name)} — ${esc(x.country)}\n  ${esc(x.website)}`).join('\n')||'No candidates returned.'}`;
    toast('Buyer discovery completed'); await loadAll();
  }catch(e){box.textContent=e.message;toast(e.message)}
}
async function prepareOutreach(){
  const id=document.getElementById('outreachLeadId').value;
  if(!id)return toast('Enter a lead ID');
  try{
    const d=await api(`/leads/${id}/outreach/prepare`,{method:'POST'});
    document.getElementById('outreachResult').textContent=
      `Prepared successfully\n\nCompany: ${d.company_name||''}\nEmail: ${d.email||''}\nStatus: ${d.outreach_status||''}\nSubject: ${d.subject||d.outreach_subject||''}\nFollow-up: ${d.follow_up_at||''}`;
    toast('Outreach prepared');
    await loadAll();
  }catch(e){document.getElementById('outreachResult').textContent=e.message;toast(e.message)}
}
async function sendOutreach(){
  const id=document.getElementById('outreachLeadId').value;
  if(!id)return toast('Enter a lead ID');
  if(!confirm('Send this outreach email through Gmail?'))return;
  try{
    const d=await api(`/leads/${id}/outreach/send`,{method:'POST'});
    document.getElementById('outreachResult').textContent=JSON.stringify(d,null,2);
    toast('Email sent successfully');
    await loadAll();
  }catch(e){document.getElementById('outreachResult').textContent=e.message;toast(e.message)}
}
async function loadFollowups(){
  const box=document.getElementById('followupTable'); if(!box)return;
  try{
    const d=await api('/outreach/follow-ups/due');
    const rows=d.follow_ups||[];
    box.innerHTML=rows.length?leadRows(rows):'<div class="loading">No follow-ups are due right now.</div>';
  }catch(e){box.innerHTML=`<div class="loading">${esc(e.message)}</div>`;}
}
function renderAnalytics(){
  const s=window.__summary||{};
  ['aTotal','aSent','aResponses','aFollowups'].forEach((id,i)=>document.getElementById(id).textContent=[s.total_leads,s.sent,s.responses_received,s.follow_up_pending][i]??0);
  const total=Math.max(s.total_leads||1,1);
  document.getElementById('analyticsBars').innerHTML=[
    ['Not Contacted',s.not_contacted||0],['Ready to Send',s.ready_to_send||0],['Sent',s.sent||0],['Responses',s.responses_received||0]
  ].map(([n,v])=>`<div class="pipeline-row"><div class="pipeline-label"><span>${n}</span><strong>${v}</strong></div><div class="bar"><span style="width:${Math.min(100,v/total*100)}%"></span></div></div>`).join('');
}
const oldSetStats=setStats;
setStats=function(s){window.__summary=s;oldSetStats(s);renderAnalytics();};
loadAll();
