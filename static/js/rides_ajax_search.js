/**
 * Created by Alice on 4/28/2017.
 */
///THIS FILE MUST BE IMPORTED BEFORE THE "main" FILE.
/**
  Executes a search for colors containing a substring.
 */
var processSearch = function()  {
  //The key-press listener is no longer attached

  //Get and trim the search text.
  var searchText = $('#rides_search_text').val().trim().toUpperCase();

  // if(searchText.length < MIN_SEARCH_CHARS)  {
  //   //Too short. Ignore the submission, and erase any current results.
  //   $('#rides_search_results').html("");
  //
  // }  else  {
  //   //There are at least two characters. Execute the search.
  //
    var processServerResponse = function(serverResponse_data, textStatus_ignored,jqXHR_ignored)
    {
       // alert("serverResponse_data='" + serverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "'");
      $('#rides_search_results').html(serverResponse_data);
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
        'rides_search_text' : searchText,
          'ride_type': ride_type
      },
      dataType: 'html',
      failure:function(){
        alert('server request failed');
      },
      success: processServerResponse,
    };
    $.ajax(config);
};