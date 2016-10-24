// Initialize Firebase
var config = {
    apiKey: "AIzaSyAsEtFc9Awen5pWY-Zi5fBzJG9HjnrzPGE",
    authDomain: "minebook-b2fe8.firebaseapp.com",
    databaseURL: "https://minebook-b2fe8.firebaseio.com",
    storageBucket: "minebook-b2fe8.appspot.com",
    messagingSenderId: "1087681682464"
};

firebase.initializeApp(config);
var provider = new firebase.auth.GoogleAuthProvider();
var OnLogin_ = function () {};
var OnLogout_ = function () {};
var OnFirstLogin_ = function () {};

function login(callback) {
    firebase.auth().signInWithPopup(provider).then(function(result) {
        // This gives you a Google Access Token.
        var token = result.credential.accessToken;
        // The signed-in user info.
	var user = result.user;
	if (callback) callback(user);
    }).catch(function(error) {
	console.log("Error logging in: " + error.errorMessage);
    });
}

function logout() {
    firebase.auth().signOut();
}

function setPlayerName(player) {
  var user = firebase.auth().currentUser;
  user.updateProfile({displayName: player}).catch(function(error) {
    console.log('Error setting displayName: ' + error);
  });
  firebase.database().ref('users/' + user.uid).set({player_name: player})
    .then(function() {
      OnLogin_();
    }).catch(function(error) {
      console.log('Error setting users/uid/player: ' + error);
    });
}

function setLoginPath(OnFirstLogin, OnLogin, OnLogout) {
  if (OnFirstLogin) OnFirstLogin_ = OnFirstLogin;
  if (OnLogin) OnLogin_ = OnLogin;
  if (OnLogout) OnLogout_ = OnLogout;
}

// Determine the auth state of the user.
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    firebase.database().ref('/users/' + user.uid).once('value').then(function(snapshot) {
      if (snapshot.val().player_name) return OnLogin_(user);
      OnFirstLogin_(user);
    }).catch(function(error) {
      console.log(error.message);
      OnFirstLogin_(user);
    });    
  } else {
    OnLogout_(user);
  }
});
