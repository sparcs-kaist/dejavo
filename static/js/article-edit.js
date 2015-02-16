$(document).ready(function(){

	var $current_button = $('#category_list li.toggled');
	$('#category_list li').click(function(){
		if($current_button) $current_button.removeClass('toggled');
		($current_button = $(this)).addClass('toggled');
	});

	$('div#article_image_new').hover(function (){
		var $this = $(this);
		var div = $this.find('div.cross-large');
		var span = $this.find('span');
		div.animate({
			backgroundColor: "#f15050",

		}, 500);
		span.animate({
			color : "#f15050",
		}, 500);
	}, function () {
		var $this = $(this);
		var div = $this.find('div.cross-large');
		var span = $this.find('span');
		div.animate({
			backgroundColor: "#f0795b",
		}, 500);
		span.animate({
			color : "#f0795b",
		}, 500);
	});

	var titleEditable = $('input#article_title_input').editable({
		'placeholder' : '제목 입력',
		'font-size' : '49px',
		'line-height' : '49px',
		'font-family' : 'Nanum Barun Gothic',
		'text-position' : {
			'top' : -0.5
		},
		'updateCSS' : function() {
			return {
				'width' : this.element.width() + 40 + 'px',
				'height' : this.element.height() - 12 + 'px',
				'top' :  this.element.position().top - 8 + 'px',
				'left' : this.element.position().left - 32 + 'px',
			};
		},
	}).data('editable');

	var subtitleEditable = $('input#article_subtitle_input').editable({
		'placeholder' : '부제목 입력',
		'font-size' : '21px',
		'line-height' : '21px',
		'font-family' : 'Nanum Barun Gothic',
		'text-position' : {
			'top' : -7
		},
		'updateCSS' : function() {
			return {
				'width' : this.element.width() + 24 + 'px',
				'height' : this.element.height() - 18 + 'px',
				'top' :  this.element.position().top - 3 + 'px',
				'left' : this.element.position().left - 24 + 'px',
			};
		},
	}).data('editable');

	var locationEditable = $('input#location_input').editable({
		'placeholder' : '장소 입력',
		'font-size' : '25px',
		'line-height' : '25px',
		'font-family' : 'Nanum Barun Gothic',
		'text-position' : {
			'top' : 1.5
		},
	}).data('editable');

	var hostnameEditable = $('input#host_name_input').editable({
		'placeholder' : '주체 단체 명',
		'font-size' : '25px',
		'line-height' : '25px',
		'font-family' : 'Nanum Barun Gothic',
		'text-position' : {
			'top' : 1.5
		},
	}).data('editable');

	var hostcontentEditable = $('textarea#host_content_textarea').editable({
		'placeholder' : '주체 단체 설명',
		'line-height' : '68px',
	}).data('editable');

	var noticeEditable = $('textarea#notice_content_textarea').editable({
		'placeholder' : '공지사항 입력',
		'line-height' : '68px',
		'color' : '#beb7b7',
	}).data('editable');

	var editable_list = [titleEditable, subtitleEditable,
		locationEditable, hostnameEditable, hostcontentEditable, noticeEditable];

	$(window).resize(function () {
			$.each(editable_list, function(i, e){
			e.update();
		})
	});

	$.each($('#timeslot_table tr'), function(i, v){
		var $this = $(this);
		var timeslotID = $this.attr('timeslot-id');
		var removeIcon = $(this).find('.timeslot-remove');
		removeIcon.click(function(e) {
			$this.remove();
		});
	});

	$('#timeslot_add_container').click(function(e){
		var ele = $('#timeslot_add_form');
		var $this = $(this);
		var position = $this.position();
		ele.css({
			'top' : position.top + 40,
			'left' : position.left - 300,
		});
		ele.toggle();
		$('#ts_label').empty().focus();
	});

	$('#timeslot_add_button').click(function(e){
		e.preventDefault();
		var data = getNewTimeSlot();
		var stime = data.start_time;

		var tr = $('<tr></tr>').attr('mode', 'new');
		var removeTD = $('<td></td>').addClass('timeslot-remove');
		removeTD.append($('<div></div>').addClass('timeslot-remove-icon'));
		var dateTD = $('<td>' + (stime.getMonth() + 1) + '월 ' +
							stime.getDate() + '일 ' + stime.getHours() + '시 ' +
							stime.getMinutes() + '분</td>')
					.addClass('timeslot-time')
					.attr({
						'time-year' : stime.getFullYear(),
						'time-month' : stime.getMonth() + 1,
						'time-date' : stime.getDate(),
						'time-hour' : stime.getHours(),
						'time-minute' : stime.getMinutes(),
					});
		var labelTD = $('<td></td>');
		labelTD.append('<button class="timeslot-label">' + data.label + '</button>');;

		tr.append(removeTD).append(dateTD).append(labelTD);
		$('#timeslot_table tbody').append(tr);

		removeTD.click(function (e){
			tr.remove();
		});

		$('#timeslot_add_form').toggle();
		$('#timeslot_add_form input').val('');
	});

	$('#owner_add_container').click(function(e) {
		var ele = $('#owner_add_form');
		var $this = $(this);
		var position = $this.position();
		ele.css({
			'top' : position.top + 40,
			'left' : position.left - 125,
		});
		ele.toggle();
		$('#owner_query').empty().focus();
	});

	var getNewTimeSlot = function() {
		// TODO validation
		var newDate = new Date();
		newDate.setFullYear($('#ts_year').val());
		newDate.setMonth($('#ts_month').val() - 1);
		newDate.setDate($('#ts_date').val());
		newDate.setHours($('#ts_hour').val());
		newDate.setMinutes($('#ts_minute').val());

		return {
			'label' : $('#ts_label').val(),
			'start_time' : newDate,
			'type' : 'point',
		};
	};
	var categoryList = $('#category_list').datawrapper({
		'trigger' : ['DOMSubtreeModified'],
		'getData' : function() {
			var toggledValue = this.element.find('li.toggled').attr('data-value');
			return {
				'field' : 'category',
				'value' : toggledValue,
			};
		},
	}).data('datawrapper');

	var timeslotTable = $('#timeslot_table').datawrapper({
		'trigger' : ['DOMSubtreeModified'],
		'getData': function() {
			var data = [];
			$.each(this.element.find('tr'), function(i, _tr){
				var tr = $(_tr);
				var timeslot = { };
				var mode = tr.attr('mode');
				if (mode == 'old'){
					timeslot['id'] = tr.attr('timeslot-id');
				} else {
					var label = tr.find('.timeslot-label').text();
					var timeTD = tr.find('.timeslot-time');
					var time = timeTD.attr('time-year') + '-' + timeTD.attr('time-month') +
							'-' + timeTD.attr('time-date') + 'T' + timeTD.attr('time-hour') +
							':' + timeTD.attr('time-minute') + 'Z';
					timeslot['label'] =  label;
					timeslot['start_time'] = time;
					timeslot['type'] = 'point';
				}
				data.push(timeslot);
			});
			return {
				'field' : 'timeslot',
				'value' : JSON.stringify(data),
			};
		},
	}).data('datawrapper');

	$('#article_image_input').change(function() {
		if (this.files && this.files[0]) {
			var reader = new FileReader();
			reader.onload = function (e) {
				var newImage = $(document.createElement('img')).attr({
					'src' : e.target.result,
				}).hide();
				var toAppend = $('#article_image div.editable-img').css('border', '0');
				toAppend.empty().append(newImage);
				newImage.fadeIn('slow');
			}
			reader.readAsDataURL(this.files[0]);
		}
	});

	$('#host_image_input').change(function() {
		if (this.files && this.files[0]) {
			var reader = new FileReader();
			reader.onload = function (e) {
				var newImage = $('<img></img>').attr({
					'src' : e.target.result,
					'id' : 'host_image',
				}).hide();
				var toPrepend = $('#host_image_container');
				var oldImage = $('img#host_image');
				oldImage.remove();
				toPrepend.prepend(newImage);
				newImage.click(function (e){
					e.preventDefault();
					$('#host_image_input').click();
				});
				newImage.fadeIn('slow');
			}
			reader.readAsDataURL(this.files[0]);
		}
	});

	$('#edit_button').click(function(e){
		e.preventDefault();
		if (!update(false, true)) {
			update(true, true);
		}
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

	var articleImageInput = $('#article_image_input').datawrapper({
		'trigger' : ['change'],
		'getData' : function() {
			var realInput = this.element[0];
			if (realInput.files && realInput.files[0]){
				return {
					'field' : 'image',
					'value' : realInput.files[0],
				};
			} else {
				return null;
			}
		},
	}).data('datawrapper');

	var hostImageInput = $('#host_image_input').datawrapper({
		'trigger' : ['change'],
		'getData' : function() {
			var realInput = this.element[0];
			if (realInput.files && realInput.files[0]){
				return {
					'field' : 'image',
					'value' : realInput.files[0],
				};
			} else {
				return null;
			}
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

	var ownerList = $('#owner_list').datawrapper({
		'trigger' : ['DOMSubtreeModified'],
		'getData' : function() {
			var data = [];
			$.each(this.element.find('.owner-profile'), function(i, v){
				data.push($(v).attr('ownerid'));
			});
			return {
				'field' : 'owner',
				'value' : JSON.stringify(data),
			};
		},
	}).data('datawrapper');

	var checkList = [
				titleInput,
				subtitleInput,
				categoryList,
				timeslotTable,
				articleImageInput,
				articleContent,
				locationInput,
				hostImageInput,
				hostnameInput,
				hostdescTextarea,
				noticeTextarea,
				ownerList,
			];

	var update = function (forced, to_publish) {
		var _forced = forced || false;

		var formData = new FormData();
		var fieldsData = [];

		$.each(checkList, function (i, d) {
			if (_forced || (d && d.isChanged())){
				if (d) {
					var dict = d.getData();
					if (dict) {
						fieldsData.push(dict['field']);
						formData.append(dict['field'], dict['value']);
					}
				}
			}
		});

		if (!_forced && fieldsData.length == 0){
			return false;
		}

		fieldsData.push('is_published');
		formData.append('is_published', to_publish);
		formData.append('fields', fieldsData);

		$.ajax({
			'type' : 'POST',
			'url' : document.URL,
			'data' : formData,
			'dataType' : 'json',
			'contentType' : false,
			'processData' : false,
			'success' : function (data, textStatus, jqXHR) {
				$.each(checkList, function (i, d) {
					if (d) {
						d.reset();
						d.setData(data['article']);
					}
				});
				var dd = new Date(data['article']['updated_date']);
				$("#update_time").text((dd.getMonth() + 1) + '월 ' + dd.getDate() + '일 ' +
					dd.getHours() + '시 ' + dd.getMinutes() + '분 ' + dd.getSeconds() + '초');
			},
			'error' : function(req, textStatus, err) {
				console.log(textStatus);
			},
		});

		return true;
	};

	if (!is_published) {
		setInterval(function () { update(false, false); }, 60 * 1000);
	}
});
