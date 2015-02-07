$(document).ready(function(){
	var titleInput = $("#article_title input").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function() {
			resetTimer();
		},
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

	var subtitleInput = $("#article_subtitle input").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function() {
			resetTimer();
		},
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
		'trigger' : ['input'],
		'onChanged' : function () {
			resetTimer();
		},
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

	var locationInput = $("#location_container input").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function () {
			resetTimer();
		},
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

	var hostnameInput = $("#host_head_container input").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function () {
			resetTimer();
		},
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

	var hostdescTextarea = $("#host_content textarea").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function () {
			resetTimer();
		},
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

	var noticeTextarea = $("#notice_content textarea").datawrapper({
		'trigger' : ['input'],
		'onChanged' : function () {
			resetTimer();
		},
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
			if (d.isChanged()) {
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

				timer = setInterval(update, 20 * 1000);
			},
			'error' : function(req, textStatus, err) {
				console.log(textStatus);
				timer = setInterval(update, 20 * 1000);
			},
		});
	};

	var timer = setInterval(update, 20 * 1000);
	var shortTimer = function () {
		update();
		clearInterval(timer);
		timer = setInterval(update, 20 * 1000);
	};

	function resetTimer() {
		clearInterval(timer);
		timer = setInterval(shortTimer, 2 * 1000);
	}

});
