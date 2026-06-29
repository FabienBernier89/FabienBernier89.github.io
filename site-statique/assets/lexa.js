(function(){
  // Le simulateur ne s'exécute que sur les pages qui le contiennent.
  if(!document.querySelector(".demo")) return;
  var examples=[
    { domain:"Droit des affaires", score:99,
      fr:"Chacune des Parties s'engage à conserver strictement confidentielles toutes les informations communiquées par l'autre Partie au titre du présent accord, et à ne les divulguer à aucun tiers sans son consentement écrit préalable.",
      t:{
        en:{ text:"Each Party undertakes to keep strictly confidential all information disclosed by the other Party under this agreement, and not to disclose it to any third party without its prior written consent.",
             terms:["strictly confidential","third party","prior written consent"] },
        de:{ text:"Jede Partei verpflichtet sich, sämtliche von der anderen Partei im Rahmen dieser Vereinbarung übermittelten Informationen streng vertraulich zu behandeln und sie ohne deren vorherige schriftliche Zustimmung an keinen Dritten weiterzugeben.",
             terms:["streng vertraulich","vorherige schriftliche Zustimmung","Dritten"] },
        es:{ text:"Cada una de las Partes se compromete a mantener estrictamente confidencial toda la información comunicada por la otra Parte en virtud del presente acuerdo, y a no divulgarla a ningún tercero sin su consentimiento previo por escrito.",
             terms:["estrictamente confidencial","tercero","consentimiento previo por escrito"] },
        it:{ text:"Ciascuna Parte si impegna a mantenere strettamente riservate tutte le informazioni comunicate dall'altra Parte ai sensi del presente accordo, e a non divulgarle ad alcun terzo senza il suo previo consenso scritto.",
             terms:["strettamente riservate","terzo","previo consenso scritto"] }
      }
    },
    { domain:"Droit des contrats", score:98,
      fr:"À défaut de paiement du loyer à son échéance, le présent bail sera résilié de plein droit un mois après un commandement de payer demeuré infructueux.",
      t:{
        en:{ text:"In the event of failure to pay the rent when due, this lease shall be terminated automatically one month after a formal notice to pay has remained unsuccessful.",
             terms:["terminated automatically","lease","formal notice to pay"] },
        de:{ text:"Bei nicht fristgerechter Zahlung der Miete wird dieser Mietvertrag einen Monat nach erfolgloser Zahlungsaufforderung von Rechts wegen aufgelöst.",
             terms:["Mietvertrag","von Rechts wegen","Zahlungsaufforderung"] },
        es:{ text:"En caso de impago de la renta a su vencimiento, el presente contrato de arrendamiento quedará resuelto de pleno derecho un mes después de un requerimiento de pago infructuoso.",
             terms:["de pleno derecho","contrato de arrendamiento","requerimiento de pago"] },
        it:{ text:"In caso di mancato pagamento del canone alla scadenza, il presente contratto di locazione sarà risolto di diritto un mese dopo un'ingiunzione di pagamento rimasta infruttuosa.",
             terms:["di diritto","contratto di locazione","ingiunzione di pagamento"] }
      }
    },
    { domain:"Propriété intellectuelle", score:98,
      fr:"L'Auteur cède à titre exclusif au Cessionnaire l'ensemble des droits patrimoniaux afférents à l'œuvre, pour le monde entier et pour toute la durée légale de protection.",
      t:{
        en:{ text:"The Author exclusively assigns to the Assignee all economic rights pertaining to the work, worldwide and for the entire statutory term of protection.",
             terms:["exclusively assigns","economic rights","statutory term of protection"] },
        de:{ text:"Der Urheber überträgt dem Erwerber ausschließlich sämtliche Verwertungsrechte an dem Werk, weltweit und für die gesamte gesetzliche Schutzdauer.",
             terms:["ausschließlich","Verwertungsrechte","gesetzliche Schutzdauer"] },
        es:{ text:"El Autor cede con carácter exclusivo al Cesionario la totalidad de los derechos patrimoniales correspondientes a la obra, para todo el mundo y por toda la duración legal de protección.",
             terms:["con carácter exclusivo","derechos patrimoniales","duración legal de protección"] },
        it:{ text:"L'Autore cede in via esclusiva al Cessionario l'insieme dei diritti patrimoniali relativi all'opera, per tutto il mondo e per l'intera durata legale di protezione.",
             terms:["in via esclusiva","diritti patrimoniali","durata legale di protezione"] }
      }
    }
  ];
  var $=function(id){return document.getElementById(id);};
  var src=$("dSource"), out=$("dOut"), langSel=$("dLang"), domainSel=$("dDomain"),
      btn=$("dBtn"), q=$("dQ"),
      instrBtn=$("dInstrBtn"), dot=$("dDot"), modal=$("dModal"),
      promptEl=$("dPrompt"), save=$("dSave"), cancel=$("dCancel");
  if(!src) return;
  var cur=0, lang="en", consigne="", timer=null;
  var reduce=window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function hl(text,terms){var h=esc(text);terms.forEach(function(t){var e=esc(t);h=h.replace(e,"<mark>"+e+"</mark>");});return h;}
  function resetOut(){
    if(timer){clearInterval(timer);timer=null;}
    out.innerHTML='<span class="placeholder">La traduction s\'affichera ici.</span>';
    q.classList.remove("show"); q.querySelector(".qn").textContent="0 %"; btn.disabled=false;
  }
  function loadDomain(i){cur=i; src.textContent=examples[i].fr; resetOut();}
  function setLang(){lang=langSel.value; resetOut();}
  function translate(){
    var data=examples[cur].t[lang]; if(!data) return;
    btn.disabled=true; q.classList.remove("show");
    out.innerHTML='<div class="dshim" style="width:94%"></div><div class="dshim" style="width:82%"></div><div class="dshim" style="width:88%"></div><div class="dshim" style="width:66%"></div>';
    setTimeout(function(){typeOut(data);}, reduce?0:650);
  }
  function typeOut(data){
    if(reduce){out.innerHTML=hl(data.text,data.terms); finish(); return;}
    var full=data.text, i=0;
    out.innerHTML='<span class="tt"></span><span class="dcaret"></span>';
    var tt=out.querySelector(".tt");
    timer=setInterval(function(){
      i+=2; tt.textContent=full.slice(0,i);
      if(i>=full.length){clearInterval(timer); timer=null; out.innerHTML=hl(full,data.terms); finish();}
    },16);
  }
  function finish(){
    var target=examples[cur].score||98;
    q.classList.add("show"); btn.disabled=false;
    var v=0, qn=q.querySelector(".qn");
    var it=setInterval(function(){v+=4; if(v>=target){v=target;clearInterval(it);} qn.textContent=v+" %";},22);
    if(tour.translating){tour.translating=false; setTimeout(tourComplete,320);}
  }
  function openModal(){promptEl.value=consigne; modal.classList.add("open"); if(tour.running){coach.classList.remove("show"); ring.classList.remove("show");}}
  function closeModal(){modal.classList.remove("open");}
  function saveModal(){consigne=promptEl.value.trim(); dot.classList.toggle("on", !!consigne); closeModal();}

  /* ===== Onglet Document ===== */
  var dDrop=$("dDrop"), dFile=$("dFile"), dDetect=$("dDetect"), dFileX=$("dFileX"),
      dSrcLang=$("dSrcLang"), dTargetBtn=$("dTargetBtn"), dDocDomain=$("dDocDomain"), dDocLex=$("dDocLex"),
      dDelivery=$("dDelivery"), dDocBtn=$("dDocBtn"), dLangModal=$("dLangModal"), dLangSearch=$("dLangSearch"), dLangGrid=$("dLangGrid");
  var docLangs=["Anglais (UK)","Anglais (US)","Allemand","Espagnol","Italien","Néerlandais","Portugais","Portugais (BR)","Polonais","Roumain","Grec","Suédois","Danois","Finnois","Tchèque","Slovaque","Hongrois","Bulgare","Croate","Slovène","Estonien","Letton","Lituanien","Irlandais","Maltais","Arabe","Chinois","Japonais","Coréen","Russe","Ukrainien","Turc","Hébreu","Hindi","Norvégien","Catalan"];
  var docImported=false, docTarget=null;
  var caretSvg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>';
  function buildLangGrid(f){
    dLangGrid.innerHTML="";
    docLangs.forEach(function(l){
      if(f && l.toLowerCase().indexOf(f.toLowerCase())<0) return;
      var b=mk("button","langopt"); b.type="button"; b.textContent=l;
      b.addEventListener("click",function(){pickTarget(l);});
      dLangGrid.appendChild(b);
    });
  }
  function pickTarget(l){
    docTarget=l; dTargetBtn.innerHTML=l+" "+caretSvg; dTargetBtn.classList.add("set");
    dLangModal.classList.remove("open"); maybeAdvance(dTargetBtn);
  }
  function importFile(){
    if(docImported) return; docImported=true;
    dDrop.style.display="none"; dFile.style.display="flex";
    dDetect.innerHTML='<span class="dot-detect"></span> Détection de la langue…';
    dSrcLang.textContent="Détection…"; dSrcLang.className="setv pending";
    setTimeout(function(){
      dDetect.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px"><polyline points="20 6 9 17 4 12"/></svg> Langue détectée : Français';
      dSrcLang.textContent="Français (détectée)"; dSrcLang.className="setv";
      maybeAdvance(dDrop);
    }, reduce?0:1100);
  }
  function runDocTranslate(){
    if(!docImported) importFile();
    var lang=docTarget||"Anglais (UK)";
    dDelivery.className="ddelivery show";
    dDelivery.innerHTML='<div class="dprog"><div class="dprog-steps"><span class="dprog-step" id="ps0"><span class="pdot"></span> Analyse</span><span class="dprog-step" id="ps1"><span class="pdot"></span> Traduction</span><span class="dprog-step" id="ps2"><span class="pdot"></span> Mise en page</span><span class="dprog-step" id="ps3"><span class="pdot"></span> Contrôle qualité</span></div><div class="dprog-bar"><i id="dProgBar"></i></div></div>';
    dDocBtn.disabled=true;
    var st=reduce?0:850;
    setTimeout(function(){var b=$("dProgBar"); if(b)b.style.width="100%";},60);
    var p0=$("ps0"); if(p0)p0.classList.add("on");
    setTimeout(function(){var e=$("ps1"); if(e)e.classList.add("on");}, st);
    setTimeout(function(){var e=$("ps2"); if(e)e.classList.add("on");}, st*2);
    setTimeout(function(){var e=$("ps3"); if(e)e.classList.add("on");}, st*3);
    setTimeout(function(){showDocResult(lang);}, reduce?10:(st*3+650));
  }
  function showDocResult(lang){
    var code={"Anglais (UK)":"EN","Anglais (US)":"EN","Allemand":"DE","Espagnol":"ES","Italien":"IT"}[lang]||"EN";
    dDocBtn.disabled=false;
    dDelivery.innerHTML='<div class="dresfile"><span class="fc-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></span><div class="rf-meta"><div class="rf-name">Contrat_de_prestation_Acme_'+code+'.docx</div><div class="rf-sub"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Mise en page préservée · Lexa Quality 99 %</div></div><button class="dl-btn" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg> Télécharger</button></div>';
    if(tour.translating){tour.translating=false; setTimeout(tourComplete,300);}
  }
  dDrop.addEventListener("click",importFile);
  dFileX.addEventListener("click",function(){docImported=false; dFile.style.display="none"; dDrop.style.display="flex"; dSrcLang.textContent="En attente du fichier"; dSrcLang.className="setv pending"; dDelivery.className="ddelivery"; dDelivery.innerHTML="";});
  dTargetBtn.addEventListener("click",function(){buildLangGrid(""); dLangSearch.value=""; dLangModal.classList.add("open"); if(tour.running){coach.classList.remove("show"); ring.classList.remove("show");}});
  dLangSearch.addEventListener("input",function(){buildLangGrid(dLangSearch.value);});
  dLangModal.addEventListener("click",function(e){if(e.target===dLangModal){dLangModal.classList.remove("open"); if(tour.running&&activeSteps[tour.ci]&&activeSteps[tour.ci].el===dTargetBtn)tourShow(tour.ci);}});
  dDocDomain.addEventListener("change",function(){maybeAdvance(dDocDomain);});
  dDocLex.addEventListener("change",function(){maybeAdvance(dDocLex);});
  dDocBtn.addEventListener("click",function(){ if(tour.running&&tour.ci>=0){tour.translating=true; coach.classList.remove("show"); ring.classList.remove("show"); clearTgt();} runDocTranslate(); });

  /* ===== Visite guidée (coachmarks) ===== */
  var app=document.querySelector(".demo-app");
  var textSteps=[
    {el:langSel, title:"Langue cible", msg:"Choisissez la langue de traduction.", place:"below", nextBtn:true},
    {el:domainSel, title:"Spécialisation", msg:"Sélectionnez le domaine juridique du document.", place:"below", nextBtn:true},
    {el:instrBtn, title:"Consigne", msg:"Ajoutez une instruction sur mesure (ton, terminologie…). Facultatif.", place:"right", nextBtn:true},
    {el:btn, title:"Traduction", msg:"Cliquez pour lancer la traduction.", place:"above", nextBtn:false}
  ];
  var docSteps=[
    {el:dDrop, title:"Importer un document", msg:"Importez votre fichier juridique (Word, PDF, Excel…).", place:"right", nextBtn:false},
    {el:dSrcLang, title:"Langue source détectée", msg:"Lexa détecte automatiquement la langue d'origine.", place:"below", nextBtn:true},
    {el:dTargetBtn, title:"Langue cible", msg:"Choisissez parmi plus de 40 langues spécialisées.", place:"below", nextBtn:false},
    {el:dDocDomain, title:"Catégorie du droit", msg:"Sélectionnez le domaine juridique du document.", place:"below", nextBtn:true},
    {el:dDocLex, title:"Lexique personnalisé", msg:"Appliquez votre lexique (CJUE, glossaire interne…). Facultatif.", place:"below", nextBtn:true},
    {el:dDocBtn, title:"Livraison", msg:"Lancez la traduction et téléchargez le document traduit.", place:"above", nextBtn:false}
  ];
  var textCompletion={place:"below",
    el:function(){return document.querySelector('.dtab[data-panel="doc"]') || document.getElementById("dOut");},
    title:"Traduction prête", msg:"Lexa a appliqué le lexique officiel et calculé le score qualité. À votre tour !",
    docCta:{title:"Et vos documents ?", msg:"Vous venez de voir la traduction de texte. Cliquez sur « Traduire un document » pour la suite : import de fichiers, mise en page préservée.", label:"Traduire un document ›", fn:function(){switchTab("doc");}}};
  var docCompletion={el:function(){return dDelivery;}, place:"above", title:"Document traduit", msg:"Mise en page préservée et lexique appliqué. Téléchargez votre document."};
  var activeSteps=textSteps, activeCompletion=textCompletion;
  var tour={running:false, ci:-1, translating:false}, ring=null, coach=null, started=false;
  function mk(t,c){var e=document.createElement(t); if(c)e.className=c; return e;}
  function buildCoach(){
    ring=mk("div","coach-ring"); app.appendChild(ring);
    coach=mk("div","coach");
    coach.innerHTML='<span class="carrow"></span><div class="ctitle"></div><div class="cmsg"></div><div class="cfoot"><span class="cdots"></span><span class="cact"><button class="cnext" type="button">Suivant ›</button><button class="cskip" type="button">Passer</button></span></div>';
    app.appendChild(coach);
    coach.querySelector(".cnext").addEventListener("click",tourAdvance);
    coach.querySelector(".cskip").addEventListener("click",tourEnd);
  }
  function dotsHtml(i){var h="";for(var k=0;k<activeSteps.length;k++)h+='<span class="cdot'+(k===i?" on":"")+'"></span>';return h;}
  function clearTgt(){var t=app.querySelector(".coach-target"); if(t)t.classList.remove("coach-target");}
  function placeCoach(elm,pl){
    var r=elm.getBoundingClientRect(), a=app.getBoundingClientRect();
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
  function tourShow(i){
    tour.ci=i;
    if(i>=activeSteps.length){tourComplete();return;}
    var s=activeSteps[i];
    coach.querySelector(".ctitle").textContent=s.title;
    coach.querySelector(".cmsg").textContent=s.msg;
    coach.querySelector(".cdots").innerHTML=dotsHtml(i);
    coach.querySelector(".cnext").style.display=s.nextBtn?"inline-block":"none";
    coach.querySelector(".cnext").onclick=null;
    coach.querySelector(".cskip").textContent="Passer";
    clearTgt(); s.el.classList.add("coach-target");
    setTimeout(function(){placeCoach(s.el,s.place); coach.classList.add("show"); ring.classList.add("show");},30);
  }
  function tourAdvance(){
    if(!tour.running) return;
    coach.classList.remove("show"); ring.classList.remove("show"); clearTgt();
    var n=tour.ci+1; setTimeout(function(){tourShow(n);},240);
  }
  function tourComplete(){
    clearTgt(); tour.running=false;
    var c=activeCompletion;
    var docTab=c.docCta?document.querySelector('.dtab[data-panel="doc"]'):null;
    var el=docTab||c.el();
    coach.querySelector(".ctitle").textContent=docTab?c.docCta.title:c.title;
    coach.querySelector(".cmsg").textContent=docTab?c.docCta.msg:c.msg;
    coach.querySelector(".cdots").innerHTML=dotsHtml(activeSteps.length);
    var nx=coach.querySelector(".cnext");
    if(docTab){ nx.textContent=c.docCta.label; nx.style.display="inline-block"; nx.onclick=c.docCta.fn; }
    else { nx.style.display="none"; nx.onclick=null; }
    coach.querySelector(".cskip").textContent="Terminer";
    if(docTab)el.classList.add("coach-target"); else ring.classList.remove("show");
    setTimeout(function(){placeCoach(el,c.place); coach.classList.add("show"); if(docTab)ring.classList.add("show");},30);
  }
  function tourEnd(){tour.running=false; tour.translating=false; if(coach){coach.classList.remove("show"); ring.classList.remove("show");} clearTgt();}
  function maybeAdvance(elm){if(tour.running&&activeSteps[tour.ci]&&activeSteps[tour.ci].el===elm)tourAdvance();}
  function startTour(stepsArr,completion){ if(!coach)buildCoach(); started=true; activeSteps=stepsArr; activeCompletion=completion; tour.running=true; tour.translating=false; tourShow(0); }

  langSel.addEventListener("change",function(){setLang(); maybeAdvance(langSel);});
  domainSel.addEventListener("change",function(){loadDomain(parseInt(domainSel.value,10)); maybeAdvance(domainSel);});
  instrBtn.addEventListener("click",openModal);
  save.addEventListener("click",function(){saveModal(); maybeAdvance(instrBtn);});
  cancel.addEventListener("click",function(){closeModal(); maybeAdvance(instrBtn);});
  modal.addEventListener("click",function(e){if(e.target===modal){closeModal(); maybeAdvance(instrBtn);}});
  btn.addEventListener("click",function(){ if(tour.running&&tour.ci>=0){tour.translating=true; coach.classList.remove("show"); ring.classList.remove("show"); clearTgt();} translate(); });

  /* ===== Onglets ===== */
  var tabs=Array.prototype.slice.call(document.querySelectorAll(".dtab[data-panel]"));
  var panelText=document.getElementById("panelText"), panelDoc=document.getElementById("panelDoc");
  // Motif ARIA "tabs" : roles + selection + tabindex roving (operable au clavier)
  function panelOf(name){return name==="doc"?panelDoc:panelText;}
  if(tabs.length){
    var tablist=tabs[0].parentNode;
    if(tablist){tablist.setAttribute("role","tablist"); tablist.setAttribute("aria-label","Mode de démonstration");}
    tabs.forEach(function(t){
      var name=t.getAttribute("data-panel"), on=t.classList.contains("on"), p=panelOf(name);
      t.setAttribute("role","tab");
      if(!t.id)t.id="dtab-"+name;
      if(p){p.setAttribute("role","tabpanel"); p.setAttribute("tabindex","0"); p.setAttribute("aria-labelledby",t.id); t.setAttribute("aria-controls",p.id);}
      t.setAttribute("aria-selected", on?"true":"false");
      t.setAttribute("tabindex", on?"0":"-1");
    });
  }
  function switchTab(name,focus){
    tabs.forEach(function(t){
      var sel=t.getAttribute("data-panel")===name;
      t.classList.toggle("on", sel);
      t.setAttribute("aria-selected", sel?"true":"false");
      t.setAttribute("tabindex", sel?"0":"-1");
      if(sel&&focus)t.focus();
    });
    panelText.style.display=name==="text"?"block":"none";
    panelDoc.style.display=name==="doc"?"block":"none";
    tourEnd();
    setTimeout(function(){ if(name==="doc")startTour(docSteps,docCompletion); else startTour(textSteps,textCompletion); },70);
  }
  tabs.forEach(function(t,i){
    t.addEventListener("click",function(){switchTab(t.getAttribute("data-panel"));});
    t.addEventListener("keydown",function(e){
      var k=e.key;
      if(k==="Enter"||k===" "||k==="Spacebar"){e.preventDefault(); switchTab(t.getAttribute("data-panel")); return;}
      var ni;
      if(k==="ArrowRight"||k==="ArrowDown")ni=(i+1)%tabs.length;
      else if(k==="ArrowLeft"||k==="ArrowUp")ni=(i-1+tabs.length)%tabs.length;
      else if(k==="Home")ni=0;
      else if(k==="End")ni=tabs.length-1;
      else return;
      e.preventDefault(); switchTab(tabs[ni].getAttribute("data-panel"), true);
    });
  });
  var replay=document.getElementById("dReplay"); if(replay)replay.addEventListener("click",function(){startTour(textSteps,textCompletion);});
  var replayDoc=document.getElementById("dReplayDoc"); if(replayDoc)replayDoc.addEventListener("click",function(){startTour(docSteps,docCompletion);});
  window.addEventListener("resize",function(){if(tour.running&&tour.ci>=0&&tour.ci<activeSteps.length)placeCoach(activeSteps[tour.ci].el,activeSteps[tour.ci].place);});
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!started){started=true; var demoEl=document.querySelector(".demo"); var docDefault=demoEl&&demoEl.getAttribute("data-default")==="doc"; startTour(docDefault?docSteps:textSteps, docDefault?docCompletion:textCompletion); io.disconnect();}});},{threshold:0.45});
    io.observe(document.querySelector(".demo"));
  }
  buildLangGrid("");
  loadDomain(0); setLang();
})();

