(() => {
  const $ = id => document.getElementById(id);
  const mapConfig = window.TELEMETRY_CONFIG.maps;
  const mapSelect=$("mapSelect"), dateSelect=$("dateSelect"), matchSelect=$("matchSelect");
  const canvas=$("overlay"), ctx=canvas.getContext("2d"), image=$("minimap");
  let events=[], mode="journeys", progress=100, playing=false, timer=null;
  const colors={Kill:"#ff5252",Killed:"#ff8c42",BotKill:"#ff5252",BotKilled:"#ff8c42",KilledByStorm:"#22d3ee",Loot:"#facc15"};
  const number=n=>Number(n||0).toLocaleString();
  const selectedMap=()=>mapConfig[mapSelect.value];
  const query=()=>new URLSearchParams({map:mapSelect.value,date:dateSelect.value,match:matchSelect.value,humans:$("humans").checked?"1":"0",bots:$("bots").checked?"1":"0"});
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cfg=selectedMap(), px=x=>(x-cfg.origin_x)/cfg.scale*canvas.width, py=z=>(1-(z-cfg.origin_z)/cfg.scale)*canvas.height;
    const maxTs=events.reduce((m,e)=>Math.max(m,e.timestamp_ms),0), minTs=events.reduce((m,e)=>Math.min(m,e.timestamp_ms),Number.POSITIVE_INFINITY);
    const cutoff=minTs+(maxTs-minTs)*progress/100;
    const visible=events.filter(e=>e.timestamp_ms<=cutoff);
    if(mode==="journeys"){
      const groups=new Map();
      visible.filter(e => {
    if (e.event_type === "Position" && !$("humans").checked) return false;
    if (e.event_type === "BotPosition" && !$("bots").checked) return false;

    return e.event_type === "Position" || e.event_type === "BotPosition";
    }).forEach(e => {
        const key = e.match_id + "::" + e.user_id;

        if(!groups.has(key))groups.set(key,[]);
        groups.get(key).push(e);
      });
      groups.forEach(points=>{
        points.sort((a,b)=>a.timestamp_ms-b.timestamp_ms);
        if(points.length<2)return;
        ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(px(p.x),py(p.z)):ctx.moveTo(px(p.x),py(p.z)));
        ctx.strokeStyle=points[0].is_bot?"rgba(167,139,250,.55)":"rgba(111,168,255,.72)";ctx.lineWidth=1.5;ctx.stroke();
        const last=points[points.length-1];ctx.beginPath();ctx.arc(px(last.x),py(last.z),3,0,Math.PI*2);ctx.fillStyle=points[0].is_bot?"#a78bfa":"#6fa8ff";ctx.fill();
      });
    } else {
      const bins=new Map();
      visible.forEach(e=>{
        const relevant=mode==="traffic"?(e.event_type==="Position"||e.event_type==="BotPosition"):mode==="kills"?["Kill","BotKill"].includes(e.event_type):["Killed","BotKilled","KilledByStorm"].includes(e.event_type);
        if(!relevant)return;
        const bx=Math.floor(px(e.x)/18),by=Math.floor(py(e.z)/18),key=bx+","+by;bins.set(key,(bins.get(key)||0)+1);
      });
      const max=Math.max(1,...bins.values());
      bins.forEach((n,key)=>{const [x,y]=key.split(",").map(Number),alpha=.12+n/max*.55;ctx.beginPath();ctx.arc(x*18+9,y*18+9,7+n/max*16,0,Math.PI*2);ctx.fillStyle=mode==="kills"?`rgba(255,65,65,${alpha})`:mode==="deaths"?`rgba(255,150,45,${alpha})`:`rgba(40,190,255,${alpha})`;ctx.fill()});
    }
    if($("events").checked)visible.filter(e=>!["Position","BotPosition"].includes(e.event_type)).forEach(e=>{ctx.beginPath();ctx.arc(px(e.x),py(e.z),5,0,Math.PI*2);ctx.fillStyle=colors[e.event_type]||"#fff";ctx.fill();ctx.lineWidth=1.5;ctx.strokeStyle="#111";ctx.stroke()});
  }
  async function loadFilters(){
    const params=new URLSearchParams({map:mapSelect.value,date:dateSelect.value});
    const res=await fetch("/api/filters/?"+params),data=await res.json();
    const oldDate=dateSelect.value,oldMatch=matchSelect.value;
    dateSelect.innerHTML='<option value="all">All dates</option>'+data.dates.map(d=>`<option value="${d}">${d}</option>`).join("");
    dateSelect.value=data.dates.includes(oldDate)?oldDate:"all";
    matchSelect.innerHTML='<option value="all">All matches</option>'+data.matches.map(m=>`<option value="${m}">${m}</option>`).join("");
    matchSelect.value=data.matches.includes(oldMatch)?oldMatch:"all";
  }
  async function loadData(){
    $("statusText").textContent="LOADING TELEMETRY";
    try{
      const res=await fetch("/api/telemetry/?"+query());if(!res.ok)throw new Error("Telemetry API returned "+res.status);
      const data=await res.json();events=data.events;progress=100;$("progress").value=100;
      $("players").textContent=number(data.stats.players);$("kills").textContent=number(data.stats.kills);$("deaths").textContent=number(data.stats.deaths);$("loot").textContent=number(data.stats.loot);
      $("mapTitle").textContent=selectedMap().label;$("timelineMatch").textContent=matchSelect.value==="all"?"All matches":matchSelect.value;
      $("emptyState").hidden=events.length>0;$("statusText").textContent=number(data.total)+" EVENTS LOADED";$("dbStatus").style.background="#65d69a";
      $("notice").hidden=!data.truncated;if(data.truncated)$("notice").textContent="Showing the first 60,000 events for this filter. Narrow by date or match for a complete view.";
      draw();
    }catch(err){$("statusText").textContent="API ERROR";$("dbStatus").style.background="#e5a44c";$("emptyState").hidden=false;$("emptyState").querySelector("b").textContent="Could not load telemetry";$("emptyState").querySelector("p").textContent=err.message}
  }
  async function refresh(){await loadFilters();await loadData()}
  mapSelect.addEventListener("change",async()=>{const m=selectedMap();image.src="/static/"+m.image;await refresh()});
  dateSelect.addEventListener("change",refresh);matchSelect.addEventListener("change",loadData);
  ["humans","bots","events"].forEach(id=>$(id).addEventListener("change",loadData));
  document.querySelectorAll(".mode").forEach(b=>b.addEventListener("click",()=>{document.querySelector(".mode.active")?.classList.remove("active");b.classList.add("active");mode=b.dataset.mode;draw()}));
  $("progress").addEventListener("input",e=>{progress=Number(e.target.value);$("timePct").textContent=progress+"% OF TIMELINE";$("timeState").textContent=progress>=100?"END":"PLAYBACK";draw()});
  $("play").addEventListener("click",()=>{if(playing){clearInterval(timer);playing=false;$("play").textContent="▶";return}if(progress>=100){progress=0;$("progress").value=0}playing=true;$("play").textContent="Ⅱ";timer=setInterval(()=>{progress=Math.min(100,progress+1);$("progress").value=progress;$("timePct").textContent=progress+"% OF TIMELINE";$("timeState").textContent=progress>=100?"END":"PLAYBACK";draw();if(progress>=100){clearInterval(timer);playing=false;$("play").textContent="▶"}},120)});
  $("reset").addEventListener("click",()=>{progress=100;$("progress").value=100;draw()});
  refresh();
})();