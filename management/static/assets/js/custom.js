// Login  
$(document).ready(function () {

  displayMessages();

  // Forgot Password
  $("#forgot-password-form").submit(function() {
    $("#updatePasswordButton").hide();
    $("#updatePasswordSpinner").show();
    return true;
  });
});


// My table
$(document).ready(function () {
  let table = $("#mytable").DataTable();
});


// Leads 
$(document).ready(function () {

  displayMessages();
  // Add Lead
  $("#addLeadForm").submit(function() {
    $("#saveLeadButton").hide();
    $("#saveLeadSpinner").show();
    return true;
  });

  // Edit Lead 
  $("#table").on("click", ".edit-lead-link", function () {
    $("#edit_lead [name='first_name']").val($(this).data("first-name"));
    $("#edit_lead [name='last_name']").val($(this).data("last-name"));
    $("#edit_lead [name='email']").val($(this).data("email"));
    $("#edit_lead [name='phone']").val($(this).data("phone"));
    $("#edit_lead [name='company']").val($(this).data("company"));
    var websiteValue = ($(this).data("website") === "None") ? '' : $(this).data("website");
    $("#edit_lead [name='website']").val(websiteValue);
    $("#edit_lead [name='position']").val($(this).data("position"));
    $("#edit_lead [name='edit_created_date']").val($(this).data("created-date"));
    $("#edit_lead [name='edit_service_interested']").val($(this).data("service-interested"));
    $("#edit_lead [name='source']").val($(this).data("source-id"));
    $("#edit_lead [name='status']").val($(this).data("status-id"));
    var notesValue = $(this).data("notes");
    if (notesValue.indexOf('<p>') !== -1 && notesValue.indexOf('</p>') !== -1) {
      notesValue = notesValue.replace(/<p>/g, '').replace(/<\/p>/g, '');
    }
    $("#edit_lead [name='notes']").val(notesValue);
    $("#edit_lead").modal("show");
  });

  // Add Lead Follow up 
  $("#add_follow").submit(function() {
    $("#saveLeadFollowButton").hide();
    $("#saveLeadFollowSpinner").show();
    return true;
  });

  // Edit Lead Follow up 
  $(".edit-follow-link").click(function () {
    $("#edit_follow [name='editlead']").val($(this).data("lead-id"));
    $("#edit_follow [name='edit_date_followed_up']").val($(this).data("date_followed_up"));
    $("#edit_follow [name='edit_richTextField']").val($(this).data("notes"));
  });

});


