/* ===== Simulateurs de demo par produit (Word / API / Writing) =====
   Moteur autonome : pour chaque .pdemo[data-sim], construit un mini-simulateur
   interactif + une visite guidee (reutilise le CSS .coach du socle).
   Garde : ne s'execute que si une .pdemo est presente. */
(function(){
  var roots = document.querySelectorAll(".pdemo[data-sim]");
  if(!roots.length) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mk = function(t,c){var e=document.createElement(t); if(c)e.className=c; return e;};

  var RAIL='<div class="drail"><span class="rlogo">Lex<span>a</span></span>'+
    '<span class="ri"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg></span>'+
    '<span class="ri on"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/></svg></span>'+
    '<span class="ri"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg></span></div>';
  var REPLAY='<button class="dreplay" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 1 3 6.7L3 16"/><path d="M3 21v-5h5"/></svg> Revoir la visite guidée</button>';
  function frame(label, inner){
    return '<div class="demo-app">'+RAIL+'<div class="dwrap"><div class="dtop"><div class="dtabs"><span class="dtab on">'+label+'</span></div><span class="dlive"><span class="pulse"></span> Démo en direct</span></div><div class="pbody">'+inner+'</div></div></div>';
  }

  /* ----- visite guidee generique ----- */
  function Tour(app){
    var ring,coach,ci=-1,running=false,steps=[],completion=null,self=this;
    function ensure(){ if(coach)return;
      ring=mk("div","coach-ring"); app.appendChild(ring);
      coach=mk("div","coach");
      coach.innerHTML='<span class="carrow"></span><div class="ctitle"></div><div class="cmsg"></div><div class="cfoot"><span class="cdots"></span><span class="cact"><button class="cnext" type="button">Suivant &rsaquo;</button><button class="cskip" type="button">Passer</button></span></div>';
      app.appendChild(coach);
      coach.querySelector(".cnext").addEventListener("click",advance);
      coach.querySelector(".cskip").addEventListener("click",end);
    }
    function clearTgt(){var t=app.querySelector(".coach-target"); if(t)t.classList.remove("coach-target");}
    function dots(i){var h="";for(var k=0;k<steps.length;k++)h+='<span class="cdot'+(k===i?" on":"")+'"></span>';return h;}
    function place(el,pl){
      var r=el.getBoundingClientRect(), a=app.getBoundingClientRect();
      var x=r.left-a.left, y=r.top-a.top;
      ring.style.left=(x-5)+"px"; ring.style.top=(y-5)+"px"; ring.style.width=(r.width+10)+"px"; ring.style.height=(r.height+10)+"px";
      var bw=coach.offsetWidth, bh=coach.offsetHeight, ar=coach.querySelector(".carrow"), bx, by;
      ar.removeAttribute("style");
      if(pl==="below"){by=y+r.height+16; bx=Math.min(Math.max(x,12),a.width-bw-12); ar.style.top="-6px"; ar.style.left=Math.min(Math.max((x+r.width/2)-bx,16),bw-16)+"px";}
      else if(pl==="above"){by=y-bh-16; bx=Math.min(Math.max(x+r.width-bw,12),a.width-bw-12); ar.style.bottom="-6px"; ar.style.left=Math.min(Math.max((x+r.width/2)-bx,16),bw-16)+"px";}
      else{bx=x+r.width+16; if(bx+bw>a.width-12){bx=x-bw-16; ar.style.right="-6px";}else{ar.style.left="-6px";} ar.style.top="18px"; by=y-4;}
      by=Math.min(Math.max(by,12),a.height-bh-12);
      coach.style.left=bx+"px"; coach.style.top=by+"px";
    }
    function show(i){
      if(!running)return;
      ci=i; if(i>=steps.length){complete();return;}
      var s=steps[i]; if(!s.el){advance();return;}
      coach.querySelector(".ctitle").textContent=s.title;
      coach.querySelector(".cmsg").textContent=s.msg;
      coach.querySelector(".cdots").innerHTML=dots(i);
      var nx=coach.querySelector(".cnext"); nx.style.display=s.nextBtn?"inline-block":"none"; nx.onclick=null;
      coach.querySelector(".cskip").textContent="Passer";
      clearTgt(); s.el.classList.add("coach-target");
      setTimeout(function(){place(s.el,s.place); coach.classList.add("show"); ring.classList.add("show");},30);
    }
    function advance(){ if(!running)return; coach.classList.remove("show"); ring.classList.remove("show"); clearTgt(); var n=ci+1; setTimeout(function(){show(n);},220); }
    function complete(){
      clearTgt(); running=false; var el=completion.el();
      coach.querySelector(".ctitle").textContent=completion.title;
      coach.querySelector(".cmsg").textContent=completion.msg;
      coach.querySelector(".cdots").innerHTML=dots(steps.length);
      coach.querySelector(".cnext").style.display="none"; coach.querySelector(".cnext").onclick=null;
      coach.querySelector(".cskip").textContent="Terminer";
      ring.classList.remove("show");
      setTimeout(function(){ if(el)place(el,completion.place); coach.classList.add("show");},30);
    }
    function end(){ running=false; if(coach){coach.classList.remove("show"); ring.classList.remove("show");} clearTgt(); }
    self.start=function(st,comp){ ensure(); steps=st; completion=comp; running=true; show(0); };
    self.hideForAction=function(){ if(coach){coach.classList.remove("show"); ring.classList.remove("show");} clearTgt(); };
    self.complete=function(){ if(running) complete(); };
    self.running=function(){return running;};
    self.relayout=function(){ if(running&&ci>=0&&ci<steps.length&&steps[ci].el)place(steps[ci].el,steps[ci].place); };
  }

  function q(root,sel){return root.querySelector(sel);}
  function el(root,sel){return function(){return root.querySelector(sel);};}

  /* ----- branchement commun (autostart + replay + bouton action) ----- */
  function setup(root, html, buildSteps, completion, play, resetFn){
    root.innerHTML = html;
    var app = q(root,".demo-app");
    var tour = new Tour(app);
    var startFn=function(){ if(resetFn)resetFn(root); tour.start(buildSteps(root,tour), completion(root)); };
    var actionBtn = q(root,"[data-action]");
    if(actionBtn) actionBtn.addEventListener("click",function(){
      tour.hideForAction();
      play(root, function(){ tour.complete(); });
    });
    var rep = q(root,".dreplay"); if(rep) rep.addEventListener("click",startFn);
    window.addEventListener("resize",function(){tour.relayout();});
    var done=false;
    if("IntersectionObserver" in window){
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!done){done=true; startFn(); io.disconnect();}});},{threshold:0.4});
      io.observe(root);
    } else { startFn(); }
  }

  /* ================= WORD ================= */
  function initWord(root){
    var SEG=[
      {fr:'Le Cédant garantit au Cessionnaire que les actions cédées sont libres de tout nantissement, gage ou sûreté, et qu\'aucune procédure n\'est en cours susceptible d\'en affecter la propriété.',
       en:'The Transferor warrants to the Transferee that the transferred shares are free from any pledge, lien or security interest, and that no proceedings are pending that could affect their ownership.'},
      {fr:'En cas de violation de cette garantie, le Cédant s\'engage à indemniser le Cessionnaire de l\'intégralité du préjudice subi, dans un délai de trente (30) jours à compter de la notification.',
       en:'In the event of a breach of this warranty, the Transferor undertakes to indemnify the Transferee for the entire loss suffered, within thirty (30) days of notification.'}
    ];
    var segHtml=SEG.map(function(s,i){return '<p class="wseg sel" data-seg="'+i+'">'+s.fr+'</p>';}).join('');
    var win=
      '<div class="word-win">'+
        '<div class="word-bar"><span class="wd"></span><span class="wd"></span><span class="wd"></span><span class="wt">Contrat_de_cession.docx · Word</span><span class="word-live"><span class="pulse"></span> Démo en direct</span></div>'+
        '<div class="word-rib"><span class="tabb">Accueil</span><span class="tabb">Insertion</span><span class="tabb">Mise en page</span><span class="tabb">Révision</span><span class="tabb lexa" data-lexatab>Lex<span>a</span></span></div>'+
        '<div class="word-body">'+
          '<div class="word-paper" data-doc>'+
            '<div class="wdoc-h">Article 7 · Garanties et indemnisation</div>'+
            segHtml+
            '<p class="wseg wmuted">Les autres stipulations du protocole demeurent inchangées.</p>'+
          '</div>'+
          '<aside class="word-pane">'+
            '<div class="wp-head"><span class="wp-dot"></span> Lexa · Traduction</div>'+
            '<div class="pf">Langue cible</div><div class="pbox" data-lang>Anglais (UK)</div>'+
            '<div class="pf">Domaine du droit</div><div class="pbox" data-domain>Droit des sociétés</div>'+
            '<div class="pf">Étendue</div><div class="pbox">Sélection (2 paragraphes)</div>'+
            '<button class="pbtn" type="button" data-action>Traduire la sélection</button>'+
            '<div class="wp-note"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg> Lexiques officiels appliqués automatiquement, mise en forme conservée.</div>'+
            REPLAY+
          '</aside>'+
        '</div>'+
      '</div>';
    function steps(r){ return [
      {el:q(r,"[data-lexatab]"), title:"Le complément Lexa", msg:"Lexa s'ajoute au ruban de Word, comme un complément Microsoft.", place:"below", nextBtn:true},
      {el:q(r,"[data-lang]"), title:"Langue cible", msg:"Choisissez la langue de traduction parmi plus de 40.", place:"below", nextBtn:true},
      {el:q(r,"[data-domain]"), title:"Domaine du droit", msg:"Sélectionnez la branche du droit : Lexa applique sa terminologie.", place:"below", nextBtn:true},
      {el:q(r,"[data-action]"), title:"Traduire la sélection", msg:"Le passage sélectionné est traduit directement dans le document.", place:"above", nextBtn:false}
    ];}
    var completion=function(r){return {el:el(r,"[data-doc]"), place:"below", title:"Traduit dans Word", msg:"Le passage sélectionné est traduit en anglais dans le document, la mise en forme est conservée."};};
    function play(r, done){
      var segs=r.querySelectorAll("[data-doc] .wseg.sel"), i=0;
      function step(){
        if(i<segs.length){
          var s=segs[i]; s.classList.add("translating");
          (function(seg){ setTimeout(function(){ seg.innerHTML=SEG[+seg.getAttribute("data-seg")].en; seg.classList.remove("translating"); seg.classList.add("tr"); }, reduce?0:420); })(s);
          i++; setTimeout(step, reduce?0:780);
        } else {
          var b=q(r,"[data-action]"); b.classList.add("done"); b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Traduit · Lexa Quality 99 %';
          setTimeout(function(){done&&done();}, reduce?10:400);
        }
      }
      step();
    }
    function reset(r){ r.querySelectorAll("[data-doc] .wseg.sel").forEach(function(s){ s.classList.remove("tr","translating"); s.innerHTML=SEG[+s.getAttribute("data-seg")].fr; }); var b=q(r,"[data-action]"); if(b){b.classList.remove("done"); b.textContent="Traduire la sélection";} }
    setup(root, '<div class="demo-app">'+win+'</div>', steps, completion, play, reset);
  }

  /* ================= API ================= */
  function initApi(root){
    var req='<div class="code-win"><div class="code-bar"><span class="d"></span><span class="d"></span><span class="d"></span><span class="verb">POST</span><span class="path">/v1/translations</span></div>'+
      '<pre><code><span class="c-com"># Requête</span>\n'+
      '<span class="c-fn">curl</span> -X POST https://api.lexamt.com/v1/translations \\\n'+
      '  -H <span class="c-str">"Authorization: Bearer VOTRE_CLE"</span> \\\n'+
      '  -d <span class="c-str">\'{ "source_lang": "fr", "target_lang": "en",</span>\n'+
      '       <span class="c-key" data-param>"domain": "droit_des_contrats"</span> <span class="c-str">}\'</span></code></pre></div>';
    var resp='<div class="code-win api-resp"><div class="code-bar"><span class="verb ok">200 OK</span><span class="path">reponse</span></div>'+
      '<pre><code>{\n  <span class="c-key">"id"</span>: <span class="c-str">"trn_8f2a1c"</span>,\n  <span class="c-key">"status"</span>: <span class="c-str">"completed"</span>,\n  <span class="c-key">"quality_score"</span>: 99\n}</code></pre></div>';
    var inner='<div class="api-demo">'+req+'<button class="api-send" type="button" data-action>Envoyer la requête</button>'+resp+REPLAY+'</div>';
    function steps(r){return [
      {el:q(r,"[data-param]"), title:"Vos paramètres", msg:"Langue et domaine du droit : Lexa applique le moteur spécialisé et les lexiques adaptés.", place:"below", nextBtn:true},
      {el:q(r,"[data-action]"), title:"Envoyer la requête", msg:"Lancez l'appel : la traduction juridique revient instantanément.", place:"above", nextBtn:false}
    ];}
    var completion=function(r){return {el:el(r,".api-resp"), place:"above", title:"Réponse reçue", msg:"Traduction et score qualité renvoyés en JSON, prêts à intégrer dans vos outils."};};
    function play(r, done){ var b=q(r,"[data-action]"); b.disabled=true; setTimeout(function(){ q(r,".api-resp").classList.add("show"); b.disabled=false; setTimeout(function(){done&&done();}, reduce?10:450);}, reduce?0:520); }
    function reset(r){ var x=q(r,".api-resp"); if(x)x.classList.remove("show"); var b=q(r,"[data-action]"); if(b)b.disabled=false; }
    setup(root, frame("API REST", inner), steps, completion, play, reset);
  }

  /* ================= WRITING ================= */
  function initWriting(root){
    var RES={
      reformuler:'La société <strong>Durand &amp; Associés</strong> s\'engage à verser 45 000 euros à M. Martin à titre d\'indemnité transactionnelle.',
      anonymiser:'La société <mark>[SOCIÉTÉ A]</mark> versera <mark>[MONTANT]</mark> à <mark>[PARTIE B]</mark> au titre de l\'indemnité transactionnelle.',
      resumer:'Indemnité transactionnelle de 45 000 euros versée par Durand &amp; Associés à M. Martin (article 4).'
    };
    var PH='Choisissez une action puis cliquez sur Appliquer.';
    var inner='<div class="wr-demo">'+
      '<div class="wr-cols">'+
        '<div class="wr-card"><div class="wr-h">Texte source</div><div>La société <strong>Durand &amp; Associés</strong> versera la somme de <strong>45 000 euros</strong> à Monsieur <strong>Martin</strong> au titre de l\'indemnité transactionnelle prévue à l\'article 4 du protocole.</div></div>'+
        '<div class="wr-card wr-out"><div class="wr-h">Résultat</div><span data-out class="wr-ph">'+PH+'</span></div>'+
      '</div>'+
      '<div class="wr-bar">'+
        '<div class="wr-modes" data-modes><button class="wmode" type="button" data-mode="reformuler">Reformuler</button><button class="wmode on" type="button" data-mode="anonymiser">Anonymiser</button><button class="wmode" type="button" data-mode="resumer">Résumer</button></div>'+
        '<button class="wr-apply" type="button" data-action>Appliquer</button>'+
      '</div>'+
      REPLAY+'</div>';
    function steps(r){return [
      {el:q(r,"[data-modes]"), title:"Choisissez l'action", msg:"Reformuler, anonymiser ou résumer, selon votre besoin.", place:"above", nextBtn:true},
      {el:q(r,"[data-action]"), title:"Appliquer", msg:"Lexa adapte le texte en conservant le sens et la terminologie juridiques.", place:"above", nextBtn:false}
    ];}
    var completion=function(r){return {el:el(r,".wr-out"), place:"above", title:"Texte adapté", msg:"Le texte est transformé selon le mode choisi, prêt à être réutilisé."};};
    function mode(r){var a=r.querySelector(".wmode.on"); return a?a.getAttribute("data-mode"):"anonymiser";}
    function play(r, done){ var o=q(r,"[data-out]"); o.classList.remove("wr-ph"); o.innerHTML=RES[mode(r)]; q(r,".wr-out").classList.add("show"); setTimeout(function(){done&&done();}, reduce?10:450); }
    function reset(r){ var out=q(r,".wr-out"); if(out)out.classList.remove("show"); var o=q(r,"[data-out]"); if(o){o.className="wr-ph"; o.textContent=PH;} }
    setup(root, frame("Lexa Writing", inner), steps, completion, play, reset);
    root.querySelectorAll(".wmode").forEach(function(m){m.addEventListener("click",function(){root.querySelectorAll(".wmode").forEach(function(x){x.classList.remove("on");}); m.classList.add("on"); reset(root);});});
  }

  var BUILDERS={ word:initWord, api:initApi, writing:initWriting };
  roots.forEach(function(root){ var t=root.getAttribute("data-sim"); if(BUILDERS[t]){ try{ BUILDERS[t](root); }catch(e){} } });
})();
