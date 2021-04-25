var API_URL = "https://i645of8oc3.execute-api.us-east-2.amazonaws.com/Beta/customers";


//switch case for customer view
$('select[name="form-change"]').on('change', function () {
    const switchForms = $(this).val();
    switch (switchForms) {
        case 'Add':
            $('.addCall').show();
            $('.statusCall').hide();
            $('.locationsCall').hide();
            break;
        case 'Track':
            $('.addCall').hide();
            $('.statusCall').show();
            $('.locationsCall').hide();
            break;
        case 'Office':
            $('.addCall').hide();
            $('.statusCall').hide();
            $('.locationsCall').show();
            break;
    }
});

//switch case for employee view
$('select[name="form-change"]').on('change', function () {
    const switchForms = $(this).val();
    switch (switchForms) {
        case 'viewPkgLocations':
            $('.viewPkgLocationsCall').show();
            $('.killEmployeeCall').hide();
            break;
        case 'delete':
            $('.viewPkgLocationsCall').hide();
            $('.killEmployeeCall').show();
            break;
    }
});

$("#customer-form").on("submit", function (e) {
    $.ajax({
        type: 'POST',
        url: API_URL,
        data: $("#customer-form").serialize(),
        datatype: 'json',
        success: function (data) {
            alert($("#customer-form").serialize());
        }
    });
    e.preventDefault();
});