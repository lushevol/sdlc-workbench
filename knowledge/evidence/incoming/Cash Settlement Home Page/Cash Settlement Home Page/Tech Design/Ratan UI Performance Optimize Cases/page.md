# Loading Config JSON Synchronously

*12/6/2022*

## 1) Description

- Place: entrance of each Application HTML <header>
- For example: - URL: [https://ratan-cashflow.uk.dev.net:8453/cashflow.html?workspaceId=80247220159124&time=1670291226267](https://ratan-cashflow.uk.dev.net:8453/cashflow.html?workspaceId=80247220159124&time=1670291226267) - Code at line 28
- Influence: - Block ”main.js“ execute - Loading in a queue and all request durations are summed （200+ms * n） ![Annotation 2022-12-06 102508.jpg](attachments/Annotation 2022-12-06 102508.jpg)

## 2）Current Code Block

```js
<!DOCTYPE html><html lang="en"><head>
    <!-- Line 28 Start -->
    <script>
      function queryJson(n) {						 		// add callback at second param
        const e = new XMLHttpRequest();
        return (
          e.open("GET", `/${n}.json`, !1),					 // change to async
          e.setRequestHeader("If-Modified-Since", "0"),
          e.send(null),
          JSON.parse(e.responseText)
        );
      }
      {
        const n = queryJson("ratanConfig"),					// construct in callback function 
          e = {
            ...queryJson("cashflowDetailsConfig"),
            ...queryJson("tradeDetailsConfig"),
            ...queryJson("tradesConfig"),
            ...queryJson("exceptionConfig"),
            ...queryJson("cashflowConfig"),
            ...n,
          }; 
        (window.ratanConfig = {}),
          Object.keys(e).forEach(function (n) {				
            Object.defineProperty(window.ratanConfig, n, {  // can also freeze the object in callback 
              get: function () {
                return e[n];
              },
              set: function () {
                console.log("Can not be modified!");
              },
            });
          });
      }
    </script>
    <script defer="defer" src="/static/js/main.b251edd2.js"></script>  <!--Move main.js after root-div->
    <link href="/static/css/main.53081a22.css" rel="stylesheet" /></head>
 	<body><noscript>You need to enable JavaScript to run this app.</noscript>
    	<div id="root"></div>
  <!-- Line 28 end-->
</body></html>
```

**Line 8：XMLHTTPRequest.open**

> Refer：[https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/open](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/open)

**Line36: Script Tag of main.js **

Place to the behind of "root div container"

## 3) Solution

JSON Config

- Change to async, fire all request with a callback function which can assign each config to the Window.ratanConfig
- XMLHTTPRequest.open("GET", url, true)
- XMLHTTPRequest.onload
- Double check the main.js entry if any exist function can check the config file loaded.

JS Script (SSR)

- Write the Config into HTML Script Tag as Javascript Object
- SSR server-side-rendering