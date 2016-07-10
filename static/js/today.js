function setPageHeight() {
	$(body).css("min-height", window.screen.height);
}

window.onload = function() {
	//alert("ok");
	setPageHeight();
}