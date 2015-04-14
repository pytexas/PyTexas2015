pytx.factory("APIFactory", function ($http) {
  function APIFactory (version, scope) {
    this.version = version;
    this.loading = false;
    this.scope = scope;
    
    this.finished_loading = this._finished_loading.bind(this);
    this.show_form_errors = this._show_form_errors.bind(this);
  }
  
  APIFactory.prototype.get = function (url, params, config) {
    var APIService = this;
    APIService.loading = true;
    url = APIService.prepare_url(url);
    params = APIService.prepare_params(params);
    config = config || {};
    config.params = params;
    
    var promise = $http.get(url, config);
    promise.finally(APIService.finished_loading);
    return promise;
  };
  
  APIFactory.prototype.post_form = function (url, params, config) {
    var APIService = this;
    APIService.loading = true;
    url = APIService.prepare_url(url);
    params = APIService.prepare_params(params);
    
    var promise = $http.post(url, params, config);
    promise.error(APIService.show_form_errors);
    promise.finally(APIService.finished_loading);
    return promise;
  };
  
  APIFactory.prototype.post = function (url, params, config) {
    var APIService = this;
    APIService.loading = true;
    url = APIService.prepare_url(url);
    params = APIService.prepare_params(params);
    
    var promise = $http.post(url, params, config);
    promise.finally(APIService.finished_loading);
    return promise;
  };
  
  APIFactory.prototype._finished_loading = function () {
    this.loading = false;
  };
  
  APIFactory.prototype._show_form_errors = function (data) {
    if (data.errors) {
      this.scope.errors = data.errors;
      this.scope.show_error('Please correct the errors in your request.');
    }
    
    else if (data.message) {
      this.scope.show_error(data.message);
    }
  };
  
  APIFactory.prototype.prepare_url = function (url) {
    url = CONFIG.api_base + 'api/' + this.version + '/' + url;
    
    return url;
  };
  
  APIFactory.prototype.prepare_params = function (params) {
    params = params || {};
    params.conf = CONFIG.conf;
    
    return params;
  };
  
  return APIFactory;
});
