var dataService = function($http) {
  this.http_ = $http;

  this.UPLOAD_TABLE_ = '/upload';

  this.REQUEST_TABLE_LIST_ = '/requestTableList/';

  this.REQUEST_TABLE_DATA_ = '/requestTableData/';

  this.CHANGE_TABLE_DATA_ = '/changeTableData/';

  this.OUTLIER_NAME_LIST = [
      'emptyOutlier', 
      'patternInconsistent',
      'lengthOutlier',
      'numericalOutlier'
      ];

  // The outlier name to color mapping.
  this.OUTLIER_NAME_COLOR = {
      'emptyOutlier': '#87CEEB', // sky blue
      'patternInconsistent': '#FA8072', //salmon
      'lengthOutlier': 'orange',
      'numericalOutlier': '#9ACD32',// yellow green
  };

  this.isQueryingTable = false;

  this.tableList = [];

  this.getTableList();

  this.curTableObj = {};
 
  this.lastClick_ = {
    chartRow: -1,
    chartColumn: -1,
  };

};

dataService.prototype.uploadTable = function(formData) {
  this.http_.post(this.UPLOAD_TABLE_, formData, {
          headers: {'Content-Type': undefined},
          transformRequest: angular.identity
      })
      .success(function(data, status, headers, config) {
        this.getTableList();     
      }.bind(this))
      .error(function(data, status, headers, config) {
        alert("The table already exists.");
      }.bind(this));
  
};

dataService.prototype.getTableList = function() {
  var request = {
  };
  this.tableList = [];

  return this.http_.post(this.REQUEST_TABLE_LIST_, JSON.stringify(request))
      .success(function(data, status, headers, config) {
        this.tableList = data;
      }.bind(this))
      .error(function(data, status, headers, config) {
        console.log('error');
        console.log(data);
      }.bind(this));
};


dataService.prototype.getTableData = function(tableName) {
  var request = {
    'name': tableName
  };

  this.isQueryingTable = true;

  return this.http_.post(this.REQUEST_TABLE_DATA_, request, {
        headers: {'Content-Type': 'application/json'}
      })
      .success(function(data, status, headers, config) {
        console.log(data);
        this.parseTableData(data); 
        this.isQueryingTable = false;
      }.bind(this))
      .error(function(data, status, headers, config) {
        alert("Failed to get table data.");
        this.isQueryingTable = false;
      }.bind(this));
};

// Parses table data to tableObj and tableChart.
dataService.prototype.parseTableData = function(tableData) {
  this.curTableObj = {
    name: tableData.name,
    header: [],
    bodyData: [],
    anomaly: tableData.anomaly
  };
  var bodyData = this.curTableObj.bodyData;
  for (var i in tableData.data) {
    var colData = tableData.data[i];
    this.curTableObj.header[i] = { 
      value: colData.header
    };

    for (var j in colData.colData) {
      while (j >= bodyData.length) {
        bodyData.push([]);
      }
      bodyData[j][i] = {
        value: colData.colData[j]
      };
    }
  }
};


dataService.prototype.clickOutlier = function(chartRow, chartColumn) {
  this.resetTableColor();
  if (this.lastClick_.chartRow === chartRow && this.lastClick_.chartColumn === chartColumn) {
    return;
  }

  this.lastClick_.chartRow = chartRow;
  this.lastClick_.chartColumn = chartColumn;

  var colNum = chartRow;

  if (this.curTableObj.anomaly.length <= colNum) {
    alert('Cannot find the anomaly of the clicked column.');
    return;
  }
  var outlierName = this.OUTLIER_NAME_LIST[chartColumn - 1];
  if (outlierName === undefined) {
    alert('Unknown anomaly.');
    return;
  }

  var backgroundColor = this.OUTLIER_NAME_COLOR[outlierName];
  if (backgroundColor === undefined) {
    alert('Cannot find color of this type of outlier.');
    return;
  }

  var indexList = this.curTableObj.anomaly[colNum][outlierName];
  if (indexList === undefined) {
    alert('Cannot find the cells of this type of outlier.');
    return;
  }

  for (var i in indexList) {
    var index = indexList[i];
    if (index >= this.curTableObj.bodyData.length) {
      alert('The outlier row index: ' + index + ' is out-of-range.');
      continue;
    }
    this.curTableObj.bodyData[index][colNum].backgroundColor = 
        backgroundColor;

  }
};

dataService.prototype.resetTableColor = function() {
  for (var i in this.curTableObj.bodyData) {
    for (var j in this.curTableObj.bodyData[i]) {
      this.curTableObj.bodyData[i][j].backgroundColor = '';
    }
  }
};

dataService.prototype.changeTableData = function() {
  if (this.curTableObj === undefined || this.curTableObj.header === undefined ||
      this.curTableObj.bodyData === undefined) {
    alert('Cannot find current table data.');
    return;
  }

  if (this.curTableObj === undefined || this.curTableObj.header === undefined ||
      this.curTableObj.bodyData === undefined) {
    alert('Cannot find current table data.');
    return;
  }

  var tableData = this.convertTableObj(this.curTableObj);
  return this.http_.post(this.CHANGE_TABLE_DATA_, JSON.stringify(tableData));
};

dataService.prototype.convertTableObj = function(tableObj) {
  var tableData = {
    'name': tableObj.name,
    'data': []
  };

  var headerData = [];
  for (var i in tableObj.header) {
    headerData.push(tableObj.header[i].value);
  }
  tableData['data'].push(headerData);

  for (var rowIdx in tableObj.bodyData) {
    var rowData = [];
    for (var i =0; i < tableObj.bodyData[rowIdx].length;++i) {
      rowData.push(tableObj.bodyData[rowIdx][i].value);
    }
    tableData['data'].push(rowData);
  }
  return tableData;
};

angular.module('hamster.service.dataService', [])
	     .service('dataService', dataService);