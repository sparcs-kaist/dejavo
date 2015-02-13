(function ($) {

	var Editable = (function (element, options) {

		function Editable(element, options) {
			var $this = this;
			this.element = $(element);
			this.updateCSS = options.updateCSS;
			this.div = $(document.createElement('div')).css(options.div_css).css({
				'font-family' : options['font-family'],
				'font-size' : options['font-size'],
				'color' : options.color,
				'line-height' : options['line-height'],
				'text-align' : options['text-align'],
			});
			this.span = $(document.createElement('span')).css({
				'position' : 'relative',
			});
			this.span.offset(options['text-position']);
			this.div.append(this.span);

			this.element.keyup(function (e) {
				$this.update();
			});

			this.element.mouseenter(function (e) {
				$this.element.css('background-color', 'transparent');
				$this.update();
				$this.element.parent().append($this.div);
			});
			this.element.focus(function (e) {
				$this.span.text('');
			});
			this.element.focusout(function (e) {
				if($this.element.val().trim() == ''){
					$this.span.text(options.placeholder);
					$this.update();
					$this.element.parent().append($this.div);
				} else {
					$this.div.remove();
				}
			});
			this.element.mouseleave(function (e) {
				if($this.element.val().trim() == ''){
					return;
				}

				if($this.element.is(':focus')){
					return;
				}
				$this.element.css('background-color', 'inherit');
				$this.div.remove();
			});

			Editable.prototype.update = function () {
				this.div.css(this.updateCSS());
			}
		};

		return Editable;
	})();

	$.fn.editable = function(userOptions) {

		return this.each(function () {
			var $this = $(this);
			if (!$this.data('editable')) {
				userOptions = $.extend({}, $.fn.editable.defaults, userOptions);
				$this.data('editable', new Editable(this, userOptions));
			}
		});
	};

	$.fn.editable.defaults = {
		'div_css' : {
			'position' : 'absolute',
			'z-index' : -1,
			'border' : '12px solid transparent',
			'border-image' : 'url(/static/css/images/dot_square.png) 12 12 round',
			'background-color' : 'transparent',
			'border-image-width' : '12px',
		},
		'updateCSS' : function () {
			return {
				'width' : this.element.width() - 12 + 'px',
				'height' : this.element.height() - 12 + 'px',
				'top' :  this.element.position().top - 6 + 'px',
				'left' : this.element.position().left - 6 + 'px',
			};
		},
		'text-align' : 'center',
		'placeholder' : '내용을 입력하세요',
		'font-family' : 'Nanum Gothic',
		'font-size' : '15px',
		'line-height' : '15px',
		'color' : '#f0795b',
		'text-position' : {},
	};

}(window.jQuery));
