$(function(){

   $('.post_list').show();
   $('.smalltitle').click(function(){
       var cs = $(this).children('.oi').attr('class');
       if (cs == 'oi oi-plus mr-2'){
            $(this).children('.oi').attr('class','oi oi-minus mr-2');
       }else{
            $(this).children('.oi').attr('class','oi oi-plus mr-2');
       }
       $(this).siblings().toggle();

   });
   // hide or show tag edit form
   $('#tag-btn').click(function () {
        $('#tags').hide();
        $('#tag-form').show();
    });
    $('#cancel-tag').click(function () {
        $('#tag-form').hide();
        $('#tags').show();
    });

    $('#deleteModal').on('show.bs.modal', function (e) {
        $('.delete-form').attr('action', $(e.relatedTarget).data('href'));
    });

})  
