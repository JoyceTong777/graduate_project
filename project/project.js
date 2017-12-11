var ProjectCtrl = function($scope, dataService) {
	this.dataService_ = dataService;
	this.name = '';

  $scope.$watch(function(){ 
    return this.dataService_.curTableObj;
  }.bind(this), 
  function() {
    this.name = dataService.curTableObj.name;
  }.bind(this));
};

ProjectCtrl.prototype.download = function() {
	if (this.dataService_.curTableObj === undefined ||
			this.dataService_.curTableObj.name === undefined) {
		alert("Cannot find current table data.");
		return;
	}

  var tableData = 
  		this.dataService_.convertTableObj(this.dataService_.curTableObj);

  var csvContent = 'data:text/csv;charset=utf-8,';
  tableData.data.forEach(function(rowArray){
   	let row = rowArray.join(",");
   	csvContent += row + "\r\n"; // add carriage return
	}); 

  var data = encodeURI(csvContent);

  var fileName = tableData.name;
  if (!fileName.endsWith(".csv")) {
  	fileName += '.csv';
  }

  var link = document.createElement('a');
  link.setAttribute('href', data);
  link.setAttribute('download', fileName);
  link.click();
}