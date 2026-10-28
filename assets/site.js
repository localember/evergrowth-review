(function(){
  var subs=document.querySelectorAll('.nav .has-sub');
  function closeAll(except){subs.forEach(function(li){if(li!==except){li.classList.remove('open');var b=li.querySelector('.nav-link');if(b)b.setAttribute('aria-expanded','false');}});}
  subs.forEach(function(li){
    var b=li.querySelector('.nav-link');
    b.addEventListener('click',function(e){e.preventDefault();var o=!li.classList.contains('open');closeAll(li);li.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');});
  });
  document.addEventListener('click',function(e){if(!e.target.closest('.nav'))closeAll();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();closeMobile();}});
  var burger=document.getElementById('burger'),mnav=document.getElementById('mobile-nav');
  function closeMobile(){if(!mnav)return;mnav.classList.remove('open');burger.setAttribute('aria-expanded','false');}
  if(burger){burger.addEventListener('click',function(){var o=!mnav.classList.contains('open');mnav.classList.toggle('open',o);burger.setAttribute('aria-expanded',o?'true':'false');});}
  document.querySelectorAll('.m-item>button').forEach(function(b){b.addEventListener('click',function(){var p=b.parentNode;var o=!p.classList.contains('open');p.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');});});
})();
