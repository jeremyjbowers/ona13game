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
        console.log(e);
        var date = new Date(e.timestamp*1000);
        console.log(date);

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
    }
  });
});