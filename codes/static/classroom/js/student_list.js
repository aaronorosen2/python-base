$(document).ready(function () {

  $(".login-button").on("click",  () => {
    $("#studentModal").addClass("is-visible");
  });

  $(".student-close").on("click", () => {
    $("#studentModal").removeClass("is-visible");
  });
  // getStudentData() //get all student list from javascript using ajax call
});

function deleteId(id){
  $.ajax({
    url:'/students_list/delete/',
    data: {
      'id': id 
    },
    datatype:'json',
    success: function(){
      location.reload();
    }
  })
}

// function getStudentData(){
//   console.log("Ajax called")
//   $.ajax({
//     method: 'GET',
//     url:'/students_list/get/students',
//     async: false,
//     datatype:'json',
//     success:  (response,textStatus,jqXHR ) =>{
//       console.log(response)
//     },
//     error:  (jqXHR,textStatus,errorThrown) => {
//       console.log(jqXHR)
//       console.log(textStatus)
//       console.log(errorThrown)
//     }

//   })
// }

