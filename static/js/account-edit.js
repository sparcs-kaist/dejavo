$(document).ready(function () {

	$('#profile_image_input').change(function() {
		var formData = new FormData();

		formData.append('profile_image', this.files[0]);
		formData.append('fields', 'profile_image');

		$.ajax({
			'type' : 'POST',
			'url' : '/account/edit/',
			'data' : formData,
			'dataType' : 'json',
			'contentType' : false,
			'processData' : false,
			'success' : function (data, textStatus, jqXHR) {
				ZB.updateLoginInfo(data);
			},
		});
	});

	var facebook_disconnect = function () {
		$.ajax({
			'type' : 'POST',
			'url' : '/social/disconnect/facebook/',
			'dataType' : 'json',
			'success' : function (data, textStatus, jqXHR) {
				$.notify('계정 연동이 취소되었습니다.', 'success');
				$('#facebook_email_input').val('연동 안됨');
				$('#disconnect_error').text();
				$('button#facebook_disconnect').unbind('click');
				$('button#facebook_disconnect').attr('id', 'facebook_connect').text('계정 연동하기')
					.click( function () {
						facebook_connect();
					});
			},
			'error' : function() {
				$('#disconnect_error').text('비밀번호를 먼저 설정하시기 바랍니다.');
				$('#disconnect_error').animate( { 'background-color' : "#f15050" }, 1 )
					.animate( { 'background-color' : "transparent" }, 1000 );
			},
		});
	};

	$('button#facebook_disconnect').click( function () { facebook_disconnect(); } );

	var facebook_connect = function () {
		FB.getLoginStatus(function(response) {
			if (response.status === 'connected') {
				facebook_connect_req(response.authResponse.accessToken);
			} else if (response.status === 'not_authorized') {
				FB.login(function(response) {
					facebook_connect_req(response.authResponse.accessToken);
				}, {
					scope : 'email',
				});
			} else {
				FB.login(function(response) {
					facebook_connect_req(response.authResponse.accessToken);
				}, {
					scope : 'email',
				});
			}
		});
	};

	var facebook_connect_req = function (accessToken) {
		$.ajax({
			'method' : 'GET',
			'dataType' : 'json',
			'url' : '/social/auth/facebook/?access_token=' + accessToken,
			'success' : function(response) {
				$.notify('계정 연동에 성공하였습니다.', 'success');
				$('#facebook_email_input').val(response.social_url);
				$('button#facebook_connect').unbind('click');
				$('button#facebook_connect').attr('id', 'facebook_disconnect').text('계정 연동 취소하기')
					.click( function () {
						facebook_disconnect();
					});
			},
			'error' : function(jqXHR, textStatus, errorThrown) {
				$('#disconnect_error').text('연동에 실패하였습니다.');
				$('#disconnect_error').animate( { 'background-color' : "#f15050" }, 1 )
					.animate( { 'background-color' : "transparent" }, 1000 );
			},
		});
	};

	$('button#facebook_connect').click(function () { facebook_connect(); });

	$('button#change_password').click(function () {
		var new_password1 = $('input#new_password1');
		var new_password2 = $('input#new_password2');
		$.ajax({
			'type' : 'POST',
			'url' : '/account/edit/',
			'dataType' : 'json',
			'data' : {
				'fields' : 'password',
				'password1' : new_password1.val(),
				'password2' : new_password2.val(),
			},
			'success' : function (data, textStatus, jqXHR) {
				$.notify('비밀번호가 변경되었습니다.', 'success');
				$('#change_password_error').text('');
				new_password1.val('');
				new_password2.val('');
			},
			'error' : function () {
				$('#change_password_error').text('비밀번호가 비어있거나 일치하지 않습니다.');
				$('#change_password_error').animate( { 'background-color' : "#f15050" }, 1 )
					.animate( { 'background-color' : "transparent" }, 1000 );
			},
		});
	});
});
