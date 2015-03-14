$(document).ready(function(){

	$("a#login_button").click(function(e){
		e.preventDefault();
		ZB.login();
	});

	window.fbAsyncInit = function() {
		FB.init({
			appId   : '274526142597066',
			xfbml   : true,
			status  : true,
			cookie  : true,
			version : 'v2.2'
		});

		FB.getLoginStatus(function(response) {
			ZB.statusChangeCallback(response);
		});
	};
});
