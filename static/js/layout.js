$(document).ready(function(){
	$('a#create_article').click(function(e){
		e.preventDefault();

		$.ajax({
			'type' : 'POST',
			'url' : '/article/create/',
			'dataType' : 'json',
			'success' : function(data, textStatus, jqXHR) {
				if (jqXHR.status == 201) {
					var newLocation = jqXHR.getResponseHeader('Location');
					window.location.replace(newLocation);
					
				} else if (jqXHR.status == 200) {
					// there is a draft!
					// TODO
					var newLocation = jqXHR.getResponseHeader('Location');
					console.log(newLocation);
				}
			},
			'error' : function(req, textStatus, jqXHR) {
			},
		});
	});

	$('div#profile_container').mouseover(function() {
		if (ZB.isLogin()) {
			ZB.showAccountDialog();
		}
	}).mouseleave(function () {
		ZB.removeAccountDialog();
	});
});
