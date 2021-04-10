$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#customer_name").val(res.name);
        $("#customer_address").val(res.address);
        $("#customer_phone_number").val(res.phone_number);
        $("#customer_email").val(res.email);
        $("#customer_credit_card").val(res.credit_card);
        if (res.active == true) {
            $("#customer_active").val("true");
        } else {
            $("#customer_active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_name").val("");
        $("#customer_address").val("");
        $("#customer_phone_number").val("");
        $("#customer_email").val("");
        $("#customer_credit_card").val("");
        $("#customer_active").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#customer_name").val();
        var address = $("#customer_address").val();
        var phone_number = $("#customer_phone_number").val();
        var email = $("#customer_email").val();
        var credit_card = $("#customer_credit_card").val();
        var active = $("#customer_active").val() == "true";

        var data = {
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "credit_card": credit_card,
            "active": active
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var name = $("#customer_name").val();
        var address = $("#customer_address").val();
        var phone_number = $("#customer_phone_number").val();
        var email = $("#customer_email").val();
        var credit_card = $("#customer_credit_card").val();
        var active = $("#customer_active").val() == "true";
     
        

        var data = {
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "credit_card": credit_card,
            "active": active
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data()
    });

})