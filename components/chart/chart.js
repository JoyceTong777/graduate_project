var ChartCtrl = function($scope, dataService) {
  this.scope_ = $scope;
  
  this.dataService_ = dataService;

  this.tableObj = dataService.curTableData;

  this.scope_.$watch(function(){ 
    return this.dataService_.curTableObj;
  }.bind(this), 
  function() {
    this.drawAnomalyChart(this.dataService_.curTableObj);
  }.bind(this));

  
};

ChartCtrl.prototype.drawAnomalyChart = function(tableObj) {
  if (!tableObj.hasOwnProperty('header') || 
      !tableObj.hasOwnProperty('anomaly')) {
    return;
  }
  if (tableObj.header.length !== tableObj.anomaly.length) {
    alert("Column size mismatchs.");
    return;
  }

  var drawData = [
    ['Column Name', 'empty', 'patternInconsistent', 'length', 
        'numericalOutlier', { role: 'annotation' }],
  ];

  // The i-th column.
  for (var i in tableObj.anomaly) {
    var colArray = [];
    // Adds header.
    colArray.push(tableObj.header[i].value);
    for (var j in this.dataService_.OUTLIER_NAME_COLOR) {
      colArray.push(
          tableObj.anomaly[i][j].length);
    }

    colArray.push('');
    drawData.push(colArray);
  }

  console.log(drawData);

  var data = google.visualization.arrayToDataTable(drawData);

  var options = {
    isStacked: true,
    chartArea:{top:50,left:50,bottom:60,width:'80%',height:'80%'},
    series: {
      0:{color:'#87CEEB'},
      1:{color:'#FA8072'},
      2:{color:'orange'},
      3:{color:'#9ACD32'},
    }
  };
  var chart = new google.visualization.ColumnChart(
      document.getElementById("chart_div"));
  chart.draw(data, options);  

  google.visualization.events.addListener(chart, 'select', selectHandler.bind(this));

  function selectHandler() {
    var selection = chart.getSelection();
    if (selection.length === 0) return;
    var row = selection[0].row;
    var column = selection[0].column;
    
    this.dataService_.clickOutlier(row, column);
    this.scope_.$apply();
  };
};

angular.module('hamster.directive.Chart', [])
       .directive('chart', function() {
         return {
           restrict: 'E',
           scope: {},
           templateUrl: 'components/chart/chart.html',
           controller: ChartCtrl,
           controllerAs: 'chartCtrl',
         };
       });