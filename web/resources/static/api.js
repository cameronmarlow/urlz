(function(window, $){
  var API = function(elem, options){
      this.elem = elem;
      this.$elem = $(elem);
      this.options = options;
    };

  API.prototype = {
    defaults: {
      path: '/api/',
      types: ['user', 'post', 'tag']
    },
    init: function() {
      this.config = $.extend({}, this.defaults, this.options);
      var client = new $.RestClient('/api/', {
        ajax: {contentType: "application/json"},
        stringifyData: true,
        stripTrailingSlash: true
      });
      $.each(this.config.types, function(index, value) {
        client.add(value);
      });
      this.client = client
      return this;
    },
  };

  API.defaults = API.prototype.defaults;

  $.fn.api = function(options) {
    return this.each(function() {
      new API(this, options).init();
    });
  };

  window.API = API;
})(window, jQuery);


$( document ).ready(function() {
  var client = new $.RestClient('/api/', {
      ajax: {contentType: "application/json"},
      stringifyData: true,
      stripTrailingSlash: true
  });



});