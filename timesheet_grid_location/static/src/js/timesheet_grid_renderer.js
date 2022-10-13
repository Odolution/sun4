odoo.define('timesheet_grid_location.TimerGridRenderer', function (require) {
    "use strict";

    var TimerGridRenderer = require('timesheet_grid.TimerGridRenderer');
    const utils = require('web.utils');
    var rpc = require('web.rpc');

    utils.patch(TimerGridRenderer.prototype, 'location_patch',{
        async _setProjectTask(projectId, taskId) {
             await this._super(...arguments);

             var id_get = this.timesheetId;
             if (this.timesheetId){
                 function showPosition(position) {
                     rpc.query({
                         model: 'account.analytic.line',
                         method: 'save_location',
                         args: ["Abc",{"id":id_get,"longitude":position.coords.longitude,"latitude":position.coords.latitude}],
                     }).then(function (products) {
                         console.log(products);
                     });
                 }
                 function showError(error) {
                    switch(error.code) {
                      case error.PERMISSION_DENIED:
                        x.innerHTML = "User denied the request for Geolocation."
                        break;
                      case error.POSITION_UNAVAILABLE:
                        x.innerHTML = "Location information is unavailable."
                        break;
                      case error.TIMEOUT:
                        x.innerHTML = "The request to get user location timed out."
                        break;
                      case error.UNKNOWN_ERROR:
                        x.innerHTML = "An unknown error occurred."
                        break;
                    }
                  }
                  
                 if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition, showError);
                  } else { 
                    x.innerHTML = "Geolocation is not supported by this browser.";
                  }
             }

        },
    });

});