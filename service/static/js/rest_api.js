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
            url: "/customers/" + customer_id + "/deactivate",
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

    // ****************************************
    // Deactivate a Customer
    // ****************************************

    $("#deactivate-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/deactivate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            // console.log(res)
            update_form_data(res)
            flash_message("Customer deactivated.")
            show_in_search_results_by_customer_id()
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Activate a Customer
    // ****************************************

    $("#activate-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/activate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Customer activated.")
            show_in_search_results_by_customer_id()
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });




    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#customer_name").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:10%">Phone Number</th>'
            header += '<th style="width:10%">Email</th>'
            header += '<th style="width:10%">Credit Card</th>'
            $("#search_results").append(header);
            var firstCustomer = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var row = "<tr><td>"+customer.id+"</td><td>"+customer.name+"</td><td>"+customer.address+"</td><td>"+customer.phone_number+"</td><td>"+customer.email+"</td><td>"+customer.credit_card+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCustomer = customer;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    })
})