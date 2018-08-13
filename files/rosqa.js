(function () {
    /* globals window:false, $:false*/
    "use strict";
    var ROSQA = Object.create(null);

    var sample_data = {
        "loc": 1733,
        "comment_ratio": "33.3%",
        "cyclomatic_complexity": 3,
        "maintainability_index": null,
        "class_coupling": null,
        "depth_inheritance": null,
        "coding_violations": 615
    };

    ROSQA.data = {
        electricqa: null,
        fuerteqa:   null,
        groovyqa:   null,
        hydroqa:    sample_data,
        indigoqa:   sample_data,
        jadeqa:     null,
        kineticqa:  sample_data,
        lunarqa:    null,
        melodicqa:  null
    };

    ROSQA.showDetails = function (el) {
        var $el = $(el), id = $el.attr("id");
        var data = ROSQA.data[id];
        if (data != null) {
            var $panel = $("#" + id + "-panel");
            ROSQA.populateTable($panel, data);
            $panel.toggle();
        }
        return false;
    };

    ROSQA.populateTable = function ($panel, data) {
        var $table = $panel.find(".qa-metrics-table");
        if ($table.data("populated")) return;
        var $cells = $table.find("td");
        for (var i = $cells.length; i--;) {
            var metric = $cells[i].dataset.metric;
            if (metric != null) {
                var value = data[metric];
                if (value != null) {
                    $cells.eq(i).text("" + value);
                } else {
                    $cells.eq(i).text("-");
                }
            }
        }
        $table.data("populated", true);
    };

    window.ROSQA = ROSQA;
})();