// Students
$(document).ready(function () {

  displayMessages();
  
  //Add Enquiry
  $("#addEnquiryForm").submit(function() {
    $("#saveEnquiryButton").hide();
    $("#saveEnquirySpinner").show();
    return true;
  });

  //Edit Enquiry
  $("#addenq").on("click", ".edit-enquiry-link", function () {
    var enquiryId = $(this).data("enquiry-id");
    $("#edit_enquiry [name='enquiry_id']").val(enquiryId);
    $("#edit_enquiry [name='name']").val($(this).data("name"));
    $("#edit_enquiry [name='father_name']").val($(this).data("father-name"));
    $("#edit_enquiry [name='mother_name']").val($(this).data("mother-name"));
    $("#edit_enquiry [name='email']").val($(this).data("email"));
    $("#edit_enquiry [name='contact_no']").val($(this).data("contact-no"));
    var existingGender = $(this).data("gender");
    $("#editGender").val(existingGender).change();
    $("#edit_enquiry [name='address']").val($(this).data("address"));
    $("#edit_enquiry [name='pincode']").val($(this).data("pincode"));
    $("#edit_enquiry [name='whatsapp_no']").val($(this).data("whatsapp-no"));
    var courseId = $(this).data("course-interested");
    $("#editCourse").val(courseId).change();
    var discountedFee = $(this).data("discounted-fee");
    if (discountedFee == 'None' ) {
      $("#edit_enquiry [name='discounted_fee']").val('');
    } else {
      $("#edit_enquiry [name='discounted_fee']").val(discountedFee);
    }
    $("#edit_enquiry [name='education']").val($(this).data("education"));

    var enquiryDate = $(this).data("enquiry-date");
    var formateDateExisting = moment(enquiryDate, "MMM. DD, YYYY").format("YYYY-MM-DD");
    $("#edit_enquiry [name='enquiry_date']").val(formateDateExisting);

    var dobDate = $(this).data("dob");
    var formateDOBExisting = moment(dobDate, "MMM. DD, YYYY").format("DD-MM-YYYY");
    $("#edit_enquiry [name='dob']").val(formateDOBExisting);

    $("#edit_enquiry").modal("show");
  });
  $(".view-file-button").on("click", function () {
    const existingFile = $(this).siblings("input").attr("data-existing-file");

    if (existingFile) {
      window.open(existingFile, "_blank");
    } else {
      toastr.warning("No document chosen.");
    }
  });
  $("#editEnquiryForm").submit(function() {

    var enquiryDate = $("#editDate").val();
    var formattedEnquiryDate = moment(enquiryDate, "YYYY-MM-DD").format("DD-MM-YYYY");
    $("#editDate").val(formattedEnquiryDate);

    var dobDate = $("#editDob").val();
    var formattedDobDate = moment(dobDate, "YYYY-MM-DD").format("DD-MM-YYYY");
    $("#editDob").val(formattedDobDate);

    $("#editEnquiryButton").hide();
    $("#editEnquirySpinner").show();
    return true;
  });

  //Add Admission
  $("#addStudentForm").submit(function() {
    $("#saveAdmissionButton").hide();
    $("#saveAdmissionSpinner").show();
    return true;
  });

  //Edit Admission
  $(".edit-student-link").on("click", function () {
    const enquiryId = $(this).data("enquiry-id");
    const admissionId = $(this).data("admission-id");
    const admissionFee = $(this).data("admission-fee");
    const studentPhoto = $(this).data("studentPhoto");
    const qualificationDocs = $(this).data("qualificationDocs");
    const addressDocType = $(this).data("addressDocType");
    const addressDocs = $(this).data("addressDocs");
    const admissionDate = $(this).data("admission-date");
    const dateObject = new Date(admissionDate);

    const day = ("0" + dateObject.getDate()).slice(-2);
    const month = ("0" + (dateObject.getMonth() + 1)).slice(-2);
    const year = dateObject.getFullYear();

    const formattedDate = `${day}-${month}-${year}`;

    $("#editEnquiry").val(enquiryId);
    $("#editStudentId").val(admissionId);
    $("#editAdmissionFee").val(admissionFee);
    $("#editStudentPhoto").attr("data-existing-file", studentPhoto);
    $("#editStudentPhoto")
      .siblings(".view-file-button")
      .html(studentPhoto ? "<i class='fa fa-eye'></i> View " : " View")
      .toggle(!!studentPhoto);
    $("#editQualificationDocs").attr("data-existing-file", qualificationDocs);
    $("#editQualificationDocs")
      .siblings(".view-file-button")
      .html(qualificationDocs ? "<i class='fa fa-eye'></i> View " : "View")
      .toggle(!!qualificationDocs);
    $("#editAddressDocType").val(addressDocType);
    $("#editAddressDocs").attr("data-existing-file", addressDocs);
    $("#editAddressDocs")
      .siblings(".view-file-button")
      .html(addressDocs ? "<i class='fa fa-eye'></i> View " : "View")
      .toggle(!!addressDocs);
    $("#editAdmissionDate").val(formattedDate);

    $("#editEnquiry").trigger("change");
    $("#editAddressDocType").trigger("change");
  });
  $(".view-file-button").on("click", function () {
    const existingFile = $(this).siblings("input").attr("data-existing-file");

    if (existingFile) {
      window.open(existingFile, "_blank");
    } else {
      toastr.warning("No document chosen.");
    }
  });
  $("#editStudentForm").submit(function() {
    $("#editAdmissionButton").hide();
    $("#editAdmissionSpinner").show();
    return true;
  });

  //Fee Management
  $("#addFeeManagementForm").submit(function() {
    $("#saveFeeButton").hide();
    $("#saveFeeSpinner").show();
    return true;
  });
});


