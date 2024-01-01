function cssLoaded() {
    console.log("CSS loaded successfully.");
  }
  
  function cssFallback() {
    var cssLink = document.createElement("link");
    cssLink.type = "text/css";
    cssLink.rel = "stylesheet";
    cssLink.href = css_fallback_url; // We'll define this variable in HTML
    document.head.appendChild(cssLink);
    console.log("Falling back to local CSS.");
  }
  
  function jsLoaded() {
    console.log("JS loaded successfully.");
  }
  
  function jsFallback() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = js_fallback_url; // We'll define this variable in HTML
    document.body.appendChild(script);
    console.log("Falling back to local JS.");
  }
  