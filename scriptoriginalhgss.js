
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
	var cols = 10;
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
	var cols = 10;
	var row = table.insertRow(table.rows.length);

	var dex = row.insertCell(0);
	dex.innerHTML = FormatNumberLength(poke.dex, 3);

	var name = row.insertCell(1);
	name.innerHTML = '<img src=\"pokes/' + FormatNumberLength(poke.dex, 3) + 'MS.png\" style="vertical-align:middle" onclick=\"clickimg(\'' + poke.dex + '\')\"> ' + poke.name;
	name.style.textAlign = "left";

	var place = row.insertCell(2);
	place.innerHTML = poke.place;

	var subloc = row.insertCell(3);
	subloc.innerHTML = poke.subloc;

	var game = row.insertCell(4);
	game.innerHTML = poke.game;

	var method = row.insertCell(5);
	method.innerHTML = poke.method;

	var levelmin = row.insertCell(6);
	levelmin.innerHTML = poke.levelmin;

	var levelmax = row.insertCell(7);
	levelmax.innerHTML = poke.levelmax;

	var prob = row.insertCell(8);
	prob.innerHTML = poke.prob;

	var specialprob = row.insertCell(9);
	specialprob.innerHTML = poke.specialprob;

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
		document.getElementById("restantes").innerHTML = 'Quedan <b style="color:#3178ea;">' + data.length + '</b> Pokémon.'
	}
	xhr.open("POST", "/post", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		poke: document.getElementById("pokename").value
	}));
}

function clickimg(dex){
	var xhr = new XMLHttpRequest();
	xhr.onload = function(){
		getPoke()
	}
	xhr.open("POST", "/catch", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		dex: dex,
	}));
}

function startScripts(){
	getPoke();
}

window.onload = startScripts;
