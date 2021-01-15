// var SERVER = "https://sfapp-api.dreamstate-4-all.org/";
// var SERVER = 'http://localhost:8000/'
// /var passwordResetToken = getParam("token");
// var userToken = localStorage.getItem("user-token");

$(document).ready(function () {

  $(".login-button").on("click",  () => {
    $("#studentModal").addClass("is-visible");
  });

  $(".student-close").on("click", () => {
    $("#studentModal").removeClass("is-visible");
  });
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
      // window.location.assign('/students_list/')
    }
  })
}