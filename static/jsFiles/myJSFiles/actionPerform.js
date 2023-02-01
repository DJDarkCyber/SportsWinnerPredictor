$(document).ready(function() {

    
    
    // $(".web-showcase-events").hover(function(){
    //   $(".showcase-events-desc").slideDown("fast");
      
    // },
    // function(){
    //   $(".showcase-events-desc").slideUp("fast", function(){
      
    //   });
    // }
    // );

    $(".web-showcase-events").on('mouseenter touchstart', function(){
      $(this).find(".showcase-events-desc").slideDown("fast");
    }).on('mouseleave touchend', function(){
      $(this).find(".showcase-events-desc").slideUp("fast");
    }
  );



});


$(document).scroll(function() {
    $("#header").toggleClass("scrolled", $(this).scrollTop() > 50);
  });