// Form Validatoion
$(document).ready(function () {
  $(".name").on("input", function () {
    var errorMessage = $(this).siblings(".error-message");
    var inputValue = $(this).val();
    var regex = /[^A-Za-z\s]/;

    if (inputValue.startsWith(" ")) {
      errorMessage.hide();
      $(this).val(inputValue.trimStart());
      $(this).focus();
    } else if (/^\s/.test(inputValue) || regex.test(inputValue)) {
      errorMessage.show();
      $(this).focus();
      $(this).val(inputValue.replace(/^\s+|[^A-Za-z\s]+/g, ""));
    } else {
      errorMessage.hide();
      $(this).focus();
    }
  });

  //Email Validation Code
  $(".email").on("input", function (event) {
    var email = $(this).val();
    var validRegex =
      /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z]+)*$/;

    if (!validRegex.test(email)) {
      $(".error-msg").show();
      $(this).focus();
    } else {
      $(".error-msg").hide();
      $(this).focus();
    }
  });

  $(".email").on("keydown", function (event) {
    if (event.keyCode === 32) {
      // Check if the pressed key is the spacebar
      event.preventDefault(); // Prevent the default behavior (typing a space)
    }
  });

  //Mobile Number Validation Code
  $(".mobileno").on("input", function () {
    var errorMessageMobile = $(this).siblings(".errorMessageMobile");
    var inputValue = $(this).val();

    if (inputValue.startsWith(" ")) {
      errorMessageMobile.hide();
      $(this).val(inputValue.trimStart());
      $(this).focus();
    } else {
      var regex = /^\d{0,10}$/; // Matches exactly 10 digits

      if (!regex.test(inputValue)) {
        errorMessageMobile.show();
        $(this).focus();
        $(this).val(inputValue.replace(/\D/g, "").slice(0, 10));
      } else {
        if (inputValue.length === 10) {
          errorMessageMobile.hide();
        } else {
          errorMessageMobile.hide();
        }
        $(this).focus();
      }
    }
  });

  //Block Keybord after 10 Number
  $(".mobileno").on("keyup", function () {
    var errorMessageMobile = $(this).siblings(".errorMessageMobile");
    var inputValue = $(this).val();

    if (inputValue.length === 10) {
      errorMessageMobile.hide();
    }
  });

  //Website InputBox Validation Code
  $(".website").on("input", function (event) {
    var website = $(this).val();
    var validRegex = /^[a-zA-Z+.[a-zA-Z]*$/;

    if (website.startsWith(" ")) {
      $(this).val(website.trimStart());
      $(".error-web").hide();
      $(this).focus();
    } else {
      if (!validRegex.test(website)) {
        $(".error-web").show();
        $(this).focus();
      } else {
        $(".error-web").hide();
        $(this).focus();
      }
    }
  });

  //TextArea Limit Validation Code
  $(".limit").on("input", function () {
    var classes = $(this).attr("class").split(" ");
    var textLimitClass = classes.find((cls) => cls.startsWith("limittext"));
    var maxChars = textLimitClass
      ? parseInt(textLimitClass.replace("limittext", ""))
      : 5;
    var text = $(this).val();
    var relatedDiv = $(this).next(".charcount");
    var remainingChars = maxChars - text.length;

    var strippedText = text.replace(/(<([^>]+)>)/gi, "");

    var specialCharsOnly = /^(?=.*[A-Za-z])[^\w\s]*$/;
    var alphanumericRegex = /[A-Za-z0-9-]/;

    if (!alphanumericRegex.test(text) || specialCharsOnly.test(text)) {
      $(this).val("");
      remainingChars = maxChars;
      relatedDiv.text(remainingChars + "/" + maxChars);
      return;
    }

    if (text !== strippedText) {
      $(this).val(strippedText);
      text = strippedText;
      remainingChars = maxChars - text.length;
      relatedDiv.text(remainingChars + "/" + maxChars);
      return;
    }

    if (remainingChars < 0) {
      var trimmedText = text.slice(0, maxChars);
      $(this).val(trimmedText);
      remainingChars = 0;
    }

    relatedDiv.text(remainingChars + "/" + maxChars);
  });

  // Leave Balance
  $(document).ready(function () {
    $(".leave-balance").on("input", function () {
      var leaveInput = $(this).val().trim();
      var regex = /^(?:0|[1-9]|1[0-7])$/;

      if (!regex.test(leaveInput)) {
        $(".error-leave-message")
          .text("Please enter a valid leave balance between 0 and 17.")
          .show();
      } else {
        $(".error-leave-message").hide();
      }
    });
  });

  //Start pincode validation
  $(".pincode").on("input", function () {
    var errorMessagePincode = $(this).siblings(".errorMessagePincode");
    var inputValue = $(this).val();

    if (inputValue.startsWith(" ")) {
      errorMessagePincode.hide();
      $(this).val(inputValue.trimStart());
      $(this).focus();
    } else {
      var regex = /^\d{0,6}$/; // Matches exactly 6 digits

      if (!regex.test(inputValue)) {
        errorMessagePincode.show();
        $(this).focus();
        $(this).val(inputValue.replace(/\D/g, "").slice(0, 6));
      } else {
        if (inputValue.length === 6) {
          errorMessagePincode.hide();
        } else {
          errorMessagePincode.hide();
        }
        $(this).focus();
      }
    }
  });

  //Block Keybord after 6 Digit Pin Number
  $(".pincode").on("keyup", function () {
    var errorMessagePincode = $(this).siblings(".errorMessagePincode");
    var inputValue = $(this).val();

    if (inputValue.length === 6) {
      errorMessagePincode.hide();
    }
  });


  //Start Fee validation
  $(".feelimit").on("input", function () {
    var errorMessageFee = $(this).siblings(".errorMessageFee");
    var inputValue = $(this).val();

    if (inputValue.startsWith(" ")) {
      errorMessageFee.hide();
      $(this).val(inputValue.trimStart());
      $(this).focus();
    } else {
      var regex = /^\d{0,5}$/; // Matches exactly 6 digits

      if (!regex.test(inputValue)) {
        errorMessageFee.show();
        $(this).focus();
        $(this).val(inputValue.replace(/\D/g, "").slice(0, 5));
      } else {
        if (inputValue.length === 5) {
          errorMessageFee.hide();
        } else {
          errorMessageFee.hide();
        }
        $(this).focus();
      }
    }
  });

  //Block Keybord after 5 Digit Fee
  $(".feelimit").on("keyup", function () {
    var errorMessageFee = $(this).siblings(".errorMessageFee");
    var inputValue = $(this).val();

    if (inputValue.length === 5) {
      errorMessageFee.hide();
    }
  });



  // Max Leave
  $(document).ready(function () {
    $(".leave-category").on("input", function () {
      var leaveInput = $(this).val().trim();
      var regex = /^(?:0|[1-9]|[1-2][0-9]|30)$/;

      if (!regex.test(leaveInput)) {
        $(".error-leavecategorymessage")
          .text("Please enter a valid Max Leave between 0 and 30.")
          .show();
      } else {
        $(".error-leavecategorymessage").hide();
      }
    });
  });

  //future date not select
  $(document).ready(function () {
    $(".pastselect").datetimepicker({
      format: "YYYY-MM-DD",
    });

    // Disable future dates
    $(".pastselect").on("dp.show", function (e) {
      var today = moment();
      $(this).data("DateTimePicker").maxDate(today);
    });
  });

  //Past date not select
  $(document).ready(function () {
    $(".futureselect").datetimepicker({
      format: "YYYY-MM-DD",
    });

    // Disable Past dates
    $(".futureselect").on("dp.show", function (e) {
      var today = moment();
      $(this).data("DateTimePicker").minDate(today);
    });
  });

  //Disable Submit Button..

  $(document).ready(function () {
    var requireFieldChanged = false;  
    // Function to check if all required fields are filled
    function checkRequiredFields(form) {
      var formIsValid = true;
  
      form.find(".require[required]").each(function () {
        if (
          $(this).is(
            "input[type='text'], input[type='number'], input[type='file'], input[type='radio'], textarea"
          )
        ) {
          if ($(this).val().trim() === "") {
            formIsValid = false;
            return false;
          }
        } else if ($(this).is("select")) {
          if ($(this).val() === "---") {
            formIsValid = false;
            return false;
          }
        } else if ($(this).is(".datetimepicker")) {
          var dateValue = $(this).val();
          var isValidDate = /^\d{4}-\d{2}-\d{2}$/.test(dateValue);
  
          if (!isValidDate || dateValue.trim() === "") {
            formIsValid = false;
            return false;
          }
        }
      });
  
      return formIsValid;
    }
  
    // Trigger input change event on required fields when any modal with class 'modal-class' is loaded
    $('.modal').on('shown.bs.modal', function () {
      $(this).find(".require").trigger("change");
    });
  
    // Event listener for changes in required fields
    $(".modal").on("input change", ".require", function () {
      requireFieldChanged = true; // Set the flag to true whenever a required field is changed
  
      var form = $(this).closest(".disable-button");
      var submitButton = form.find(".savebutton");
  
      // Check if all required fields are filled or if no required field has been changed
      var formIsValid = checkRequiredFields(form) || !requireFieldChanged;
  
      // Enable submit button if form is valid
      submitButton.prop("disabled", !formIsValid);
    });
  
    // Event listener for form submission
    $(".modal").on("submit", ".disable-button", function (e) {
      var submitButton = $(this).find(".savebutton");
  
      if (submitButton.prop("disabled")) {
        e.preventDefault();
        // alert("Please fill in all required fields!");
      }
    });
  });
  
  

//Plz Do Not Delete This Code When Ever Testing Is Not Doen.

  // $(document).ready(function () {
  //   $(".require").on("input change", function () {
  //     var form = $(this).closest(".disable-button");
  //     var submitButton = form.find(".savebutton");
  //     var formIsValid = true;

  //     form.find(".require[required]").each(function () {
  //       if (
  //         $(this).is(
  //           "input[type='text'], input[type='number'], input[type='file'], input[type='radio'], textarea"
  //         )
  //       ) {
  //         if ($(this).val().trim() === "") {
  //           formIsValid = false;
  //           return false;
  //         }
  //       } else if ($(this).is("select")) {
  //         if ($(this).val() === "---") {
  //           formIsValid = false;
  //           return false;
  //         }
  //       } else if ($(this).is(".datetimepicker")) {
  //         var dateValue = $(this).val();
  //         var isValidDate = /^\d{4}-\d{2}-\d{2}$/.test(dateValue);

  //         if (!isValidDate || dateValue.trim() === "") {
  //           formIsValid = false;
  //           return false;
  //         }
  //       }
  //     });

  //     if (formIsValid) {
  //       submitButton.prop("disabled", false);
  //     } else {
  //       submitButton.prop("disabled", true);
  //     }
  //   });

  //   $(".disable-button").submit(function (e) {
  //     var submitButton = $(this).find(".savebutton");

  //     if (submitButton.prop("disabled")) {
  //       e.preventDefault();
  //       // alert("Please fill in all required fields!");
  //     }
  //   });
  // });






  //Commune Selector Search Option
  $(document).ready(function () {
    $(".searchoption").select2({ elementWidth: "100%" });
  });

  //Search Option For Admin Dashboard 
  $(document).ready(function () {
    const selectDropdowns = [
      { id: "#dashselect2", className: ".dashleavetype" },
      { id: "#dashselect2", className: ".dashAssignAss" },
      { id: "#dashallemp", className: "dashallleave" },
    ];

    selectDropdowns.forEach((dropdown) => {
      if ($(dropdown.id).length) {
        $(dropdown.className).select2({
          dropdownParent: $(dropdown.id),
        });
      }
    });
  });



  //Search Option For Profile Page Information 
  $(document).ready(function () {
    const selectDropdowns = [
      { id: "#profile_info", className: ".profile-info-report" },
      { id: "#personal_info_modal", className: ".personalinfomarital" },
      { id: "#add_emergency_modal", className: ".contact_type" },
      { id: "#emergency_contact_modal", className: ".edit_contact_type" },
    ];

    selectDropdowns.forEach((dropdown) => {
      if ($(dropdown.id).length) {
        $(dropdown.className).select2({
          dropdownParent: $(dropdown.id),
        });
      }
    });
  });



  //Search Selector Option For Lead Models
  $(document).ready(function () {
    const selectDropdowns = [
      { id: "#add_lead", className: ".modelsearchoption" },
      { id: "#edit_lead", className: ".editleadservice" },
      { id: "#edit_lead", className: ".editleadsource" },
      { id: "#edit_lead", className: ".editleadstatus" },
      { id: "#add_follow", className: ".add_followearchoption" },
      { id: "#edit_follow", className: ".edit_followearchoption" },
    ];

    selectDropdowns.forEach((dropdown) => {
      if ($(dropdown.id).length) {
        $(dropdown.className).select2({
          dropdownParent: $(dropdown.id),
        });
      }
    });
  });

  //Search Select form For Student Models
  $(document).ready(function () {
    if ($("#add_students").length) {
      $(".studentenquiry").select2({
        dropdownParent: $("#add_students"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_students").length) {
      $(".addreshdoc").select2({
        dropdownParent: $("#add_students"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#edit_students").length) {
      $(".editaddreshdoc").select2({
        dropdownParent: $("#edit_students"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_enquiry").length) {
      $(".addgender").select2({
        dropdownParent: $("#add_enquiry"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_enquiry").length) {
      $(".addcourse").select2({
        dropdownParent: $("#add_enquiry"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#edit_enquiry").length) {
      $(".editgender").select2({
        dropdownParent: $("#edit_enquiry"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#edit_enquiry").length) {
      $(".editcourse").select2({
        dropdownParent: $("#edit_enquiry"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_fee_management").length) {
      $(".addfee").select2({
        dropdownParent: $("#add_fee_management"),
      });
    }
  });

  //Search Select form For Add Policy Model
  $(document).ready(function () {
    if ($("#add_policy").length) {
      $(".addcatagory").select2({
        dropdownParent: $("#add_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_policy").length) {
      $(".approveedby").select2({
        dropdownParent: $("#add_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_user_nda").length) {
      $(".userndacategory").select2({
        dropdownParent: $("#add_user_nda"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_user_nda").length) {
      $(".ndaapproveedby").select2({
        dropdownParent: $("#add_user_nda"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_hr_policy").length) {
      $(".hrcatagory").select2({
        dropdownParent: $("#add_hr_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_hr_policy").length) {
      $(".hrapproved").select2({
        dropdownParent: $("#add_hr_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#update_policy").length) {
      $(".hrupdat").select2({
        dropdownParent: $("#update_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#update_policy").length) {
      $(".hrapprovedby").select2({
        dropdownParent: $("#update_policy"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_manage_employee_bond").length) {
      $(".empbond").select2({
        dropdownParent: $("#add_manage_employee_bond"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_manage_employee_bond").length) {
      $(".empbondapprov").select2({
        dropdownParent: $("#add_manage_employee_bond"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#update_manage_employee_bond").length) {
      $(".updateempbondname").select2({
        dropdownParent: $("#update_manage_employee_bond"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#update_manage_employee_bond").length) {
      $(".updateempbondapprove").select2({
        dropdownParent: $("#update_manage_employee_bond"),
      });
    }
  });

  //Search Select form For Add Leave Models
  $(document).ready(function () {
    if ($("#add_leaves").length) {
      $(".addleaveemp").select2({
        dropdownParent: $("#add_leaves"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_leaves").length) {
      $(".addleavetyp").select2({
        dropdownParent: $("#add_leaves"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_leaves").length) {
      $(".leav_st").select2({
        dropdownParent: $("#add_leaves"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#add_leaves").length) {
      $(".addtype").select2({
        dropdownParent: $("#add_leaves"),
      });
    }
  });

  $(document).ready(function () {
    if ($("#approve_leave").length) {
      $(".approvestatus").select2({
        dropdownParent: $("#approve_leave"),
      });
    }
  });

  //Select form For Performance Models

  $(document).ready(function () {
    if ($("#add_performance").length) {
      $(".selectperformemp").select2({
        dropdownParent: $("#add_performance"),
      });
    }
  });


  //Max & Min Validation
  //For Top Manage Rating Performance
  $(document).ready(function () {
    var timer; // Variable to store timer ID

    function performValidation() {
      var maxVal = parseInt($(".maxTopNumber").val());
      var minVal = parseInt($(".minTopNumber").val());
      var errorTop = $(".errorTop");
      if (!isNaN(minVal) && !isNaN(maxVal) && maxVal <= minVal) {
        errorTop.show();
        $(".maxTopNumber").val("");
      } else {
        errorTop.hide();
      }
    }

    function triggerValidation() {
      clearTimeout(timer); // Clear the previous timer
      timer = setTimeout(performValidation, 1000); // Set a new timer for 1 second
    }

    $(".updateTopButton").on("click", function () {
      triggerValidation();
    });

    $(".maxTopNumber, .minTopNumber").on("keypress", function (event) {
      var charCode = event.which ? event.which : event.keyCode;
      if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
      }
      triggerValidation();
      return true;
    });

    // Event listener for input finish in number fields
    $(".maxTopNumber, .minTopNumber").on("input", function () {
      clearTimeout(timer); // Clear the previous timer
      setTimeout(performValidation, 1000); // Trigger validation immediately after input
    });
  });

  // Event listener for input finish in number fields
  $(".maxTopNumber, .minTopNumber").on("input", function () {
    clearTimeout(timer); // Clear the previous timer
    setTimeout(performValidation, 1000); // Trigger validation immediately after input
  });

  //For Average Rating Performance
  $(document).ready(function () {
    var timer; // Variable to store timer ID

    function performValidation() {
      var maxVal = parseInt($(".maxAvgNumber").val());
      var minVal = parseInt($(".minAvgNumber").val());
      var errorAvg = $(".errorAvg");
      if (!isNaN(minVal) && !isNaN(maxVal) && maxVal <= minVal) {
        errorAvg.show();
        $(".maxAvgNumber").val("");
      } else {
        errorAvg.hide();
      }
    }

    function triggerValidation() {
      clearTimeout(timer); // Clear the previous timer
      timer = setTimeout(performValidation, 1000); // Set a new timer for 1 second
    }

    $(".updateAvgButton").on("click", function () {
      triggerValidation();
    });

    $(".maxAvgNumber, .minAvgNumber").on("keypress", function (event) {
      var charCode = event.which ? event.which : event.keyCode;
      if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
      }
      triggerValidation();
      return true;
    });

    // Event listener for input finish in number fields
    $(".maxAvgNumber, .minAvgNumber").on("input", function () {
      clearTimeout(timer); // Clear the previous timer
      setTimeout(performValidation, 1000); // Trigger validation immediately after input
    });
  });

  $(".maxAvgNumber, .minAvgNumber").on("keypress", function (event) {
    var charCode = event.which ? event.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      return false;
    }
    triggerValidation();
    return true;
  });

  // Event listener for input finish in number fields
  $(".maxAvgNumber, .minAvgNumber").on("input", function () {
    clearTimeout(timer); // Clear the previous timer
    setTimeout(performValidation, 1000); // Trigger validation immediately after input
  });

  //Bottom Performance
  $(document).ready(function () {
    var timer; // Variable to store timer ID

    function performValidation() {
      var maxVal = parseInt($(".maxBotNumber").val());
      var minVal = parseInt($(".minBotNumber").val());
      var errorBot = $(".errorBot");
      if (!isNaN(minVal) && !isNaN(maxVal) && maxVal <= minVal) {
        errorBot.show();
        $(".maxBotNumber").val("");
      } else {
        errorBot.hide();
      }
    }

    function triggerValidation() {
      clearTimeout(timer);
      timer = setTimeout(performValidation, 1000);
    }

    $(".updateBotButton").on("click", function () {
      triggerValidation();
    });

    $(".maxBotNumber, .minBotNumber").on("keypress", function (event) {
      var charCode = event.which ? event.which : event.keyCode;
      if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
      }
      triggerValidation();
      return true;
    });

    $(".maxBotNumber, .minBotNumber").on("input", function () {
      clearTimeout(timer);
      setTimeout(performValidation, 1000);
    });
  });

  //Star Ratting..
  $(document).ready(function () {
    $('.star').on('input', function (e) {
      var inputValue = $(this).val();
      var regex = /^[0-5]$/;

      if (!regex.test(inputValue)) {
        $(this).val('');
      }
    });
  });


});


// Fee Detail Modal
$("#feeDetailModal").on("show.bs.modal", function (event) {
  const link = $(event.relatedTarget);
  const admissionName = link.data("admission-name");
  const courseName = link.data("course-name");
  const totalPaid = link.data("total-paid");
  const totalDue = link.data("total-due");
  const feeEntries = link.data("fee-entries");

  const data = feeEntries.replace(/'/g, '"');
  const feeEntriesData = JSON.parse(data);

  const modalTitle = document.getElementById("admissionDetailsModalLabel");
  const totalPaidElement = document.getElementById("totalPaid");
  const totalDueElement = document.getElementById("totalDue");
  const tableBody = document.getElementById("feeDetailTableBody");

  modalTitle.innerHTML = `<div class="text-center">${admissionName}</div><div class="text-center">${courseName}</div>`;
  totalPaidElement.innerText = `${totalPaid}`;
  totalDueElement.innerHTML = `<h5>${totalDue}</h5>`;

  tableBody.innerHTML = "";

  if (Array.isArray(feeEntriesData)) {
    feeEntriesData.forEach((entry) => {
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td>${entry.paid_fee}</td>
        <td>${entry.fee_paid_date}</td>
      `;
      tableBody.appendChild(newRow);
    });
  } else {
    console.error("Invalid fee entries data:", feeEntriesData);
  }
});


// Callback function to execute when an element comes into view
function onIntersection(entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      let img = entry.target;
      let src = img.getAttribute("data-src");
      if (src) {
        img.src = src;
        img.removeAttribute("data-src");
      }
    }
  });
}

// Find all images with 'data-src' attribute
let images = document.querySelectorAll("img[data-src]");

// Create an Intersection Observer instance
let observer = new IntersectionObserver(onIntersection);

// Start observing each image
images.forEach((img) => {
  observer.observe(img);
});

function admissionFilter() {
  const selectedStudent = document.getElementById("selectStudent").value;
  const dateRange = document.getElementById("dateRangeSelect").value;
  const currentUrl = window.location.href;
  const url = new URL(currentUrl);
  if (selectedStudent) {
    url.searchParams.set("select_student", selectedStudent);
  } else {
    url.searchParams.delete("select_student");
  }

  if (dateRange) {
    url.searchParams.set("date_range", dateRange);
  } else {
    url.searchParams.delete("date_range");
  }
  window.location.href = url.toString();
}

function enquiryFilter() {
  const selectedStudent = document.getElementById("selectStudent").value;
  const selectedCourse = document.getElementById("selectCourse").value;
  const currentUrl = window.location.href;
  const url = new URL(currentUrl);
  if (selectedStudent) {
    url.searchParams.set("select_student", selectedStudent);
  } else {
    url.searchParams.delete("select_student");
  }

  if (selectedCourse) {
    url.searchParams.set("select_course", selectedCourse);
  } else {
    url.searchParams.delete("select_course");
  }
  window.location.href = url.toString();
}

//Leaves 
$(document).ready(function () {

  displayMessages();

  //Approve Leave
  $("#leaveTable").on("click", ".approve-leave", function () {
    var leaveId = $(this).data("leave-id");
    $("#approve_leave [name='leave_id']").val(leaveId);

    var employeeFirstName = $(this).data("employee-first-name");
    var employeeLastName = $(this).data("employee-last-name");
    var employeeUsername = $(this).data("employee-username");
    var employeeName = employeeFirstName ? `${employeeFirstName} ${employeeLastName}` : employeeUsername;
    $("#approve_leave [name='employee_names']").val(employeeName);
    $("#approve_leave [name='employee_name']").val(employeeUsername);
    $("#approve_leave [name='leave_type']").val($(this).data("leave-type"));
    $("#approve_leave [name='reason_value']").val($(this).data("reason"));
    $("#approve_leave [name='no_of_days']").val($(this).data("total"));
    $("#approve_leave [name='type']").val($(this).data("type"));
    $("#approve_leave [name='requested_date']").val($(this).data("requested-date"));
    var leaveStatus = $(this).data("leave-status");
    $("#leaveStatus").val(leaveStatus);
    $("#reasonText").text($(this).data("reason"));
    const notesValue = $(this).data("notes");
    $("#notes").text(notesValue === "None" ? '' : notesValue);
    const fromDate = new Date($(this).data("start-from") + ' UTC');
    const formattedFromDate = fromDate.toISOString().split("T")[0];
    const toDate = new Date($(this).data("end-to") + ' UTC');
    const formattedToDate = toDate.toISOString().split("T")[0];
    $("#approve_leave [name='from_date']").val(formattedFromDate);
    $("#approve_leave [name='to_date']").val(formattedToDate);
    var startDateHalf = $(this).data("start-half");
    var endDateHalf = $(this).data("end-half");
    var isStartChecked = startDateHalf === "True"
    var isEndChecked = endDateHalf === "True"
    $("#approve_leave [name='edit_half_day_start']").prop("checked", isStartChecked);
    $("#approve_leave [name='edit_half_day_end']").prop("checked", isEndChecked);
    $("#approve_leave").modal("show");
  });
  $("#approveForm").submit(function() {
    $("#approveLeaveButton").hide();
    $("#approveLeaveSpinner").show();
    return true;
  });
  
  //Add Leave
  $("#addLeaveForm").submit(function() {
    $("#saveLeaveButton").hide();
    $("#saveLeaveSpinner").show();
    return true;
  });
});


// Profile Page Informations
$(document).ready(function () {

  displayMessages();
  
  //Add Emergency Contact
  $("#addEmergencyContactForm").submit(function() {
    $("#addEmergencyButton").hide();
    $("#addEmergencySpinner").show();
    return true;
  });

  //Edit Emergency Contact
  $("#emergencyContactForm").submit(function() {
    $("#updateEmergencyButton").hide();
    $("#updateEmergencySpinner").show();
    return true;
  });

  //Add Education Information
  $("#addEducationForm").submit(function() {
    $("#addEducationButton").hide();
    $("#addEducationSpinner").show();
    return true;
  });

  //Edit Education Information
  $("#educationForm").submit(function() {
    $("#updateEducationButton").hide();
    $("#updateEducationSpinner").show();
    return true;
  });

  //Add Experience Information
  $("#addExperienceForm").submit(function() {
    $("#addExperienceButton").hide();
    $("#addExperienceSpinner").show();
    return true;
  });

  //Edit Experience Information
  $("#experienceForm").submit(function() {
    $("#updateExperienceButton").hide();
    $("#updateExperienceSpinner").show();
    return true;
  });

  //Add Family Information
  $("#addFamilyForm").submit(function() {
    $("#addFamilyButton").hide();
    $("#addFamilySpinner").show();
    return true;
  });

  //Edit Family Information
  $(".edit-family-data").on("click", function () {
    var familyId = $(this).data("family-id");
    var name = $(this).data("name");
    var relation = $(this).data("relation");
    var phone = $(this).data("phone-number");
    const dateOfBirth = $(this).data("birth-date");
    const dateObject = new Date(dateOfBirth);

    const day = ("0" + dateObject.getDate()).slice(-2);
    const month = ("0" + (dateObject.getMonth() + 1)).slice(-2);
    const year = dateObject.getFullYear();

    const formattedDate = isNaN(dateObject) ? '' : `${day}-${month}-${year}`;

    $("#family_info_modal #editFamilyDetail").val(familyId);
    $('#family_info_modal input[name="name"]').val(name);
    $('#family_info_modal input[name="relation"]').val(relation);
    $('#family_info_modal input[name="dob"]').val(formattedDate);
    $('#family_info_modal input[name="phone"]').val(phone);
    $("#family_info_modal").modal("show");
  });
  $("#family_info_modal").submit(function() {
    $("#saveFamilyButton").hide();
    $("#saveFamilySpinner").show();
    return true;
  });

  //Update Profile
  $(".edit-profile-link").on("click", function () {
    const photo = $(this).data("photo");
    $("#editPhoto").attr("data-existing-file", photo);
    $("#editPhoto")
    .siblings(".view-file-button")
    .html(photo ? "<i class='fa fa-eye'></i> View " : " View")
    .toggle(!!photo);
  });
  $(".view-file-button").on("click", function () {
    const existingFile = $(this).siblings("input").attr("data-existing-file");

    if (existingFile) {
      window.open(existingFile, "_blank");
    } else {
      toastr.warning("No document chosen.");
    }
  });
  $("#profileForm").submit(function() {
    $("#saveProfileButton").hide();
    $("#saveProfileSpinner").show();
    return true;
  });

  //Update Personal Information
  $("#personal_info_form").submit(function() {
    $("#savePersonalInfoButton").hide();
    $("#savePersonalInfoSpinner").show();
    return true;
  });

  //Update Bank Information
  $("#bank_form").submit(function() {
    $("#saveBankButton").hide();
    $("#saveBankSpinner").show();
    return true;
  });

  // Profile Assets Informaiton
  $(".assets-modal").on("click", function () {
    const name = $(this).data("name");
    const conditionType = $(this).data("condition-type");
    const assetType = $(this).data("asset-type");
    const cost = $(this).data("cost");
    const assignId = $(this).data("assign-id");
    const serialNumber = $(this).data("serial-number");
    const assignBy = $(this).data("assign-by");
    const assignDate = $(this).data("assign-date");

    const assignIdValue = assignId !== 'None' ? assignId : '';
    const serialValue = serialNumber !== 'None' ? serialNumber : ''
    const assignByValue = assignBy !== 'None' ? assignBy : '';
    const assignDateValue = assignDate !== 'None' ? assignDate : ''

    $("#editAssetName").val(name);
    $("#editCondition").val(conditionType);
    $("#editAssetType").val(assetType);
    $("#editCost").val(cost);
    $("#editAssignId").val(assignIdValue);
    $("#editSerial").val(serialValue);
    $("#editAssignedBy").val(assignByValue);
    $("#editAssignedDate").val(assignDateValue);
  });
});


// Performance view
$(document).ready(function () {

  displayMessages();
  $("#addPerformanceForm").submit(function() {
    $("#savePerformanceButton").hide();
    $("#savePerformanceSpinner").show();
    return true;
  });
});