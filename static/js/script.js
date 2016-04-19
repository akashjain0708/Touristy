// Write any custom javascript functions here
function touristyLink() {
  if(localStorage.getItem("UID")!= null) {
	window.location = "#/list";
  }
  else
  	window.location = "#/home";
}