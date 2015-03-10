$(document).ready(function(){

	$("a#login_button").click(function(e){ e.preventDefault();
		var modal = $('#login_container').modal({
			overlayCss : { 'background' : '#000' },
			overlayId : 'modal-overlay',
			position : ['30%',],
			onOpen : function (dialog) {
				dialog.overlay.fadeIn(200);
				dialog.container.fadeIn(200, function () {
					dialog.data.fadeIn(200);

					dialog.data.find('input#login_username').focus();
					dialog.data.find('#facebook_login').click(function(e){
						e.preventDefault();
						FB.login(function(response) {
							registerOrLogin(response.authResponse.accessToken);
						}, {
							scope : 'email',
						});
					});
				});
			},
			onClose: function (dialog) {
				dialog.overlay.fadeOut(200, function () {
					$.modal.close();
				});
				dialog.data.fadeOut(200, function () {
					dialog.container.fadeOut(200);
				});
			},
		});

		$('#modal-overlay').click(function() {
			modal.close();
		});
	});


	function statusChangeCallback(response) {
		// The response object is returned with a status field that lets the
		// app know the current login status of the person.
		// Full docs on the response object can be found in the documentation
		// for FB.getLoginStatus().
		if (response.status === 'connected') {
			// Logged into your app and Facebook.
			registerOrLogin(response.authResponse.accessToken);
		} else if (response.status === 'not_authorized') {
			// The person is logged into Facebook, but not your app.
			//FB.login(function(response) {
			//	console.log(response);
			//}, { scope : 'email'});
		} else {
			// The person is not logged into Facebook,
			// so we're not sure if they are logged into this app or not.
		}
	}

	function updateLoginInfo(userinfo) {
		var name_div = $('#head_container #name');
		var n = $(document.createElement('a'));
		var n_s = $(document.createElement('span')).text(userinfo.last_name + ' ' + userinfo.first_name);
		n.append(n_s)
		var p = $(document.createElement('img')).
				attr('src', userinfo.profile_image).addClass('menu_right profile_img');
		name_div.empty().append(n).append(p);
	}

	function registerOrLogin(accessToken) {
		$.ajax({
			'method' : 'GET',
			'dataType' : 'json',
			'url' : '/social/auth/facebook/?access_token=' + accessToken,
			'success' : function(response) {
				console.log(response);
				$.modal.close();
				updateLoginInfo(response);
				// TODO
				// also need to update q and a part
			},
		});
	}

	window.fbAsyncInit = function() {
		FB.init({
			appId   : '274526142597066',
			xfbml   : true,
			status  : true,
			cookie  : true,
			version : 'v2.2'
		});

		FB.getLoginStatus(function(response) {
			statusChangeCallback(response);
		});
	};
});
