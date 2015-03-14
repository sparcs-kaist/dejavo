ZB = {};

ZB.statusChangeCallback = function(response) {
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
		ZB.registerOrLogin(response.authResponse.accessToken);
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

ZB.updateLoginInfo = function(userinfo) {
	var profile = $('#head_container .profile');
	var a = $(document.createElement('a'));
	var a_s = $(document.createElement('span')).text(userinfo.last_name + ' ' + userinfo.first_name);
	a.append(a_s);
	$('img.profile-image').attr('src', userinfo.profile_image);
	profile.empty().append(a);
}

ZB.registerOrLogin = function(accessToken) {
	$.ajax({
		'method' : 'GET',
		'dataType' : 'json',
		'url' : '/social/auth/facebook/?access_token=' + accessToken,
		'success' : function(response) {
			console.log(response);
			$.modal.close();
			ZB.updateLoginInfo(response);
			// TODO
			// also need to update q and a part
		},
	});
}

ZB.login = function (){

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
						ZB.registerOrLogin(response.authResponse.accessToken);
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
};

$(document).ready(function(){
	(function(d, s, id){
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {return;}
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

	window.fbAsyncInit = function() {
		FB.init({
			appId   : '274526142597066',
			xfbml   : true,
			status  : true,
			cookie  : true,
			version : 'v2.2'
		});
	};
});
