var UrlzAPI = (function () {

  return {
    init: function(options) {
      this.defaults = {
        path: '/api/',
        types: {
          user: 'user',
          post: 'post',
          tag: 'tag',
          link: 'url'   // URL is a reserved method
        }
      }

      $.extend({}, this.defaults, this.options);

      var client = new $.RestClient('/api/', {
        ajax: {contentType: "application/json"},
        stringifyData: true,
        stripTrailingSlash: true
      });
      $.each(this.defaults.types, function(key, value) {
        client.add(key, {url: value});
      });
      this.client = client
      return this;
    },
  }


});

$( document ).ready( api = UrlzAPI().init() );