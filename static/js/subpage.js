$('#option1').click(function() {
    $.ajax({
      type: 'GET',
      url: '{{ url_for("subpage1")}}',
      dataType: 'html',
      success: function(response) {
        $('#div-html').html(response);
      }
    });
  });
  
  $('#option2').click(function() {
    $.ajax({
      type: 'GET',
      url: '{{ url_for("subpage2")}}',
      dataType: 'html',
      success: function(response) {
        $('#div-html').html(response);
      }
    });
  });