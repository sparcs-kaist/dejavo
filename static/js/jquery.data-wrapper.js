/*
 * image should not call this
 */

(function ($) {

	var DataWrapper = (function (element, options) {

		function DataWrapper(element, options) {
			var _this = this;
			var _element = $(element);

			this.changed = false;
			this.element = _element;
			this.getData = options.getData;
			this.setData = options.setData;
			this.onChanged = options.onChanged;
			this.options = options;

			$.each(options.trigger, function (i, a) {
				_element.on(a, function () {
					_this.changed = true;
					_this.onChanged();
				});
			});
		};

		DataWrapper.prototype.isChanged = function () {
			return this.changed;
		};

		DataWrapper.prototype.reset = function () {
			this.changed = false;
		};

		return DataWrapper;
	})();

	$.fn.datawrapper = function(userOptions) {

		return this.each(function () {
			var $this = $(this);
			if (!$this.data('datawrapper')) {
				userOptions = $.extend({}, $.fn.datawrapper.defaults, userOptions);
				$this.data('datawrapper', new DataWrapper(this, userOptions));
			}
		});
	};

	$.fn.datawrapper.defaults = {
		'trigger' : ['input'],
		'getData' : function () {},
		'setData' : function () {},
		'onChanged' : function () {},
	};

}(window.jQuery));
