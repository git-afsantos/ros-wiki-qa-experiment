(function () {
    "use strict";
    var ROSQA = Object.create(null);

    ROSQA.data = {
        electricqa: null,
        fuerteqa:   null,
        groovyqa:   null,
        hydroqa:    null,
        indigoqa:   null,
        jadeqa:     null,
        kineticqa:  null,
        lunarqa:    null,
        melodicqa:  null
    };

    ROSQA.showDetails = function (el) {
        var $el = $(el), id = $el.attr("id");
        var data = ROSQA.data[id];
        $("#" + id + "-panel").toggle();
        return false;
    };

    window.ROSQA = ROSQA;
})();
