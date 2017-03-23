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
		FB.login(function(response) {
			ZB.registerOrLogin(response.authResponse.accessToken);
		}, {
			scope : 'email',
		});
	} else {
		// The person is not logged into Facebook,
		// so we're not sure if they are logged into this app or not.
		FB.login(function(response) {
			ZB.registerOrLogin(response.authResponse.accessToken);
		}, {
			scope : 'email',
		});
	}
}

ZB.updateLoginInfo = function(userinfo) {
	var profile = $('#head_container .profile');
	var a = $(document.createElement('a'));
	var a_s = $(document.createElement('span')).text(userinfo.last_name + ' ' + userinfo.first_name);
	a.append(a_s);
	$.each($('.profile-image.vhmiddle-update'), function (i,v) {
		$(this).data('vhmiddle').updateImage(userinfo.profile_image);
	});
	profile.empty().append(a);

	var url = window.location.href;
	var article_view_regex = new RegExp('^(http[s]?:\\/\\/)' + window.location.host + '\\/article\\/([0-9]+)\\/$');

	// if current page if article view page, check whether the user is participating this article or not.
	if (article_view_regex.test(url)){
		var a_id = article_view_regex.exec(url)[2];
		$.ajax({
			'url' : '/account/check_participate/' + a_id + '/',
			'dataType' : 'json',
			'method' : 'GET',
			'success' :  function(response){
				if (response.check) {
					$('li#participate').attr('data-action', 'unparticipate');
					$('li#participate span').text('취소');
				}
			},
		});
	}
}

ZB.isLogin = function() {
	return $('div#profile_container').find('#login_button').length == 0;
};

ZB.registerOrLogin = function(accessToken) {
	$.ajax({
		'method' : 'GET',
		'dataType' : 'json',
		'url' : '/social/auth/facebook/?access_token=' + accessToken,
		'success' : function(response) {
			$.modal.close();
			ZB.updateLoginInfo(response);
			// TODO
			// also need to update q and a part
		},
		'error' : function(jqXHR, textStatus, errorThrown) {
			$('#facebook_error').text('이메일 주소를 가져오지 못했습니다.');
			$('#facebook_error').animate( { 'background-color' : "#f15050" }, 1 )
				.animate( { 'background-color' : "transparent" }, 1000 );
		},
	});
}

ZB.register = function () {

	var register = {
		init: function () {
			$.get("/account/registration_form/", function(data){
				// create a modal dialog with the data
				$(data).modal({
					overlayCss : { 'background' : '#000' },
					overlayId : 'modal-overlay',
					overlayClose : true,
					position : ['25%',],
					onOpen: register.open,
					//onShow: register.show,
					onClose: register.close
				});
			});
		},

		open : function (dialog) {
			dialog.overlay.fadeIn(200);
			dialog.container.fadeIn(200, function () {
				dialog.data.fadeIn(200);

				var register_button = dialog.data.find('#register_button_container button');
				var email = dialog.data.find('input#register_email');
				var password = dialog.data.find('input#register_password');
				var password_check = dialog.data.find('input#register_password_check');
				var firstname = dialog.data.find('input#register_firstname');
				var lastname = dialog.data.find('input#register_lastname');
				var csrf = dialog.data.find('input[name=csrfmiddlewaretoken]');

				var password_fail = $('#register_password_error');
				var error = dialog.data.find('span#register_error');

				email.focus();

				email.focusout(function(e){
					// check email duplication
					email.val(email.val().trim());
					$.ajax({
						'method' : 'GET',
						'url' : '/account/email_check/',
						'data' : {'email' : email.val()},
						'dataType' : 'json',
						'success' : function(data, textStatus, jqXHR){
							error.text('사용 가능한 이메일 주소입니다.');
						},
						'error' : function(jqXHR, textStatus, errorThrown) {
							if (jqXHR.status == 400) {
								error.text('잘못된 이메일 주소입니다.');
							} else if (jqXHR.status == 409) {
								error.text('이미 등록된 이메일 주소입니다.');
							}
						},
					});
				});

				$.each([password, password_check], function(i, element) {
					$(element).on('input', function () {
						var p = password.val();
						var pc = password_check.val();
						if (p == '' && pc == '') {
							password_fail.text('');
						} else if (p != '' && pc != '' && pc == p) {
							password_fail.text('일치');
						} else {
							password_fail.text('불일치');
						}
					});
				});

				$.each([password, password_check], function(i, e) {
				});

				register_button.click(function(e){
					e.preventDefault();
					$.ajax({
						'method' : 'POST',
						'dataType' : 'json',
						'url' : '/account/register/',
						'data' : {
							'email' : email.val(),
							'csrfmiddlewaretoken' : csrf.val(),
							'password1' : password.val(),
							'password2' : password_check.val(),
							'firstname' : firstname.val(),
							'lastname' : lastname.val(),
						},
						'success' : function(response) {
							$.modal.close();
							email.val('');
							password.val('');
							password_check.val('');
							firstname.val('');
							lastname.val('');
							$.notify("인증메일이 보내졌습니다. 메일을 통해 활성화 하시기 바랍니다.", "success");
						},
						'error' : function(jqXHR) {
							var msg = jqXHR.responseJSON;
							dialog.data.find('span#register_error').text(msg.error);
						},
					});
				});
			});
		},
		close: function (dialog) {
			dialog.overlay.fadeOut(200, function () {
				$.modal.close();
			});
			dialog.data.fadeOut(200, function () {
				dialog.container.fadeOut(200);
			});
		},
	};
	register.init();
};

