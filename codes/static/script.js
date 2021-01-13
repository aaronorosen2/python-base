$(document).on("click", ".open-AddBookDialog", function () {

    var myBookId = $(this).data('val');
    console.log(myBookId)
    const date = document.getElementById("date")
    date.value= myBookId
   console.log(date)

});