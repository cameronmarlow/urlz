var Tag = function(data) {
  this.owner_id = ko.observable(data.owner_id);
  this.name = ko.observable(data.name);
  this.type = ko.observable(data.type);
  this.description = ko.observable(data.description);
}

var Link = function(data) {
  this.url = ko.observable(data.url);
  this.redirect_to = ko.observable(data.redirect_to);
  this.redirects = ko.observableArray(data.redirects);
  this.status = ko.observable(data.status);
  this.title = ko.observable(data.title);
  this.description = ko.observable(data.description);
  this.image = ko.observable(data.image);
}

function TagListViewModel(params) {
  // Data
  var self = this;
  self.tags = ko.observableArray([]);
  self.newTagText = ko.observable();

  self.init = function() {
    api.client.tag.read().done(self.setTags);
    return self;
  };

  self.setTags = function(data) {
    ko.mapping.fromJS(data.objects, Tag, self.tags);
  };

  // Operations
  self.addTag = function () {
    self.tags.push(new Tag({ name: this.newTagText() }));
    self.newTagText = "";
  };
}

var tagListViewModel = new TagListViewModel().init()

ko.applyBindings(tagListViewModel);