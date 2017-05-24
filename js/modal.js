$(function() {

var modal = $('.modal');
var closeButtons = $('.close-modal');
// set open modal behaviour

$('.open-modal').on('click', function() {
	var modal_id = $(this).attr("data");
	var modal_c = $("#" + modal_id);
  	modal_c.addClass('modal-open');
});

// set close modal behaviour
$.each(closeButtons, function(i, closeButton){
	$(closeButton).on('click', function(){
		modal.removeClass('modal-open');
	})
});


// close modal if clicked outside content area
$('.modal-inner').on('click', function() {
  modal.removeClass('modal-open');
});

// prevent modal inner from closing parent when clicked
$('.modal-content').on('click', function(e) {
	e.stopPropagation();
});

})
