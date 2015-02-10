$(document).ready(function(){

	$('#article_image input').fileupload({
		'url' : document.URL,
		'dataType' : 'json',
		'done' : function(e, data) {
			var newImage = $('<img></img>').attr({
				'src' : data.result.article.poster,
			}).hide();
			var toAppend = $('#article_image div.editable-img');
			toAppend.empty().append(newImage);
			newImage.fadeIn('slow');
		},
		//'progressall' : function(e, data) {
		//	var progress = parseInt(data.loaded / data.total * 100, 10);
		//	$('#image-progress').text(progress + '%');
		//},
	 	'formData' : {'fields[]' : 'image'}
	});	

	$('#host_image_input').fileupload({
		'url' : document.URL,
		'dataType' : 'json',
		'done' : function(e, data) {
			var newImage = $('<img></img>').attr({
				'src' : data.result.article.host.image,
				'id' : 'host_image',
			}).hide();
			var toPrepend = $('#host_head_container');
			var oldImage = $('img#host_image');
			oldImage.remove();
			toPrepend.prepend(newImage);
			newImage.fadeIn('slow');
		},
		//'progressall' : function(e, data) {
		//	var progress = parseInt(data.loaded / data.total * 100, 10);
		//	$('#image-progress').text(progress + '%');
		//},
	 	'formData' : {'fields[]' : 'host_image'}
	});	

	var titleInput = $("#article_title_input").datawrapper({
		'getData' : function() {
			return {
				'field' : 'title',
				'value' : this.element.val().trim(),
			};
		},
		'setData' : function(data) {
			this.element.val(data['title']);
		},
	}).data('datawrapper');

	var subtitleInput = $("#article_subtitle_input").datawrapper({
		'getData' : function() {
			return {
				'field' : 'subtitle',
				'value' : this.element.val().trim(),
			};
		},
		'setData' : function(data) {
			this.element.val(data['subtitle']);
		},
	}).data('datawrapper');

	var articleContent = $("#article_content").datawrapper({
		'getData' : function () {
			return {
				'field' : 'content',
				'value' : this.element.cleanHtml(),
			};
		},
		'setData' : function (data) {
			this.element.html(data.content);
		},
	}).data('datawrapper');

	var locationInput = $("#location_input").datawrapper({
		'getData' : function() {
			return {
				'field' : 'location',
				'value' : this.element.val(),
			}
		},
		'setData' : function(data) {
			this.element.val(data['location']);
		},
	}).data('datawrapper');

	var hostnameInput = $("#host_name_input").datawrapper({
		'getData' : function() {
			return {
				'field' : 'host_name',
				'value' : this.element.val(),
			};
		},
		'setData' : function(data) {
			this.element.val(data['host']['name']);
		},
	}).data('datawrapper');

	var hostdescTextarea = $("#host_content_textarea").datawrapper({
		'getData' : function() {
			return {
				'field' : 'host_description',
				'value' : this.element.val(),
			};
		},
		'setData' : function(data) {
			this.element.val(data['host']['description']);
		},
	}).data('datawrapper');

	var noticeTextarea = $("#notice_content_textarea").datawrapper({
		'getData' : function() {
			return {
				'field' : 'announcement',
				'value' : this.element.val().trim(),
			};
		},
		'setData' : function(data) {
			this.element.val(data['announcement']);
		},
	}).data('datawrapper');

	var checkList = [
				titleInput,
				subtitleInput,
				articleContent,
				locationInput,
				hostnameInput,
				hostdescTextarea,
				noticeTextarea
			];

	var update = function () {
		var postData = {'fields' : []};
		var flag = false;
		$.each(checkList, function (i, d) {
			if (d.isChanged()){
				flag = true;
				var dict = d.getData();
				postData[dict['field']] = dict['value'];
				postData['fields'].push(dict['field']);
			}
		});

		if (!flag) {
			return;
		}

		console.log(postData);
		clearInterval(timer);

		$.ajax({
			'type' : 'POST',
			'url' : document.URL,
			'data' : postData,
			'dataType' : 'json',
			'success' : function (data, textStatus, jqXHR) {
				$.each(checkList, function (i, d) {
					d.reset();
					d.setData(data['article']);
				});
				var dd = new Date(data['article']['updated_date']);
				$("#update_news").text(dd.getMonth() + '월 ' + dd.getDate() + '일 ' + 
					dd.getHours() + '시 ' + dd.getMinutes() + '분 ' + dd.getSeconds() + '초');
			},
			'error' : function(req, textStatus, err) {
				console.log(textStatus);
			},
		});
	};
});
