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
					var html = data.html;
					var edit_url = data.location;
					$(html).modal({
						overlayCss : { 'background' : '#000' },
						overlayId : 'modal-overlay',
						overlayClose : true,
						position : ['35%',],
						onOpen : function(dialog) {
							dialog.overlay.fadeIn(200);
							dialog.container.fadeIn(200, function () {
								dialog.data.fadeIn(200);
							});

							var edit_button = dialog.data.find('button#article_edit');
							var create_button = dialog.data.find('button#article_create');

							edit_button.click(function(e){
								window.location.replace(edit_url);
							});
							create_button.click(function(e){
								$.ajax({
									'method' : 'POST',
									'dataType' : 'json',
									'url' : '/article/create/?force=true',
									'success' : function(data, textStatus, jqXHR) {
										var newLocation = jqXHR.getResponseHeader('Location');
										window.location.replace(newLocation);
									},

								});
							});
						},
						onClose : function(dialog) {
							dialog.overlay.fadeOut(200, function () {
								$.modal.close();
							});
							dialog.data.fadeOut(200, function () {
								dialog.container.fadeOut(200);
							});
						},
					});
				}
			},
			'error' : function(req, textStatus, jqXHR) {
				if (req.status == 401) {
					ZB.login(function () {
						$('a#create_article').click();
					});
				}
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
