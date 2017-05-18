$(function() {

var modal = $('.modal');
var closeButtons = $('.close-modal');
// set open modal behaviour

$('.open-modal').on('click', function() {
  modal.toggleClass('modal-open');
});
// set close modal behaviour

/*
for (i = 0; i < closeButtons.length; ++i) {
  closeButtons[i].addEventListener('click', function() {
    modal.toggleClass('modal-open');
	});
}
*/


// close modal if clicked outside content area
$('.modal-inner').on('click', function() {
  modal.toggleClass('modal-open');
});

// prevent modal inner from closing parent when clicked
$('.modal-content').on('click', function(e) {
	e.stopPropagation();
});

})
