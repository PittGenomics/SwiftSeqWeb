/**
 * Created by dfitzgerald on 8/11/15.
 */
$(document).ready(function(){
    var getParametersForProgramURL = '/generate-workflow/generate/get-parameters-for-program/';

    $('.option-checkbox').change(function(){
        /* Get the Step ID, hook it up to respective program panel */
        var stepId = $(this).data('stepid');
        var $panel = $('div.panel-program[data-stepid="' + stepId + '"]');
        $panel.slideToggle(150);
    });

    $('div.programset').each(function(){
        var stepId = $(this).parent('div.panel-program').data('stepid');
        $(this).ProgramSet({stepId: stepId});
    });

    $('span.add-program').click(function(){
        var stepId = $(this).data('stepid');
        var $panelProgram = $('div.panel-program[data-stepid="'+stepId+'"]');
        $('<div>').addClass('panel-body programset').appendTo($panelProgram).ProgramSet({stepId: parseInt(stepId)});
    });

    $('#submitbutton').click(function(){
        $('input').removeAttr('disabled');
        $('<iframe>').attr({
            src: '/generate-workflow/process-workflow/?' + $('form').serialize(),
            style: 'display:none'
        }).appendTo($('body')).ready(function(){
            window.location.replace('/generate-workflow/download-complete/');
        });
    });

    /* Make available options box sticky */
    var sticker = $('#sticker');
    var stickerWidth = sticker.outerWidth(true);
    sticker.css('width', stickerWidth);
    var rightCol = $('#rightCol');
    var pos = sticker.position();
    $(window).scroll(function(){
        var windowpos = $(window).scrollTop();
        if(windowpos >= pos.top - 50){
            sticker.addClass('stick');
            rightCol.addClass('col-md-offset-4');
        }else{
            sticker.removeClass('stick');
            rightCol.removeClass('col-md-offset-4');
        }
    }).resize(function(){
        stickerWidth = sticker.outerWidth(true);
    });
});