/* ===== Bascule mensuel / annuel (page Tarifs) =====
   Module independant et guarde : ne s'execute que si la bascule est presente.
   Met a jour les prix (data-price-monthly / data-price-annual), le suffixe
   d'unite (par mois / par mois, facture annuellement) et l'etat actif. */
(function(){
  var toggle=document.querySelector("[data-billing-toggle]");
  if(!toggle) return;
  var opts=Array.prototype.slice.call(toggle.querySelectorAll(".bt-opt"));
  var priceEls=Array.prototype.slice.call(document.querySelectorAll("[data-price-monthly]"));
  var noteEls=Array.prototype.slice.call(document.querySelectorAll("[data-billnote]"));
  function apply(mode){
    var annual=(mode==="annual");
    toggle.setAttribute("data-active", annual?"annual":"monthly");
    opts.forEach(function(o){o.setAttribute("aria-pressed", o.getAttribute("data-billing")===mode ? "true":"false");});
    priceEls.forEach(function(el){
      var v=annual ? el.getAttribute("data-price-annual") : el.getAttribute("data-price-monthly");
      if(v!=null) el.textContent=v;
    });
    noteEls.forEach(function(el){
      el.textContent=annual ? "par utilisateur / mois, facturé annuellement" : "par utilisateur / mois";
    });
  }
  opts.forEach(function(o){
    o.addEventListener("click",function(){apply(o.getAttribute("data-billing"));});
  });
  apply("monthly");
})();
