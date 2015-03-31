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
});