ZB.login = function (postFunc){

	var login = {
		'postFunc' : postFunc,
		init : function() {
			$.get("/account/login_form/", function(data){
				// create a modal dialog with the data
				$(data).modal({
					overlayCss : { 'background' : '#000' },
					overlayId : 'modal-overlay',
					overlayClose : true,
					position : ['25%',],
					onOpen: login.open,
					onShow: login.show,
					onClose: login.close
				});
			});
		},

		show : function(dialog) {
			dialog.data.find("#register_link").click(function(e){
				e.preventDefault();
				dialog.closeForRegister = true;
				$.modal.close();

			});
		},

		open : function (dialog) {
			dialog.overlay.fadeIn(200);
			dialog.container.fadeIn(200, function () {
				dialog.data.fadeIn(200);
				dialog.data.find('input#login_email').focus();
				dialog.data.find('#facebook_login').click(function(e){
					e.preventDefault();
					FB.getLoginStatus(function(response) {
						ZB.statusChangeCallback(response);
					});
				});


				var login_button = dialog.data.find('#login_button button');
				var email = dialog.data.find('input#login_email');
				var password = dialog.data.find('input#login_password');
				var csrf = dialog.data.find('input[name=csrfmiddlewaretoken]');
				$.each([password, email], function(i, v) {
					v.on('keypress', function (e) {
						if (e.which == 13) {
							login_button.click();
						}
					});
				});

				login_button.click(function(e){
					e.preventDefault();
					$.ajax({
						'method' : 'POST',
						'dataType' : 'json',
						'url' : '/login/',
						'data' : {
							'email' : email.val(),
							'password' : password.val(),
							'csrfmiddlewaretoken' : csrf.val(),
						},
						'success' : function(response) {
							dialog.doPostFunc = true;
							$.modal.close();
							email.val('');
							password.val('');
							ZB.updateLoginInfo(response);
						},
						'error' : function(jqXHR) {
							dialog.data.find('span#login_error').text('아이디 혹은 비밀번호가 틀렸습니다.');
							$(dialog.data.find('span#login_error'))
								.animate( { 'background-color' : "#f15050" }, 1 )
								.animate( { 'background-color' : "transparent" }, 1000 );
							email.focus();
							password.val('');
						},
					});
				});
			});
		},
		close: function (dialog) {
			if (dialog.closeForRegister) {
				dialog.closeForRegister = false;
				dialog.overlay.fadeOut(200, function () {
					$.modal.close();
					ZB.register();
				});
			} else if (dialog.doPostFunc) {
				dialog.diPostFunc = false;
				dialog.overlay.fadeOut(200, function () {
					$.modal.close();
					login.postFunc();
				});
			} else {
				dialog.overlay.fadeOut(200, function () {
					$.modal.close();
				});
			}
			dialog.data.fadeOut(200, function () {
				dialog.container.fadeOut(200);
			});
		},
	};
	login.init();
};

ZB.showAccountDialog = function(){
	var profileDiv = $('#profile_container');

	var dialog = profileDiv.find('#account_dialog');
	if (dialog.length > 0) {
		dialog.fadeIn();
		return;
	}

	dialog = $(document.createElement('div')).attr('id', 'account_dialog');

	var logoutDiv = $(document.createElement('div'));
	var editProfileDiv = $(document.createElement('div'));
	var logout = $(document.createElement('button')).text('로그아웃');
	var editProfile = $(document.createElement('button')).text('마이페이지');

	logoutDiv.append(logout);
	editProfileDiv.append(editProfile);

	dialog.hide();
	dialog.append(logoutDiv).append(editProfileDiv);
	logout.click(function () {
		$.ajax({
			'method' : 'GET',
			'dataType' : 'json',
			'url' : '/logout/',
			'success' : function() {
				window.location = '/';
			},
			'error' : function () {},
		});
	});
	editProfile.click(function () {
		window.location = '/account/';
	});

	var pPosition = profileDiv.offset();

	var leftMargin = (profileDiv.width() - 140) / 2;
	if (leftMargin < 0 && leftMargin > -70) leftMargin = -70;
	pPosition.top+= 65;
	pPosition.left += leftMargin;
	dialog.css({
		'top' : pPosition.top,
		'left' : pPosition.left,
	});
	profileDiv.append(dialog);
	dialog.fadeIn();
};

ZB.removeAccountDialog = function(){
	var dialog = $('#account_dialog');
	dialog.fadeOut('fast', function () {
		dialog.remove();
	});
};

$(document).ready(function(){

	$('.vhmiddle').vhmiddle();

	(function(d, s, id){
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {return;}
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

	window.fbAsyncInit = function() {
		FB.init({
			appId   : '974575612566516',
			xfbml   : true,
			status  : true,
			cookie  : true,
			version : 'v2.3'
		});
	};
});
