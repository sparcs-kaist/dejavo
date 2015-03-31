(function ($) {

	var VHMiddle = (function (element, options) {

		function VHMiddle(element, options) {

			var $this = this;
			this.element = $(element);
			this.showWidth = this.element.attr('data-width');
			this.showHeight = this.element.attr('data-height');
			this.image = this.element.find('img');

			VHMiddle.prototype.update = function () {
				var image = new Image();
				image.src = this.image.attr('src');
				var nWidth = image.naturalWidth;
				var nHeight = image.naturalHeight;

				if (nWidth > nHeight) {
					this.orientation = 'landscape';
				} else {
					this.orientation = 'portrait';
				}

				this.image.removeAttr('style');
				this.image.hide();
				if (this.orientation == 'landscape') {
					this.element.removeClass('vhmiddle-portarit').addClass('vhmiddle-landscape');
				}
				else if (this.orientation == 'portrait') {
					this.element.removeClass('vhmiddle-landscape').addClass('vhmiddle-portrait');
				}
			};

			VHMiddle.prototype.updateImage = function (newSrc) {
				var a = this;
				this.image.fadeOut('fast', function() {
					$(this).attr('src', newSrc).bind('onreadystatechange load', function(){
						a.update();
						if (this.complete) $(this).fadeIn('fast');
					});
				});
			};

			this.element.css({
				'width' : this.showWidth,
				'height' : this.showHeight,
			});

			this.update();
			if (this.image.is(':hidden')){
				this.image.fadeIn('fast');
			}

			this.image.load(function () {
				$this.update();
				if ($this.image.is(':hidden')){
					$this.image.fadeIn('fast');
				}
			});
		};

		return VHMiddle;
	})();

	$.fn.vhmiddle = function(userOptions) {
		return this.each(function () {
			var $this = $(this);
			if (!$this.data('vhmiddle')) {
				userOptions = $.extend({}, $.fn.vhmiddle.defaults, userOptions);
				$this.data('vhmiddle', new VHMiddle(this, userOptions));
			}
		});
	};

}(window.jQuery));
