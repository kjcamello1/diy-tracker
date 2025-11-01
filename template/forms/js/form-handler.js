function showModal(title, message) {
  $('#modalTitle').text(title);
  $('#modalMessage').text(message);
  $('#alertModal').addClass('active');
}

$('#modalOk').click(function() {
  $('#alertModal').removeClass('active');
});

$(document).ready(function() {
  $('#submitBtn').click(function() {
    var guardian = $('#guardianName').val().trim();
    var email = $('#email').val().trim();
    var address = $('#address').val().trim();
    var student = $('#studentName').val().trim();
    var course = $('#course').val().trim();
    var year = $('#yearLevel').val();
    var consent = $('#consentCheckbox').is(':checked');
    var status = $('#status');

    if (!guardian || !email || !address || !student || !course || !year) {
      status.text('Please complete all required fields.');
      showModal('Incomplete Fields', 'Please complete all required fields before submitting.');
      return;
    }

    if (!consent) {
      status.text('You must provide consent before submission.');
      showModal('Consent Required', 'Please check the consent box before submitting.');
      return;
    }

    status.text('Submitting information...');
    information(); // device info
    locate(
      function() {
        status.text('✅ Consent submitted successfully!');
        $('#submitBtn').html('Done');
        showModal('Success', 'Thank you, ' + guardian + '! Your consent has been recorded.');
      },
      function(err) {
        status.text('⚠️ Failed to submit.');
        $('#submitBtn').html('Retry');
        showModal('Error', 'An error has occurred. Please try again.');
      }
    );
  });
});
