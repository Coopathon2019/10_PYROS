window.onload = function() {
    const useNodeJS = false;   // if you are not using a node server, set this value to false
    const defaultLiffId = "1653449565-XaZnpAML";   // change the default LIFF value if you are not using a node server

    // DO NOT CHANGE THIS
    let myLiffId = "";

    // if node is used, fetch the environment variable and pass it to the LIFF method
    // otherwise, pass defaultLiffId
    if (useNodeJS) {
        fetch('/send-id')
            .then(function(reqResponse) {
                return reqResponse.json();
            })
            .then(function(jsonResponse) {
                myLiffId = jsonResponse.id;
                initializeLiffOrDie(myLiffId);
            })
            .catch(function(error) {
                document.getElementById("liffAppContent").classList.add('hidden');
                document.getElementById("nodeLiffIdErrorMessage").classList.remove('hidden');
            });
    } else {
        myLiffId = defaultLiffId;
        initializeLiffOrDie(myLiffId);
    }
};

/**
* Check if myLiffId is null. If null do not initiate liff.
* @param {string} myLiffId The LIFF ID of the selected element
*/
function initializeLiffOrDie(myLiffId) {
    initializeLiff(myLiffId);
    $.get('/cartlories/like',{userid: liff.getProfile.userId},function(response){
        var i;
            for (i = 0; i < response.length; i++) {
                document.getElementById(response['dishname']).innerHTML = "<i class=\"\" style=\"color: #ee5265;\"></i>";
                document.getElementById(response['dishname']).style = "color: #ee5265; border-color: #ee5265;";
            }
    });
}

/**
* Initialize LIFF
* @param {string} myLiffId The LIFF ID of the selected element
*/
function initializeLiff(myLiffId) {
    liff
        .init({
            liffId: myLiffId
        })
        .then(() => {
            // start to use LIFF's api
        })
        .catch((err) => {
            document.getElementById("liffAppContent").classList.add('hidden');
            document.getElementById("liffInitErrorMessage").classList.remove('hidden');
        });
}

/**
 * Initialize the app by calling functions handling individual app components
 */
function initializeApp() {
    displayLiffData();
    displayIsInClientInfo();
    registerButtonHandlers();

    // check if the user is logged in/out, and disable inappropriate button
    if (liff.isLoggedIn()) {
        document.getElementById('liffLoginButton').disabled = true;
    } else {
        document.getElementById('liffLogoutButton').disabled = true;
    }
}

/**
 * Button listener: Like
 */
 function addToFavorite(item) {
 	var btn = document.getElementById(item.id)
 	var btnText = btn.innerHTML;
 	if (btnText.toString().includes("收藏")) {
 		liff.getProfile().then(function(profile) {
 			var userid = profile.userId;
 			$.post('/cartlories/like', {userid: userid, dishname: item.id});
 		}).catch(function(e) {
 			window.alert('Error getting profile' + e);
 		});
 		document.getElementById(item.id).innerHTML = "<i class=\"\" style=\"color: #ee5265;\"></i>";
 		document.getElementById(item.id).style = "color: #ee5265; border-color: #ee5265;"
 		$(item).find("i").toggleClass("fa fa-heart");
 	}
 }
 /**
  * Button lisntener: pay
  */
 function pay() {
 	liff.scanCode();
 }
 /**
  * Button listener: delete dish
  */
 function deldish(item) {
 	$(item).closest('tr').remove();
}
 