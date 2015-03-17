$(document).ready(function(){

	var createQuestion = function(q) {
		var q_div = $(document.createElement('div')).addClass('question').attr('question-id', q.id);

		var q_profile = $(document.createElement('div')).addClass('question-profile-image-container');
		var q_p_img = $(document.createElement('img')).attr('src', q.writer.image_url).addClass('question-profile-image');
		q_profile.append(q_p_img);

		var q_c_container = $(document.createElement('div')).addClass('question-content-container');
		var q_meta = $(document.createElement('div')).addClass('question-meta');
		var p_name = $(document.createElement('span')).addClass('question-profile-name').text(q.writer.last_name + ' ' + q.writer.first_name);
		var created_date = new Date(q.created_date);
		var time = $(document.createElement('span')).addClass('question-time').text(
			(created_date.getMonth() + 1) + '월 ' + created_date.getDate() + '일 ' +
			created_date.getHours() + '시 ' + created_date.getMinutes() + '분');
		q_c_container.append(q_meta.append(p_name).append(time));

		var content_div = $(document.createElement('div')).addClass('question-content').text(q.content);
		q_c_container.append(content_div);

		q_div.append(q_profile).append(q_c_container);
		return q_div;
	};

	$('div#article_image').click(function(e){
		var image = $('img#article_image_large_img');
		var imageurl = $(this).find('img').attr('src');
		var article_image_large = $('div#article_image_large');

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
				new_q.show('normal');

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

	var update_participants_list = function(user, action) {
		var list = $('#participant_list');
		var counter = $('span#participant_count');
		var count = parseInt(counter.text());

		if (action == 'participate'){
			var li = $(document.createElement('li')).attr('user-id', user.id);
			var img = $(document.createElement('img')).addClass('participant-profile-image').attr('src', user.profile_image);
			var span = $(document.createElement('span')).addClass('participant-profile-text').
				text(user.last_name + ' ' + user.first_name + ' 님이 참여합니다.');
			li.append(img).append(span);
			li.hide();
			counter.text(count + 1);
			list.prepend(li);
			li.show('fast');
			li.fadeIn('fast');
		} else {
			$.each(list.find('li'), function(i, v) {
				var element = $(v);
				if (element.attr('user-id') == user.id ) {
					element.hide('fast');
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
					ZB.login();
				}
			},
			'complete' : function(jqXHR, textStatus) {
				button.prop('disabled', false).css('opacity', 1);
			},
		});
	});
});
