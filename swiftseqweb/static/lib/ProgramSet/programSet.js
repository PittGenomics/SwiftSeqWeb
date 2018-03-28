/**
 * Created by dfitzgerald on 8/14/15.
 */
;(function($) {

var numProgramSets = 0;

$.widget('swiftseq.ProgramSet', {
    /* Define public options */
    options: {
        stepId: null
    },

    /* Define instance variables */
    programSetId: undefined,
    $widgetContainer: null,
    $programSelectBox: null,
    $parametersContainer: null,
    parametersLines: [],
    currentProgramId: 0,

    _create: function () {
        var widget = this;
        widget.programSetId = numProgramSets;
        numProgramSets++;
        /* Get program set template */
        $.get('/generate-workflow/generate/get-program-set/' + this.options.stepId + '/'
                + widget.programSetId + '/', function (data) {
            var container = widget.element;
            widget.$widgetContainer = container;
            container.append($(data));
            container.find('select').select2();

            /* Get essential handles */
            widget.$programSelectBox = container.find('select.select-programs').first();
            widget.$parametersContainer = container.find('div.parameters-container').first();
            container.find('span.remove').click(function(){
                widget.destroy();
            });

            /* Attach event handler, trigger once for initialization */
            widget.$programSelectBox.on('change', function () {
                widget.currentProgramId = widget.$programSelectBox.val();
                widget._clearParameters();
                $.getJSON('/generate-workflow/generate/get-program-attrs/' + widget.currentProgramId + '/', function(data){
                    widget.$widgetContainer.find('a.help-url').attr('href', data.help_url);
                    widget.$widgetContainer.find('input.walltime').val(data.walltime);
                });

            }).trigger('change');
        });
    },

    _addParameter: function (programId) {
        var widget = this;

        /* Only add a new parameters line if there isn't a blank one available */
        for (var i = 0; i < widget.parametersLines.length; i++) {
            if ($(widget.parametersLines[i].parameterSelect).val() === '') return;
        }

        /* Add a new parameters line */
        var parameterName = 'programSet-' + widget.programSetId + '__parameter-' + widget.parametersLines.length;
        $.get('/generate-workflow/generate/get-parameters-line/' + parameterName + '/', function (data) {
            /* Append parameters line to container */
            var $parametersLine = $(data);
            widget.$parametersContainer.append($parametersLine);
            $parametersLine.slideDown(150);

            /* Get parameters for the current program */
            var programId = widget.currentProgramId;
            $.getJSON('/generate-workflow/generate/get-parameters-for-program/' + programId + '/', function (dataJson) {
                var $parameterSelect = $parametersLine.find('select').first();
                /* Turn parameter line select box into Select2 */
                $parameterSelect.select2({
                    data: dataJson,
                    placeholder: 'Select a parameter...',
                    allowClear: true,
                    tags: true,
                    createTag: function(term){
                        console.log(term);
                        return {id: '-1', text: term.term};
                    }
                }).on('change', function () {
                    widget._addParameter(programId);
                });

                /* Store reference in widget parameter lines array */
                widget.parametersLines.push({
                    line: $parametersLine,
                    parameterSelect: $parameterSelect
                });
            });
        });
    },

    _clearParameters: function () {
        var widget = this;
        /* Clear container and widget parameter lines array */
        widget.$parametersContainer.empty();
        widget.parametersLines = [];
        /* Add a parameter to container */
        widget._addParameter(widget.currentProgramId);
    },

    _destroy: function(){
        var widget = this;
        widget.$widgetContainer.remove();
    }
});

})(jQuery);