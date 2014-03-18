var map;
var markers = [];
var interval;
var trafficLayer;

$(function(){
	$('form').submit(function(e){
		$(this).find('button').attr('disabled',true);
		$(this).find('button').html('Procurando...');
		$(this).val()
		disable_controls();
		e.preventDefault();

		$('#list a').remove();
		
		$.post('/', $("form").serialize(), callback_search);
	});

	$('#search-another').click(function(e){
		e.preventDefault();
		$('#input-bus-code').val('');
		$('#search').slideToggle();
	});

	$('#traffic').change(function(){
		var checked = $(this).is(':checked');

		if(checked){
			if(trafficLayer == undefined){
				trafficLayer = new google.maps.TrafficLayer();	
			}
			trafficLayer.setMap(map);
		}else{
			if(trafficLayer !== undefined){
				trafficLayer.setMap(null);
			}
		}
	});
	
	function setAllMap(map) {
		for (var i = 0; i < markers.length; i++) {
			markers[i].setMap(map);
		}
	}

	function clear_markers(){
		
		setAllMap(null);
		markers = [];
	}

	function enable_controls(){
		$('.map').css({'z-index': 1});
		$('.map').css({'opacity': 1});

		map.setOptions({
			disableDefaultUI: false,
			scrollwheel: true,
			draggable: true,
			disableDoubleClickZoom: true
		});
	}

	function disable_controls(){
		$('.map').css({'z-index': -10});
		$('.map').css({'opacity': 0.4});

		map.setOptions({
			disableDefaultUI: true,
			scrollwheel: false,
			draggable: false,
			disableDoubleClickZoom: false
		});
	}

	function callback_search(data){
		$('form button').attr('disabled',false);
		$('form button').html('Buscar');

		clearInterval(interval);

		$.each(data, function(index, value){
			console.log(data);

			var text = 'Destino: '+value.DenominacaoTSTP+' - '+value.Letreiro+'-'+value.Tipo;
			
			if(value.Sentido == 1){
				text = 'Destino: '+value.DenominacaoTPTS+' - '+value.Letreiro+'-'+value.Tipo;
			}

			$('#list').append(function(){
				return $('<a data-id="'+value.CodigoLinha+'" href="#" class="list-group-item">'+text+'</a>').click(
					function(e){
						e.preventDefault();

						update($(this).data('id'));
					}
				);
			});
		});

		
		$('#search').slideUp();
		$('#content').slideDown();
		
	}

	function update(id){
		enable_controls();
		$('#content').slideUp();

		$.post('/realtime', {'id': id}, callback_realtime);

		interval = setInterval(function(){
			$.post('/realtime', {'id': id}, callback_realtime);
			console.log('call');
		},30000)
		
	}

	function callback_realtime(data){
		if(data !== undefined){
			if(data.length == 0){
				return false;
			}
		}else{
			return false;
		}
		clear_markers();

		$.each(data.vs, function(index, bus){

			console.log(bus);
			var location = new google.maps.LatLng(bus.py,bus.px);
			var marker = new google.maps.Marker({
				position: location,
				map: map,
				title:"Ônibus código: "+bus.p
			});
			markers.push(marker);
		});
		console.log(markers);
		setAllMap(map);
		
		
	}


	//Done when finished to load the page
	initialize();
	$('#content').hide();

})

function initialize() {
	var mapOptions = {
		zoom: 12,
		center: new google.maps.LatLng(-23.587898,-46.6442227),
	    disableDefaultUI: true,
	    scrollwheel: false,
	    draggable: false,
	    disableDoubleClickZoom: true
	};

	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);

	
}