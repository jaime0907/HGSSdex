
var franjahoraria = 0;

function getHora(){
	var d = new Date();
	var d2 = new Date();
	var h = d.getHours();
	var ht = '';
	if(h >= 4 && h < 10){
		ht = 'Mañana';
		franjahoraria = 0;
		d2.setHours(10);
		d2.setMinutes(0);
		d2.setSeconds(0);
	}else if(h >= 10 && h < 20){
		ht = 'Día';
		franjahoraria = 1;
		d2.setHours(20);
		d2.setMinutes(0);
		d2.setSeconds(0);
	}else{
		ht = 'Noche';
		franjahoraria = 2;
		if(h > 5){
			d2.setDate(d2.getDate() + 1);
		}
		d2.setHours(4);
		d2.setMinutes(0);
		d2.setSeconds(0);
	}
	var hours = (d2-d)/1000/60/60;
	var min = (hours - Math.floor(hours)) * 60;
	var hourst = Math.floor(hours);
	var mint = Math.floor(min);

	var plural = 1;
	var remain = '(';
	if(hourst == 1)
	{
		remain += hourst + ' hora';
		plural = 0;
	}else if(hourst != 0)
	{
		remain += hourst + ' horas';
		plural = 1;
	}

	if(hourst != 0) remain += ' y ';
	if(mint == 1)
	{
		remain += mint + ' minuto';
		plural = 0;
	}else if(mint != 0)
	{
		remain += mint + ' minutos';
		plural = 1;
	}
	remain += ' restante';
	if(plural == 1){
		remain += 's';
	}
	remain += ')';
	document.getElementById("demo").innerHTML = 'Franja horaria HGSS: ' + ht + ' ' + remain;
}

function addRow(){
	var table = document.getElementById("tablepoke");
	var rows = 1;
	var cols = 3;
	var row = table.insertRow(0);
	for(var c = 0; c < cols; c++)
	{
		var cel = row.insertCell(c);
		cel.innerHTML = c;
	}
}

function FormatNumberLength(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
}

function addRowPoke(poke, lastpoke){
	var table = document.getElementById("tablepoke");
	var rows = 1;
	var cols = 3;
	var row = table.insertRow(table.rows.length);

	var dex = row.insertCell(0);
	dex.innerHTML = FormatNumberLength(poke.dex, 3);

	var name = row.insertCell(1);
	name.innerHTML = '<img src=\"static/pokes/' + FormatNumberLength(poke.dex, 3) + 'MS.png\" style="vertical-align:middle"> ' + poke.name;
	name.style.textAlign = "left";

	var place = row.insertCell(2);
	place.innerHTML = poke.place;

	var game = row.insertCell(3);
	switch(poke.game){
		case 0:
			game.innerHTML = 'HG';
			break;
		case 1:
			game.innerHTML = 'SS';
			break;
		case 2:
			game.innerHTML = 'HGSS';
			break;
		default:
			game.innerHTML = '';
			break;
	}

	var method = row.insertCell(4);
	method.innerHTML = poke.method;

	var level = row.insertCell(5);
	if(poke.levelmax == poke.levelmin){
		level.innerHTML = poke.levelmax;
	}else{
		level.innerHTML = poke.levelmin + '-' + poke.levelmax;
	}

	var prob1 = row.insertCell(6);
	if(poke.probdawn <= 0){
		prob1.innerHTML = '';
	}else{
		prob1.innerHTML = poke.probdawn + '%';
	}

	var prob2 = row.insertCell(7);
	if(poke.probday <= 0){
		prob2.innerHTML = '';
	}else{
		prob2.innerHTML = poke.probday + '%';
	}

	var prob3 = row.insertCell(8);
	if(poke.probnight <= 0){
		prob3.innerHTML = '';
	}else{
		prob3.innerHTML = poke.probnight + '%';
	}

	switch(franjahoraria){
		case 0:
			prob1.style.backgroundColor = "#ffe8fd"
			break;
		case 1:
			prob2.style.backgroundColor = "#ffe8fd"
			break;
		case 2:
			prob3.style.backgroundColor = "#ffe8fd"
			break;
		default:
			break;
	}

	if(poke.dex != lastpoke && document.getElementById("groupselector").value == 0){
		row.style.backgroundColor = "#ffeec4"
	}

}
function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie != '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) == (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
	 return cookieValue;
}
function getPoke(){
	var xhr = new XMLHttpRequest();
	xhr.onload = function(){
		var lastpoke = 0;
		var status = xhr.status; // HTTP response status, e.g., 200 for "200 OK"
		var data = JSON.parse(xhr.responseText); // Returned data, e.g., an HTML document.
		var table = document.getElementById("tablepoke");
		for(var j=table.rows.length-1;j>0;j--){
			table.deleteRow(j);
		}
		var limit = document.getElementById("limit").value;
		for(var i=0;i<data.length;i++){
			if(limit != '' && !isNaN(limit) && limit < i){
				break;
			}
			addRowPoke(data[i], lastpoke);
			lastpoke = data[i].dex;
		}
	}
	xhr.open("POST", "/post", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	xhr.send(JSON.stringify({
		poke: document.getElementById("pokename").value,
		game: document.getElementById("gameselector").value,
		group: document.getElementById("groupselector").value,
		limit: document.getElementById("limit").value
	}));
}


function startScripts(){
	getPoke();
}

window.onload = startScripts;
