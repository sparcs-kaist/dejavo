$(document).ready(function(){

	var createQuestion = function(q) {
		var q_div = $(document.createElement('div')).addClass('question').attr('question-id', q.id);

		var q_profile = $(document.createElement('div')).addClass('question-profile-image-container vhmiddle').
							attr('data-width', '60').attr('data-height', '60');
		var q_p_img = $(document.createElement('img')).attr('src', q.writer.image_url);
		q_profile.append(q_p_img);

		var q_c_container = $(document.createElement('div')).addClass('question-content-container');
		var q_meta = $(document.createElement('div')).addClass('question-meta');
		var p_name = $(document.createElement('span')).addClass('question-profile-name').text(q.writer.last_name + ' ' + q.writer.first_name);
		var created_date = new Date(q.created_date);
		var time = $(document.createElement('span')).addClass('question-time').text(
			(created_date.getMonth() + 1) + '월 ' + created_date.getDate() + '일 ' +
			created_date.getHours() + '시 ' + created_date.getMinutes() + '분');

		var delete_span = $(document.createElement('span')).addClass('question-delete');
		delete_span.click(function(e) {
			var c = confirm('정말로 삭제하시겠습니까?');
			if (c) {
				$.ajax({
						'method' : 'GET',
						'dataType' : 'json',
						'url' : '/article/' + articleID + '/qna/delete/' + q.id,
						'success' : function(data, textStatus, jqXHR) {
							if (q_div.find('.answer').length == 0) {
								q_div.fadeOut(function () { q_div.remove(); });
							} else {
								var span = $(document.createElement('span')).
										addClass('deleted').text('-- deleted --');
								content_div.empty().append(span);
								delete_span.remove();
							}
						},
						'error' : function(jqXHR, textStatus, errorThrown) {
							alert('error');
						},
					});
			}
		});
		q_c_container.append(q_meta.append(p_name).append(time).append(delete_span));

		var content_div = $(document.createElement('div')).addClass('question-content').text(q.content);
		q_c_container.append(content_div);

		var answer_popup = $(document.createElement('div')).addClass('answer-popup');
		answer_popup.click(function () {
			var answer_write = createAnswerPopup(q.id);
			answer_popup.after(answer_write);
			answer_write.find('textarea').focus();
		});
		var answer_popup_img = $(document.createElement('img')).attr('src', '/media/answer.png');
		q_c_container.append(answer_popup.append(answer_popup_img));

		q_div.append(q_profile).append(q_c_container);
		q_profile.vhmiddle();
		return q_div;
	};

	var createAnswer = function(a, q_id) {
		var a_div = $(document.createElement('div')).addClass('answer').attr('answer-id', a.id);
		var a_profile = $(document.createElement('div')).addClass('answer-profile-image-container vhmiddle').
							attr('data-width', '40').attr('data-height', '40');
		var a_p_img = $(document.createElement('img')).attr('src', a.writer.image_url).addClass('answer-profile-image');
		a_profile.append(a_p_img);

		var a_c_container = $(document.createElement('div')).addClass('answer-content-container');
		var a_meta = $(document.createElement('div')).addClass('answer-meta');
		var a_name = $(document.createElement('span')).addClass('answer-profile-name').text(a.writer.last_name + a.writer.first_name);
		var created_date = new Date(a.created_date);
		var time = $(document.createElement('span')).addClass('answer-time').text((created_date.getMonth() + 1) + '월 ' + created_date.getDate() + '일 ' + created_date.getHours() + '시 ' + created_date.getMinutes() + '분');
		var delete_span = $(document.createElement('span')).addClass('answer-delete');
		delete_span.click(function(e){
			var c = confirm('정말로 삭제하시겠습니까?');
			if (c) {
				$.ajax({
					'method' : 'GET',
					'dataType' : 'json',
					'url' : '/article/' + articleID + '/qna/' + q_id + '/delete/' + a.id,
					'success' : function(data, textStatus, jqXHR) {
						var span = $(document.createElement('span')).
								addClass('deleted').text('-- deleted --');
						content_span.empty().append(span);
						delete_span.remove();
					},
					'error' : function(jqXHR, textStatus, errorThrown) {
						alert('error');
					},
				});
			}
		});
		a_c_container.append(a_meta.append(a_name).append(time).append(delete_span));

		var content_span = $(document.createElement('span')).addClass('answer-content').text(a.content);
		a_c_container.append(content_span);

		a_div.append(a_profile).append(a_c_container);
		a_profile.vhmiddle();
		return a_div;
	};

	$('div#article_image').click(function(e){
		var image = $('img#article_image_large_img');
		var article_image_large = $('div#article_image_large');
		image.attr('src', image.attr('data-large-url'));
		image.load(function() {
			var modal = article_image_large.modal({
				overlayCss : {
					'background' : '#000',
				},
				containerCss : {
					'position' : 'absolute',
				},
				opacity: 80,
				maxWidth: $(window).width() - 100,
				overlayId : 'modal-overlay',
				onOpen : function(dialog) {

					dialog.overlay.fadeIn(200);
					dialog.container.fadeIn(200, function () {
						dialog.data.fadeIn(200);
					});
					dialog.container.click(function() {
						$.modal.close();
					});
				},
				onShow : function(dialog) {
					dialog.container.css('height', '');
				},
				onClose : function(dialog) {
					dialog.overlay.fadeOut(200, function () {
						$.modal.close();
					});
					dialog.data.fadeOut(200, function () {
						dialog.container.fadeOut(200);
					});
				},

			});

			$('#modal-overlay').click(function() {
				$.modal.close();
			});
		});

	});

	$('#add_question_button').click(function(e){
		e.preventDefault();
		var button = $(this);
		var question_textbox = $('#question_textbox');
		var question_list = $('#question_list');
		var error_span = $('#add_question_notice');

		$.ajax({
			'method' : 'POST',
			'url' : '/article/' + articleID + '/qna/create/',
			'dataType' : 'json',
			'data' : {
				'content' : question_textbox.val(),
			},
			'beforeSend' : function(jqXHR, settings) {
				button.prop('disabled', true).css('opacity', 0.5);
			},
			'success' : function(data, textStatus, jqXHR) {
				question_textbox.val('');
				var new_q = createQuestion(data).hide();
				question_list.append(new_q);
				new_q.fadeIn('normal');

				$('html,body').animate({
					scrollTop: new_q.offset().top
				}, 'normal');
			},
			'error' : function(jqXHR, textStatus, errorThrown) {
				if (jqXHR.status == 401) {
					ZB.login();
				} else {
					error_span.text('댓글이 정상적으로 작성되지 않았습니다.')
				}
			},
			'complete' : function(jqXHR, textStatus) {
				button.prop('disabled', false).css('opacity', 1);
			},
		});
	});

	var createAnswerPopup = function (q_id) {
		var answer_write = $(document.createElement('div')).addClass('answer-write');
		var answer_profile = $(document.createElement('div')).addClass('answer-profile-image-container vhmiddle').
							attr('data-width', '40').attr('data-height', '40');
		var answer_container = $(document.createElement('div')).addClass('answer-box-container');
		var answer_profile_img = $(document.createElement('img')).attr('src', user_prof_img_src).addClass('answer-profile-image');
		var answer_meta = $(document.createElement('div')).addClass('answer-meta');
		var answer_prof_name = $(document.createElement('span')).addClass('answer-profile-name').text(user_name);
		var answer_textbox = $(document.createElement('div')).addClass('answer-textbox');
		var answer_box = $(document.createElement('textarea')).addClass('answer-box').attr({id:'answer-textbox', placeholder:'댓글을 입력하세요'});
		var answer_button_div = $(document.createElement('div'));
		var answer_button = $(document.createElement('button')).addClass('answer-button stress').attr('id', 'add_answer_button').text('댓글달기');
		var answer_notice = $(document.createElement('span')).attr('id', 'add_answer_notice');

		answer_button.click(function(e){
			$.ajax({
				'method' : 'POST',
				'url' : '/article/' + articleID + '/qna/' + q_id + '/create/',
				'dataType' : 'json',
				'data' : {
					'content' : answer_box.val(),
				},
				'beforeSend' : function(jqXHR, settings) {
					answer_button.prop('disabled', true).css('opacity', 0.5);
				},
				'success' : function(data, textStatus, jqXHR) {
					answer_box.val('');
					var new_a = createAnswer(data, q_id).hide();
					answer_write.parent().append(new_a);
					new_a.fadeIn('normal');
				},
				'error' : function(jqXHR, textStatus, errorThrown) {
					if (jqXHR.status == 401) {
						ZB.login();
					} else {
						answer_notice.text('답변이 정상적으로 작성되지 않았습니다.');
					}
				},
				'complete' : function(jqXHR, textStatus) {
					answer_button.prop('disabled', false).css('opacity', 1);
				},
			});
		});

		answer_profile.append(answer_profile_img);
		answer_meta.append(answer_prof_name);
		answer_textbox.append(answer_box);
		answer_button_div.append(answer_button).append(answer_notice);
		answer_container.append(answer_meta).append(answer_textbox).append(answer_button_div);
		answer_write.append(answer_profile).append(answer_container);
		answer_profile.vhmiddle();
		return answer_write;
	};

	$('.answer-popup-button').click(function(e){
		var button = $(this);
		$('.answer-write').remove();
		var question_id = button.parent().parent().parent().parent().attr('question-id');
		var answer_write = createAnswerPopup(question_id);
		button.parent().parent().after(answer_write);
		answer_write.find('textarea').focus();
	});

	var update_participants_list = function(user, action) {
		var list = $('#participant_list');
		var counter = $('span#participant_count');
		var count = parseInt(counter.text());

		if (action == 'participate'){
			var li = $(document.createElement('li')).attr('user-id', user.id);
			var div = $(document.createElement('div')).addClass('participant-profile-image vhmiddle').
						attr('data-width', '48').attr('data-height', '48');
			var img = $(document.createElement('img')).attr('src', user.profile_image);
			var span = $(document.createElement('span')).addClass('participant-profile-text').
				text(user.last_name + ' ' + user.first_name + ' 님이 참여합니다.');
			div.append(img).vhmiddle();
			li.append(div).append(span);
			li.hide();
			counter.text(count + 1);
			list.prepend(li);
			li.fadeIn('fast');
		} else {
			$.each(list.find('li'), function(i, v) {
				var element = $(v);
				if (element.attr('user-id') == user.id ) {
					element.fadeOut('fast', function() {
						element.remove();
					});
					counter.text(count - 1);
					return;
				}
			});
		}
	};

	$('li#participate').click(function(e){
		button = $(this);
		action = button.attr('data-action');
		span = button.find('div.share span');

		$.ajax({
			'method' : 'GET',
			'url' : '/account/' + action + '/' + articleID + '/',
			'dataType' : 'json',
			'beforeSend' : function(jqXHR, settings) {
				button.prop('disabled', true).css('opacity', 0.5);
			},
			'success' : function(data, textStatus, jqXHR) {
				if (action == 'participate') {
					span.text('취소');
					button.attr('data-action', 'unparticipate');
				} else {
					span.text('참여');
					button.attr('data-action', 'participate');
				}
				update_participants_list(data, action);
			},
			'error' : function(jqXHR, textStatus, errorThrown) {
				if (jqXHR.status == 401) {
					ZB.login(function () {
						$('li#participate').click();
					});
				}
			},
			'complete' : function(jqXHR, textStatus) {
				button.prop('disabled', false).css('opacity', 1);
			},
		});
	});

	$("button#article_edit_button").click(function(e){
		window.location = '/article/' + articleID + '/edit/';
	});

	$("button#article_delete_button").click(function(e){
		var c = confirm('정말로 삭제하시겠습니까?');
		if (c) {
			$.ajax({
				'method' : 'GET',
				'url' : '/article/' + articleID + '/delete/',
				'dataType' : 'json',
				'success' : function(data) {
					window.location = '/';
				},
			});
		}
	});


	$.each($('div.question'), function(i, elem) {
		var q = $(elem);
		var content = q.find('.question-content');
		var id = q.attr('question-id');
		q.find('.question-delete').click(function(e){
			var $this = $(this);
			var c = confirm('정말로 삭제하시겠습니까?');
			if (c) {
				$.ajax({
					'method' : 'GET',
					'dataType' : 'json',
					'url' : '/article/' + articleID + '/qna/delete/' + id,
					'success' : function(data, textStatus, jqXHR) {
						if (q.find('.answer').length == 0) {
							q.fadeOut(function () { q.remove(); });
						} else {
							var span = $(document.createElement('span')).
									addClass('deleted').text('-- deleted --');
							content.empty().append(span);
							$this.remove();
						}
					},
					'error' : function(jqXHR, textStatus, errorThrown) {
						alert('error');
					},
				});
			}
		});
	});

	$.each($('div.answer'), function(i, elem) {
		var a = $(elem);
		var content = a.find('.answer-content');
		var q_id = a.parent().parent().attr('question-id');
		var a_id = a.attr('answer-id');
		a.find('.answer-delete').click(function(e){
			var $this = $(this);
			var c = confirm('정말로 삭제하시겠습니까?');
			if (c) {
				$.ajax({
					'method' : 'GET',
					'dataType' : 'json',
					'url' : '/article/' + articleID + '/qna/' + q_id + '/delete/' + a_id,
					'success' : function(data, textStatus, jqXHR) {
						var span = $(document.createElement('span')).
								addClass('deleted').text('-- deleted --');
						content.empty().append(span);
						$this.remove();
					},
					'error' : function(jqXHR, textStatus, errorThrown) {
						alert('error');
					},
				});
			}
		});
	});
});
