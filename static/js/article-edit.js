$(document).ready(function(){

	var timeslot_add_form = $('div#timeslot_add_form');
	var timeslot_add_div = $('div#timeslot_add_container');
	var owner_add_form = $('div#owner_add_form');
	var owner_add_div = $('div#owner_add_container');

	$(document).click(function(e){
		var f = function(a, b) {
			if (b.is(e.target) || b.has(e.target).length > 0) {
				return;
			}
			if (!a.is(e.target) && a.has(e.target).length == 0) {
				a.hide();
				a.find('input').val('');
			}
		};
		f(timeslot_add_form, timeslot_add_div);
		f(owner_add_form, owner_add_div);
	});

	$.each($('#owner_list li'), function(i, v) {
		var $v = $(v);
		$v.find('span.timeslot-remove-icon').click(function(e){
			e.preventDefault();
			$v.remove();
		});
	});


	$('#owner_query').keyup(function(e){
		if (e.which == 13) {
			$('#owner_search_button').click();
		}
	});

	$('#owner_search_button').click(function(e){
		e.preventDefault();

		var q = $('#owner_query');
		var l = $('#owner_selection_list');
		var ll = $('#owner_list');
		$.ajax({
			'method' : 'GET',
			'url' : '/account/search/',
			'data' : { 'q' : q.val() },
			'dataType' : 'json',
			'error' : function(req, textStatus, err) {
				l.empty()
				var li = $('<li></li>').css('text-align', 'center');
				var div = $('<span></span>').css('line-height', '30px');
				div.text('검색 결과가 없습니다.');
				l.append(li.append(div));
				return;
			},
			'success' : function (data, textStatus, jqXHR) {

				var curr_list = [];
				$.each(ll.find('li'), function(i, profile){
					curr_list.push(parseInt($(profile).attr('ownerid')));
				});
				
				l.empty();

				if (data.result.length == 0) {
					var li = $('<li></li>').css('text-align', 'center');
					var div = $('<span></span>').css('line-height', '30px');
					div.text('검색 결과가 없습니다.');
					l.append(li.append(div));
					return;
				}

				$.each(data.result, function(i, user){
					var li = $('<li></li>');
					var user_image = $('<img></img>').addClass('owner-small-profile-image')
						.attr('src', user.profile_image);
					var user_name = $('<div></div>').addClass('owner-small-profile-name')
						.text(user.last_name + ' ' + user.first_name);

					li.append(user_image).append(user_name);
					l.append(li);

					// check if owner is included.
					if ($.inArray(user.id, curr_list) != -1){
						li.css('background-color', '#eeeeee');
						return;
					}

					li.click(function(e){
						var owner_li = $('<li></li>').attr('ownerid', user.id);
						var remove_icon = $('<span></span>').addClass('timeslot-remove-icon');
						var profile_img_div = $('<div></div>').addClass('owner-profile-image vhmiddle').
								attr('data-width', '48').attr('data-height', '48');
						var profile_img = $('<img></img>').attr('src', user.profile_image);
						var profile_text = $('<span></span>').addClass('owner-profile-text')
											.text(user.last_name + user.first_name + ' 님이 관리합니다.');

						remove_icon.click(function(e){
							e.preventDefault();
							owner_li.remove();
						});
						profile_img_div.append(profile_img).vhmiddle();
						owner_li.append(remove_icon).append(profile_img_div).append(profile_text);
						ll.append(owner_li);

						$('#owner_add_form').hide();
						q.val('');
					});
				});
			},
		});
	});

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

	$('#insert_video').click(function(e){
		var ele = $('#insert_video_form');
		var $this = $(this);
		var position = $this.position();
		ele.css({
			'top' : position.top - 50,
			'left' : position.left - 180,
		});
		ele.toggle();
		$('#video_url_input').val('').focus();
	});

	$('#video_url_input').keyup(function(e){
		if (e.which == 13) {
			$('#video_add_button').click();
		}
	});

	$('#video_add_button').click(function(e){
		var input = $('#video_url_input');
		$('#editor_youtube_input').val(input.val()).change();
		$('#insert_video_form').toggle();
		input.val('');
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
			'left' : position.left - 380,
		});
		ele.toggle();
		var currDate = new Date();
		ele.find('#ts_year').val(currDate.getFullYear());
                ele.find('#te_year').val(currDate.getFullYear());
		$('#ts_label').empty().focus();
	});

	$('#timeslot_add_form').keyup(function(e){
		if (e.which == 13) {
			$('#timeslot_add_button').click();
		}
	});

	var updateTable = function () {
		var table = $('#timeslot_table tbody');
		var tr_list = table.find('tr');
		if (tr_list.length > 0) {
			table.find('span.timeslot-main-span').remove();
			var span = $(document.createElement('span')).addClass('timeslot-main-span');
			$(tr_list[0]).find('div.squaredTwo').prepend(span.text('대표 일정'));
		}
	};

    $('.timeslot_add_checkbox').click(function() {
        var type = $(this).attr('data');

        if($(this).children('input').prop('checked')) {
            $(this).children('input').removeProp('checked');
            if(type == 'period') {
                $("#timeslot_add_end").css('display', 'none');
            } else if(type == 'time') {
                $(".timeslot_add_minutesecond").css('display', 'none');
            } else if(type == 'represent') {
            }
        } else {
            $(this).children('input').prop('checked', true);
            if(type == 'period') {
                $("#timeslot_add_end").css('display', 'block');
            } else if(type == 'time') {
                $(".timeslot_add_minutesecond").css('display', 'inline-block');
            } else if(type == 'represent') {
            }
        }
    });

    $('.timeslot_add_ampm').click(function() {
        var type = $(this).attr('data');

        if(type == 'am') {
            if($(this).children('input').prop('checked')) {
            } else {
                $(this).children('input').prop('checked', true);
                $(this).next().children('input').removeProp('checked');
            }
        } else {
            if($(this).children('input').prop('checked')) {
            } else {
                $(this).children('input').prop('checked', true);
                $(this).prev().children('input').removeProp('checked');
            }
        }
    });

    // editedit
	$('#timeslot_add_button').click(function(e){
		e.preventDefault();
		var data = getNewTimeSlot();
		if (!data) return;
		var stime = data.start_time;
                var etime = data.end_time;

		var tr = $('<tr></tr>').attr('mode', 'new');
		var removeTD = $('<td></td>').addClass('timeslot-remove');
		removeTD.append($('<div></div>').addClass('timeslot-remove-icon'));

                var tmpStr = (stime.getMonth() + 1) + '월 ' + stime.getDate() + '일 ';
                if($("#timeslot_add_start").children('div').children('div:first').children('input').prop('checked')) tmpStr = tmpStr + '오전 ';
                else tmpStr = tmpStr + '오후 ';
                if(stime.getDate() == 0) ele.find('#ts_date').val(currDate.getDate());
                if(stime.getHours() != 0 || stime.getMinutes() != 0) tmpStr = tmpStr + stime.getHours() + '시 '; 
                if(stime.getMinutes() != 0) tmpStr = tmpStr + (stime.getMinutes()<10?'0':'') + stime.getMinutes() + '분';
		var dateTD = $('<td>' + tmpStr + '</td>')
					.addClass('timeslot-time')
                                        .css('padding-right', '5px')
					.attr({
						'time-year' : stime.getFullYear(),
						'time-month' : stime.getMonth() + 1,
						'time-date' : stime.getDate(),
						'time-hour' : stime.getHours(),
						'time-minute' : stime.getMinutes(),
					});

                var tmpStr2 = (etime.getMonth() + 1) + '월 ' + etime.getDate() + '일 ';
                if($("#timeslot_add_start").children('div').children('div:last').children('input').prop('checked')) tmpStr2 = tmpStr2 + '오전 ';
                else tmpStr2 = tmpStr2 + '오후 ';
                if(etime.getHours() != 0 || etime.getMinutes() != 0) tmpStr2 = tmpStr2 + etime.getHours() + '시 '; 
                if(etime.getMinutes() != 0) tmpStr2 = tmpStr2 + (etime.getMinutes()<10?'0':'') + etime.getMinutes() + '분';
                var dateTD2 = $('<td>' + '~' + tmpStr2 + '</td>')
                    .addClass('timeslot-time')
                    .attr({
                        'time-year' : etime.getFullYear(),
                        'time-month' : etime.getMonth() + 1,
                        'time-date' : etime.getDate(),
                        'time-hour' : etime.getHours(),
                        'time-minute' : etime.getMinutes(),
                    });

		var labelTD = $('<td></td>');
		if (data.label.trim() == '') {
			labelTD.append('<span class="timeslot-label"></span>');
		} else {
                if ($(this).prev().children('input').prop('checked')) {
                    var button = $('<button class="timeslot-label is-main"></button>');
                } else {
                    var button = $('<button class="timeslot-label"></button>');
                }
			button.text(data.label);
			labelTD.append(button);
		}

		var ranID = Math.random().toString(36).substring(7);
		var isMainTD = $('<td></td>').addClass('timeslot-is-main');
		var mainDiv = $(document.createElement('div')).addClass('squaredTwo');
                if ($(this).prev().children('input').prop('checked')) {
                    var mainInput = $(document.createElement('input')).attr('type', 'checkbox').attr('id', ranID).prop('checked', true);
                } else {
                    var mainInput = $(document.createElement('input')).attr('type', 'checkbox').attr('id', ranID);
                }
		var mainLabel = $(document.createElement('label')).attr('for', ranID);
		isMainTD.append(mainDiv.append(mainInput).append(mainLabel));

		mainInput.click(function() {
			if ($(this).prop('checked')) {
				labelTD.find('.timeslot-label').addClass('is-main');
			} else {
				labelTD.find('.timeslot-label').removeClass('is-main');
			}
		});

		var table = $('#timeslot_table tbody');
                // 기간으로 표시가 checked일 경우
                if ($(this).parent().children('div:first').children('input').prop('checked')) {
                } else {
                    dateTD2.css('visibility', 'hidden');
                }
                tr.append(removeTD).append(dateTD).append(dateTD2).append(labelTD).append(isMainTD);
		table.append(tr);
		updateTable();

		removeTD.click(function (e){
			tr.remove();
			$.each(editable_list, function(i, editable) {
				editable.update();
			});
			updateTable();
		});

		$.each(editable_list, function(i, editable) {
			editable.update();
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
		$('#owner_selection_list').empty();
		ele.toggle();
		$('#owner_query').val('').focus();
	});

    // editedit
	var getNewTimeSlot = function() {
		// TODO validation
		var newDate = new Date(
				$('#ts_year').val(),
				$('#ts_month').val() - 1,
				$('#ts_date').val(),
				$('#ts_hour').val(),
				$('#ts_minute').val());
		var newDateEnd = new Date(
				$('#te_year').val(),
				$('#te_month').val() - 1,
				$('#te_date').val(),
				$('#te_hour').val(),
				$('#te_minute').val());

		if (isNaN(newDate)) {
			$('#error_msg').html('일시 형식이 잘못되었습니다.');
			$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
				.animate( { backgroundColor: "#ffffff" }, 1000 );
			return false;
		} else {
			var maxDate = new Date();
			maxDate.setDate(maxDate.getDate() + 400);
			if (newDate > maxDate) {
				$('#error_msg').html('작성된 일시가 너무 멉니다.');
				$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
					.animate( { backgroundColor: "#ffffff" }, 1000 );
				return false;
			}
		}
 
		if (isNaN(newDateEnd)) {
			$('#error_msg').html('일시 형식이 잘못되었습니다.');
			$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
				.animate( { backgroundColor: "#ffffff" }, 1000 );
			return false;
		} else {
			var maxDateEnd = new Date();
			maxDateEnd.setDate(maxDateEnd.getDate() + 400);
			if (newDateEnd > maxDateEnd) {
				$('#error_msg').html('작성된 일시가 너무 멉니다.');
				$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
					.animate( { backgroundColor: "#ffffff" }, 1000 );
				return false;
			}
		}

		return {
			'label' : $('#ts_label').val(),
			'start_time' : newDate,
            'end_time' : newDateEnd,
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

    // editedit
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
					var timeTD = tr.find('.timeslot-time:first');
					var date = new Date(timeTD.attr('time-year'),
						timeTD.attr('time-month') - 1,
						timeTD.attr('time-date'),
						timeTD.attr('time-hour'),
						timeTD.attr('time-minute'))

					var timeTD2 = tr.find('.timeslot-time:last');
					var dateEnd = new Date(timeTD2.attr('time-year'),
						timeTD2.attr('time-month') - 1,
						timeTD2.attr('time-date'),
						timeTD2.attr('time-hour'),
						timeTD2.attr('time-minute'))

					timeslot['label'] =  label;
					timeslot['start_time'] = date.toISOString();
                                        timeslot['end_time'] = dateEnd.toISOString();
					timeslot['type'] = 'point';
					timeslot['is_main'] = is_main;

                                        if(timeTD2.css('visibility') == 'hidden') timeslot['exist_end'] = false;
                                        else timeslot['exist_end'] = true;
                                        if(tr.find('.timeslot-time:first:contains("오전")')) timeslot['is_am_start'] = true;
                                        else timeslot['is_am_start'] = false;
                                        if(tr.find('.timeslot-time:last:contains("오전")')) timeslot['is_am_end'] = true;
                                        else timeslot['is_am_end'] = false;
				}
				var is_main = tr.find('.timeslot-is-main input[type=checkbox]').prop('checked');
				timeslot['is_main'] = is_main;
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
		var host_image = $('#host_image_container');
		if (this.files && this.files[0]) {
			var reader = new FileReader();
			reader.onload = function (e) {
				host_image.data('vhmiddle').updateImage(e.target.result);
			}
			reader.readAsDataURL(this.files[0]);
		}
	});

	$('#cancel_button').click(function(e){
		// TODO canel if published, remove if not

		if (is_published) {
			var c = confirm('정말로 취소하시겠습니까?');
			if (c) {
				window.location = '/article/' + articleID + '/';
			}
		} else {
			var c = confirm('정말로 삭제하시겠습니까?');
			if (c) {
				$.ajax({
					'method' : 'GET',
					'url' : '/article/' + articleID + '/delete/',
					'dataType' : 'json',
					'success' : function(data) {
						window.location = '/';
					},
					'error' : function(jqXHR) {
						$('#error_msg').text(jqXHR.responseJSON.error);
					},
				});
			}
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
					'field' : 'host_image',
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
			//this.element.html(data.content);
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
			$.each(this.element.find('li'), function(i, v){
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

		var button = $('button#edit_button');

		$.ajax({
			'type' : 'POST',
			'url' : document.URL,
			'data' : formData,
			'dataType' : 'json',
			'contentType' : false,
			'processData' : false,
			'beforeSend' : function(jqXHR, settings) {
				button.prop('disabled', true).css('opacity', 0.5);
			},
			'success' : function (data, textStatus, jqXHR) {
				$.each(checkList, function (i, d) {
					if (d) {
						d.reset();
						d.setData(data['article']);
					}
				});
				var dd = new Date(data['article']['updated_date']);
				$("#update_time").text((dd.getMonth() + 1) + '월 ' + dd.getDate() + '일 ' +
					dd.getHours() + '시 ' +
					((dd.getMinutes()<10?'0':'') + dd.getMinutes()) + '분 ' +
					((dd.getSeconds()<10?'0':'') + dd.getSeconds()) + '초 ');

				$('#error_msg').html('');
				$('#error_msg').removeAttr('style');

				if (to_publish) {
					window.location.replace(jqXHR.getResponseHeader('Location'));
				}
			},
			'error' : function(req, textStatus, err) {
				var res = req.responseJSON;
				var fields = [];
				var timeslot_count = false;
				var owner_err = false;
				if (res === undefined) {
					$('#error_msg').css({
						'padding' : '10px 5px',
						'margin-bottom' : '20px',
					});
					$('#error_msg').html('업데이트에 실패하였습니다.');
					$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
						.animate( { backgroundColor: "#ffffff" }, 1000 );
					return;
				}
				res.msg && res.msg && $.each(res.msg, function(key, val) {
					if (key == 'category'){
						fields.push('카테고리');
					} else if (key == 'host_image') {
						fields.push('주체 단체 이미지');
					} else if (key == 'host_name') {
						fields.push('주체 단체 명');
					} else if (key == 'image') {
						fields.push('메인포스터');
					} else if (key == 'title') {
						fields.push('제목');
					} else if (key == 'timeslot') {
						fields.push('일시');

					} else if (key == 'timeslot_count') {
						timeslot_count = true;
					} else if (key == 'owner') {
						owner_err = true;
					}
				});

				var msg = [];
				if (fields.length > 0) {
					msg.push('<b>' + fields.join(', ') +
							'</b>를(을) 바르게 입력하거나 선택해 주시기 바랍니다.');
				}
				if (timeslot_count){
					msg.push('최소 하나의 <b>일정</b>이 있어야합니다.');
				}
				if (owner_err){
					msg.push('최소 한 명의 <b>관리자</b>가 있어야합니다.');
				}
				$('#error_msg').css({
					'padding' : '10px 5px',
					'margin-bottom' : '20px',
				});
				$('#error_msg').html(msg.join('<br><br>'));
				$('#error_msg').animate( { backgroundColor: "#f15050" }, 1 )
					.animate( { backgroundColor: "#ffffff" }, 1000 );

			},
			'complete' : function(jqXHR, textStatus) {
				button.prop('disabled', false).css('opacity', 1);
			},
		});

		return true;
	};

	if (!is_published) {
		setInterval(function () { update(false, false); }, 60 * 1000);
	}
});
