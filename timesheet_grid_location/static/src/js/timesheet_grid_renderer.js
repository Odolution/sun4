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
                 navigator.geolocation.getCurrentPosition(showPosition);
             }

        },
    });

});