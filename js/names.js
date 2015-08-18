$('#loading').show();
var divError = document.getElementById('output-result');
var fade_out = function() {
  $("#output-result").fadeOut();
};
var errotMsgLatency = 3000;
var _columnsResultTable = [];

function initResultTableHeader() {
    _columnsResultTable = [];
    _columnsResultTable.push({"title": "Name", "Sortable": "False"}); //1
    _columnsResultTable.push({"title": "Matching Score (%)", "Sortable": "False"}); //2
}

function initInventoryTable(points) {

	resultTable = $('#result-table').DataTable({
			"autoWidth":true,
			"data":points,
			"columns":_columnsResultTable,
			"scrollY":"205px",
			"scrollX":true,
			"dom":"frtiS",
			"deferRender":true,
			"paging":false,
            "filter": false,
            "info": false,
            "targets"  : 'no-sort',
            "orderable": false,
            "order": [[ 1, 'desc' ]]
		});
}

function setData(data) {
    var points = [];
    for (nm in data) {
            addToResultTable([ucFirstAllWords(decode_utf8(nm)), (data[nm]*100).toFixed(1)]);
    }
}

function addToResultTable(p) {
    resultTable.row.add(p).draw();
}

var resultTable = null;
function clearResultTable() {
    // resultTable.rows().remove().draw();
    if (resultTable !== null && resultTable !== undefined) {
        resultTable.destroy();
    }
}

function startMatching() { 
    var name_query = $('#query-name').val();
    console.log('Matching '+name_query)
    $.ajax({
        url: "/query/",
        data: 'name='+name_query, //{'query': name_query},
        success: function(response) { 
            $('#loading').hide();
            $('#table-panel').removeClass('hidden');
            clearResultTable();
            console.log(response);
            initResultTableHeader();
            initInventoryTable([]);
            setData(JSON.parse(JSON.stringify(eval('('+response+')'))));
        },
        error : function () {
            $('#loading').hide();
            divError.innerHTML = '<dir class="alert alert-danger" role="alert">Error retrieving data.</div>';
            $("#output-result").show();
            setTimeout(fade_out, errotMsgLatency);
        }
    });
}

function decode_utf8(s) {
    return decodeURIComponent(escape(s));
}

function ucFirstAllWords( str )
{
    var pieces = str.split(' ');
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1);
    }
    return pieces.join(' ');
}