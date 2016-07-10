/*
function setPageHeight() {
	// load page with proper height
	$(body).css("min-height", document.body.scrollHeight);
}
 */

function hideSide() {
	weight = $("#nav-mobile").css("width");
	$("#nav-mobile").css("transform", "translateX(-" + weight + ")");
	$("header").css("padding-left", "0px");
	$("main").css("padding-left", "0px");
}

function showSide() {
	$("#nav-mobile").css("transform", "translateX(0%)");
	$("header").css("padding-left", "240px");
	$("main").css("padding-left", "200px");
}

window.onload = function() {
	$("#side-nav-show").onclick = function() {
		$("#nav-mobile").css("transform", "translateX(0%)");
	};
}