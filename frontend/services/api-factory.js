pytx.factory("APIFactory", function ($http) {
  function APIFactory (version) {
    this.version = version;
    this.loading = false;
    this.finished_loading = this._finished_loading.bind(this);
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
  
  APIFactory.prototype._finished_loading = function () {
    this.loading = false;
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
