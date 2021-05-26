(function($) {
  	"use strict"; // Start of use strict

  	var server_url = "http://127.0.0.1:8000/";

  	var start_at=""; 
  	var end_at = "";

  	//===========================================
  	function getGetDataFromAPI(url, callback){
        var _url = server_url + url;
        var settings = {
            "url": _url,
            "method": "GET",
            "timeout": 0,            
        };

        $.ajax(settings).done(function (response) {            
            callback(response);
        }).fail(function(response){
            //callback("[]");            
        });
    }

    function block_ui(){
        
        $.blockUI({ css: { 
            border: 'none', 
            padding: '15px', 
            backgroundColor: '#000', 
            '-webkit-border-radius': '10px', 
            '-moz-border-radius': '10px', 
            opacity: .5, 
            color: '#fff'
        } }); 
        
    }

    function unblock_ui(){
        $.unblockUI();
    }

    //================================================
  	$('#visit_daterangepicker').daterangepicker({}, function (start, end) {
        $("#visit_daterangepicker .form-control").val(start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD"));
        start_at = start.format("YYYY-MM-DD");
        end_at = end.format("YYYY-MM-DD");
        update_page();
    });

    $("#generate_btn").on("click", function(a){ 
    	var url = "generate_data";
    	block_ui();
    	getGetDataFromAPI(url, function(response){
  			update_page();
  		});

    });

    block_ui();
  	update_page();

  	function update_page(){  		
  		var url = "visit_table_data?start_at=" + start_at + "&end_at=" + end_at;

  		getGetDataFromAPI(url, function(response){
  			console.log(response);

  			var html = "";

  			var rows = response.data[0].length;

  			for(var i=0;i<rows;i++){
  				html = html + "<tr>";
  				for(var j=0; j<7; j++){
  					var dogs = " dogs";
  					if(response.data[j][i].title == "")
  						dogs = ""
  					var td = '<td><div class="visit-cell" data-date="' + response.data[j][i].date + '"><div class="cell-title">' + response.data[j][i].title + '</div><div class="cell-cc">' + response.data[j][i].cc + dogs + '</div></div></td>';
  					html = html + td;
  				}
  				html = html + "</tr>"
  			}

  			$("#visit_table tbody").html(html);
  			unblock_ui();
  		});
  	}
	
  	$(document).on('click', ".visit-cell", function(e){
  		var target = $(e.currentTarget);     
  		var date = target.data("date");

  		var url = "check_visit_date?date=" + date;
  		block_ui();
  		getGetDataFromAPI(url, function(response){
  			$("#check_visit_date_modal h4").html("Dog list in house at " + date);

  			var html = "";

  			var rows = response.data.length;

  			for(var i=0;i<rows;i++){
  				html = html + "<tr>";
  				
  				var td0 = '<td><div class="check-dog-name">' + response.data[i].dog + '</div></td>';
  				var td1 = '<td><div class="check-start">' + response.data[i].start_at + '</div></td>';
  				var td2 = '<td><div class="check-end">' + response.data[i].end_at + '</div></td>';

  				html = html + td0 + td1 + td2 +"</tr>";
  			}

  			$("#visit_check_date_table tbody").html(html);

  			$("#check_visit_date_modal").modal("show"); 
  			unblock_ui();
  		});
  	});

 
})(jQuery); // End of use strict