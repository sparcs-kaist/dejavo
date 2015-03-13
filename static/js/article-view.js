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
				error_span.text('댓글이 정상적으로 작성되지 않았습니다.')
			},
			'complete' : function(jqXHR, textStatus) {
				button.prop('disabled', false).css('opacity', 1);
			},
		});
	});
});
