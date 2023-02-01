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

  $(".predictOptionsContainer").on('mouseenter touchstart', function(){
    $(this).css("box-shadow", "rgba(130, 43, 201, 0.2) 0px 7px 29px 0px");
    $(".predictOptionHeader").css("color", "#d3c8e7");
  }).on('mouseleave touchend', function(){
    $(this).css("box-shadow", "rgba(130, 43, 201, 0.2) 0px 7px 29px 0px inset");
    $(".predictOptionHeader").css("color", "#BFACE0");
  });  


});


$(document).scroll(function() {
    $("#header").toggleClass("scrolled", $(this).scrollTop() > 50);
  });