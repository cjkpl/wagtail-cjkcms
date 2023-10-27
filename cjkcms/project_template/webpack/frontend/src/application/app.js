// This is the scss entry file
import "../styles/index.scss";

// We can import Bootstrap JS instead of the CDN link, if you do not use
// Bootstrap, please feel free to remove it.
// import "bootstrap/dist/js/bootstrap.bundle";

// If you prefer to use MDBootstrap, please uncomment the following line, 
// and comment out the line above.
import * as mdb from 'mdb-ui-kit';
window.mdb = mdb;

// We can import other JS file as we like
import "../components/sidebar";

window.document.addEventListener("DOMContentLoaded", function () {
  window.console.log("dom ready 1");
});
