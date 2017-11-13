/**
 * Created by dfitzgerald on 8/10/15.
 */
$(document).ready(function(){
    var showPointer = 0;
    var finished = false;

    var $nextButton = $('button#next_button');
    var $questionPanels = $('div.panel');
    $questionPanels.first().show();

    /* This is executing twice, find out why TODO */
    $('label.swiftseq-label-box').click(function(){
        console.log($(this).data('order'));
        console.log(showPointer);
        if(!finished && $(this).data('order') === showPointer){
            showPointer++;
            if($nextButton.data('enabled') == showPointer){
                $nextButton.prop('disabled', '');
                finished = true;
            }else{
                $('div[data-order=' + showPointer + ']').slideDown(150);
            }
        }
    });
});