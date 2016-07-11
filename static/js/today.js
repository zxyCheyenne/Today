/*
function setPageHeight() {
	// load page with proper height
	$(body).css("min-height", document.body.scrollHeight);
}
 */

var show = 0;

function showSide() {
	if (show == 1) {
		$("#nav-mobile").css("transform", "translateX(0%)");
		$("header").css("padding-left", "240px");
		$("main").css("padding-left", "200px");
		show = 0;
	} else {
		weight = $("#nav-mobile").css("width");
		$("#nav-mobile").css("transform", "translateX(-" + weight + ")");
		$("header").css("padding-left", "0px");
		$("main").css("padding-left", "0px");
		show = 1;
	}
}

function showSearch() {
    $("#search").css("margin-left", "15px");
}

function hideSearch() {
	$("#search").css("margin-left", "-" + $("#search").css("width"));
}

window.onload = function() {
	hideSearch();
};