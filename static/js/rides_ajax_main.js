/**
 * Created by Alice on 4/28/2017.
 */
//THIS MUST BE IMPORTED AS THE VERY LAST THING BEFORE THE CLOSE </body>
//tag.

/**
  The number of milliseconds to ignore key-presses in the search box,
  after a key *that was not ignored* was pressed. Used by
  `$(document).ready()`.

  Equal to <code>100</code>.
 */
var MILLS_TO_IGNORE_SEARCH = 0.01;
var FIRST_TIME = true
/**
  The number of milliseconds to ignore clicks on the *same* like
  button, after a button *that was not ignored* was clicked. Used by
  `$(document).ready()`.

  Equal to <code>500</code>.
 */
var MILLS_TO_IGNORE_LIKES = 500;
/**
   The Ajax "main" function. Attaches the listeners to the elements on
   page load, each of which only take effect every
   <link to MILLS_TO_IGNORE_SEARCH> or <link to MILLS_TO_IGNORE_LIKES>
   seconds.

   This protection is only against a single user pressing buttons as fast
   as they can. This is in no way a protection against a real DDOS attack,
   of which almost 100% bypass the client (browser) (they instead
   directly attack the server). Hence client-side protection is pointless.

   - http://stackoverflow.com/questions/28309850/how-much-prevention-of-rapid-fire-form-submissions-should-be-on-the-client-side

   The protection is implemented via Underscore.js' debounce function:
  - http://underscorejs.org/#debounce

   Using this only requires importing underscore-min.js. underscore-min.map
   is not needed.
 */
$(document).ready(function() {
    /*
     Warning: Placing the true parameter outside of the debounce call:

     $('#color_search_text').keyup(_.debounce(processSearch,
     MILLS_TO_IGNORE_SEARCH), true);

     results in "TypeError: e.handler.apply is not a function"
     */
    //    var config = {
    //        /*
    //         Using GET allows you to directly call the search page in
    //         the browser:
    //
    //         http://the.url/search/?color_search_text=bl
    //
    //         Also, GET-s do not require the csrf_token
    //         */
    //        type: "GET",
    //        url: SUBMIT_URL,
    //        dataType: 'json',
    //        success: function (data) {
    //        //     alert(data)
    //        // }
    //              var trHTML = '';
    //              $('#results_section').append(
    //                  $.map($.makeArray(data.Rides), function(item, index){
    //                      return '<tr><td>' + item +  '</td></tr>' + data.Rides[index] + '</td></tr>';}).join());
    //                }
    //
    //        };
    // $.ajax(config);

        var processInitialResponse = function(serverResponse_data, textStatus_ignored,jqXHR_ignored)
    {
       // alert("serverResponse_data='" + serverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "'");
      $('#rides_search_results').html(serverResponse_data);
      FIRST_TIME=false
    }

    var ride_type = window.location.pathname.split('/')[1];
    console.log(ride_type);
    var config = {
      /*
        Using GET allows you to directly call the search page in
        the browser:

        http://the.url/search/?color_search_text=bl

        Also, GET-s do not require the csrf_token
       */
      type: "GET",
      url: SUBMIT_URL,
      data: {
        'rides_search_text' : "",
          'ride_type': ride_type
      },
      dataType: 'html',
      failure:function(){
        alert('server request failed');
      },
      success: processInitialResponse,
    };
    $.ajax(config);


    $('#rides_search_text').keyup(_.debounce(processSearch,
        MILLS_TO_IGNORE_SEARCH, true));

    $("#rides_search_text").keypress(function(){
      var x = event.which || event.keyCode;
      if (x == 13) {
        document.activeElement.blur()
        //$("#inputWithFocus").blur()
      }
});
});