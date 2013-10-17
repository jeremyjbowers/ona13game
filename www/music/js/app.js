// Enclosures are good.
$(document).ready(function(){

  // Load the events JSON.
  $.ajax('events.json', {
    dataType: 'json',
    success: function(events, status, jqXHR){
      // Do something on success. IN this case, let's loop over the events.
      // Underscore is wonderful. _.each is underscore's loop construct.
      // Loops over "events" and make an anonymous function that returns
      // the individual event as "e", the index as "idx" and a something else.
      // I'm not actually sure what "list" is. It's in the docs, though!
      _.each(events, function(e, idx, list){

        // Log to the console. FOR SCIENCE.
        var date = new Date(e.timestamp*1000);

        var days_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        e['timestamp_slice'] = date.getDay();
        e['timestamp_string'] = days_of_the_week[date.getDay()];

        // This is the tricksy part.
        // Templates are better than string appending.
        // I stored a template in the HTML in a script tag.
        // Read about Underscore templates; they are the Lord's work.
        var compiled = _.template($('script.template-event').html());



        // Append the compiled template to div#info.
        // Also, compile the template with a variable called 'evnt'
        // that's just this instance of the event object.
        $('#info').append(compiled({ 'evnt': e }));
      });

      // Don't forget to count the cards as a condition of AJAX success.
      count_visible_cards();

    }
  });

  // Dear God, things need to filter.
  $('button').on('click', function(){

    // Get the day slice from the button. This is like 0 = Sunday, etc.
    var day_slice = $(this).attr('data-date-slice');

    // Convert that day slice into the class of cards that we want to hide.
    var day_slice_class = 'div.day-' + day_slice;

    // Hide all cards, since we only want to show certain ones.
    $('div.card').hide();

    // Show just our event days.
    $(day_slice_class).show();

    // Count what's visible.
    count_visible_cards();
  });

  // Want Grub? Click the button and a list of restaurants will show up.
  $('#wrap').on('click', '.restaurant-toggle', function(){
    console.log($(this));
    $(this).next('.restaurant-list').slideToggle('fast');
  });

  var count_visible_cards = function(){

    // Find all of the card divs that aren't hidden.
    var visible_cards = $('div.card').not(':hidden');

    // Write the card text to the H2 we previously made and replace text in there.
    $('#count-target h2').text(String(visible_cards.length) + ' events happening.');
  };

});

window.slugify = function(t){
  return t.replace(/[^-a-zA-Z0-9\s]+/ig, '').replace(/-/gi, "_").replace(/\s/gi, "-").toLowerCase();
}