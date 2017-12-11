var TableDivCtrl = function($scope, dataService) {
  this.dataService_ = dataService;

  this.isEditing = false;

  this.header = [];
  this.bodyData = [];

  $scope.$watch(function(){ 
    return this.dataService_.curTableObj;
  }.bind(this), 
  function() {
    this.updateTableData();
  }.bind(this));
};

TableDivCtrl.prototype.updateTableData = function() {
  this.header = this.dataService_.curTableObj.header;
  this.bodyData = this.dataService_.curTableObj.bodyData;
};

TableDivCtrl.prototype.startEditing = function() {
  this.isEditing = true;
};

TableDivCtrl.prototype.applyEdits = function() {
  if (this.dataService_.curTableObj === undefined || 
      this.dataService_.curTableObj.name === undefined) {
    alert('Cannot find current table data.');
    return;
  }
  var tableName = this.dataService_.curTableObj.name;
  this.dataService_.changeTableData().success(function(data, status, headers, config) {
        console.log(data); 
        this.isEditing = false; 
        this.dataService_.getTableData(tableName);        
      }.bind(this))
      .error(function(data, status, headers, config) {
        this.isEditing = false;  
        alert('Failed to apply changes: ' + status);
      }.bind(this));;
};

TableDivCtrl.prototype.click = function(cellData) {
  console.log(cellData);
}

angular.module('hamster.directive.TableDiv', [])
       .directive('tableDiv', function() {
         return {
           restrict: 'E',
           scope: {},
           templateUrl: 'components/tableDiv/tableDiv.html',
           controller: TableDivCtrl,
           controllerAs: 'tableDivCtrl',
         };
       });