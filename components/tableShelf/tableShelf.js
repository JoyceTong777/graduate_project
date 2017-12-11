var TableShelfCtrl = function($mdDialog, $scope, dataService) {
  this.scope_ = $scope;

  this.dataService_ = dataService;

  this.tableList = [];

  $scope.$watch(function(){ 
    return this.dataService_.tableList;
  }.bind(this), 
    function() {
      console.log("table list changed");
      this.tableList = this.dataService_.tableList;
  }.bind(this));

  function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.add = function(answer) {
      console.log("add");
      $mdDialog.hide(answer);
    };
  }

  $scope.showAddTable = function(ev) {
    $mdDialog.show({
      controller: AddTableDialogCtrl,
      controllerAs: 'addTableDialogCtrl',
      templateUrl: 'components/tableShelf/addTableDialog.html',
      parent: angular.element(document.body),
      targetEvent: null,
      clickOutsideToClose:true,
    })
    .then(function(answer) {
    }, function() {
    });
  };
};

TableShelfCtrl.prototype.clickTable = function(table) {
  this.dataService_.getTableData(table);
  console.log(table);
};  


var AddTableDialogCtrl = function($scope, $mdDialog, dataService) {
  this.mdDialog_ = $mdDialog;

  this.scope_ = $scope;

  this.dataService_ = dataService;
};

AddTableDialogCtrl.prototype.cancel = function() {
  this.mdDialog_.hide();
};

AddTableDialogCtrl.prototype.apply = function() {
  var formData  = new FormData();
  formData.append('file', document.getElementById('csvUpload').files[0]);
  this.dataService_.uploadTable(formData);

  this.mdDialog_.hide();
};

angular.module('hamster.directive.TableShelf', [])
       .directive('tableShelf', function() {
         return {
           restrict: 'E',
           scope: {},
           templateUrl: 'components/tableShelf/tableShelf.html',
           controller: TableShelfCtrl,
           controllerAs: 'tableShelfCtrl',
         };
       });
