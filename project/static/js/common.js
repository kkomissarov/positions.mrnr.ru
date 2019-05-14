$('#delete_project').click(function() {
	$('.modal-window-background').fadeIn(400);
	$('.modal-window-main').fadeIn(400);

});


function CloseDeleteWindow() {
	$('.modal-window-background').fadeOut(400);
	$('.modal-window-main').fadeOut(400);
};


$('.del-nope').click(CloseDeleteWindow);
$('.modal-window-background').click(CloseDeleteWindow);


$('.success_message').ready(
	function() {
		setTimeout(
			function(){
				$('.success_message').fadeOut(300);
			
		}, 2000);
	});


  $( function() {
    $( "#start_date" ).datepicker({
    	dateFormat: "dd M yy",
    	dayNamesMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    	monthNames: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    	monthNamesShort :["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"], 
    	changeMonth: true,
    	changeYear: true,
    	maxDate: 0,
    	minDate: "-6m",
    	hideIfNoPrevNext: true
    });
  });


$( function() {
	$( "#finish_date" ).datepicker({
    	dateFormat: "dd M yy",
    	dayNamesMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    	monthNames: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    	monthNamesShort :["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"], 
    	changeMonth: true,
    	changeYear: true,
    	maxDate: 0,
    	minDate: "-6m",
    	hideIfNoPrevNext: true
	 });
});