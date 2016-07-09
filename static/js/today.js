function setPageHeight() {
	// load page with proper height
	$(body).css("min-height", document.body.scrollHeight);
}

window.onload = function() {
	setPageHeight();
}