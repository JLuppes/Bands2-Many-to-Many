console.log("Toasts script loaded!");

// Bootstrap Toasts script
const toastList = document.getElementsByClassName("toast");

(function showToasts() {
  for (thisToast in toastList) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastList[thisToast]);
    if(toastBootstrap["_element"]){
        toastBootstrap.show();
    }
  }
})()