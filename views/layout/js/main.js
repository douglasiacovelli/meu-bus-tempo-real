$(function(){
	$('form button').click(function(e){
		e.preventDefault();

		$.post('/', $("form").serialize(), callback);
	});

	$('#search-another').click(function(e){
		e.preventDefault();
		$('#search').slideToggle();
	});

	function callback(data){
	
		$.each(data, function(index, value){
			console.log(value);
			if(value.Sentido == 1){
				$('#list').append('<a href="#" class="list-group-item">Destino: '+value.DenominacaoTPTS+' - '+value.Letreiro+'-'+value.Tipo+'</a>');	
			}else{
				$('#list').append('<a href="#" class="list-group-item">Destino: '+value.DenominacaoTSTP+' - '+value.Letreiro+'-'+value.Tipo+'</a>');
			}
		});

		$('#content').slideDown();
	}

	initialize();

	$('#content').hide();

})

function initialize() {
	var mapOptions = {
		zoom: 8,
		center: new google.maps.LatLng(-34.397, 150.644),
	    disableDefaultUI: true,
	    scrollwheel: false,
	    draggable: false,
	    disableDoubleClickZoom: true
	};

	var map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);
}