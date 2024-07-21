const menu = document.getElementById('menubar');
const menutimes = document.getElementById('menutimes');
menu.addEventListener('click', ()=>{
    const list = document.querySelector('nav .items > div:nth-child(2)');
    list.style.display ="flex"
});
menutimes.addEventListener('click', ()=>{
    const list = document.querySelector('nav .items > div:nth-child(2)');
    list.style.display ="none";
});