$(document).ready(function() {

    
    $('#search-input').on('keyup', function(){
        var search_query = $(this).val();

        $.ajax({
            url: '/editStudent',
            data: {'search_query': search_query},
            success: function(data){
                $('#search-results').html(data);
            }
        });
    });
    



});