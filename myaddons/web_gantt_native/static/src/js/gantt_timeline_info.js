odoo.define('web_gantt_native.Info', function (require) {
"use strict";

var Widget = require('web.Widget');

var GanttTimeLineInfo = Widget.extend({
    template: "GanttTimeLine.info",

    init: function(parent) {
        this._super.apply(this, arguments);
    },


    start: function(){

        var self = this;
        var el = self.$el;

        var parentg =  this.getParent();


        var data_widgets =  parentg.gantt_timeline_data_widget;

        _.each(data_widgets, function(widget) {

            if (!widget.record.is_group) {

                if (widget.record["bar_start_info"] || widget.record["bar_end_info"]) {

                    var el = widget.$el;

                    var row_id = widget.record.id;
                    var rowdata = '.task-gantt-bar-plan-' + row_id;

                    var info_start = widget.record["bar_start_info"] || '';
                    var info_end = widget.record["bar_end_info"] || '';


                    var bar_start_info = $('<div class="task-gantt-bar-plan-start-info"/>');
                    var bar_end_info = $('<div class="task-gantt-bar-plan-end-info"/>');
                    bar_start_info.text(info_start);
                    bar_end_info.text(info_end);



                    var bar_left = 6 * info_start.length;

                    bar_start_info.css({"left": -1*(bar_left) + "px"});
                    bar_start_info.css({"width": 6 * info_start.length + "px"});


                    var bar_right = 10 * info_end.length;
                    bar_end_info.css({"right": -1*(bar_right+10) + "px"});
                    bar_end_info.css({"width": 10 * info_end.length + "px"});

                    el.find(rowdata).append(bar_start_info);
                    el.find(rowdata).append(bar_end_info);
                }

            }

            return true;
        })


    }


});

return {
    // get_data_ghosts: get_data_ghosts,
    InfoWidget: GanttTimeLineInfo
}

});