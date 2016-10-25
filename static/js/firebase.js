// Initialize Firebase
var config = {
    apiKey: "AIzaSyAsEtFc9Awen5pWY-Zi5fBzJG9HjnrzPGE",
    authDomain: "minebook-b2fe8.firebaseapp.com",
    databaseURL: "https://minebook-b2fe8.firebaseio.com",
    storageBucket: "minebook-b2fe8.appspot.com",
    messagingSenderId: "1087681682464"
};

function Minebook () {
  firebase.initializeApp(config);
  this.provider_ = new firebase.auth.GoogleAuthProvider();
  this.callbacks_ = {}
  this.user_ = null;

  this.on = function(event, callback) {
    this.callbacks_[event] = callback;
  }

  this.performCallback = function (event) {
    var extra = [].slice.call(arguments, 1);
    if (this.callbacks_[event]) {
      this.callbacks_[event].apply(this, extra);
    }
  }

  this.login = function(callback) {
    firebase.auth().signInWithPopup(this.provider_).then(function(result) {
      // This gives you a Google Access Token.
      var token = result.credential.accessToken;
      // The signed-in user info.
      var user = result.user;
      if (callback) callback(user);
    }).catch(function(error) {
      console.log("Error logging in: " + error.errorMessage);
    });
  }

  this.logout = function() {
    firebase.auth().signOut();
  }

  this.setPlayerName = function(player) {
    var user = firebase.auth().currentUser;
    user.updateProfile({displayName: player}).catch(function(error) {
      console.log('Error setting displayName: ' + error);
    });
    firebase.database().ref('users/' + user.uid).set({player_name: player})
      .then(function() {
	this.performCallback('login');
      }).catch(function(error) {
	console.log('Error setting users/uid/player: ' + error);
      });
  }

  this.post = function(content, callback) {
    if (!this.user_) return console.log("Error: not logged in!");
    firebase.database().ref('posts/').push({
      userId: this.user_.uid,
      player: this.user_.displayName,
      content: content,
      date: (new Date).toISOString()
    }).then(function (result) {
      if (callback) return callback(result);
    }).catch(function (error) {
      console.log("Error posting: " + error);
    });
  }

  this.startListeners = function() {
    var self = this;
    // Determine the auth state of the user.
    firebase.auth().onAuthStateChanged(function(user) {
      self.user_ = user;
      if (user) {
	firebase.database().ref('/users/' + user.uid).once('value').then(function(snapshot) {
	  if (snapshot.val().player_name) return self.performCallback('login', self.user_);
	  return self.performCallback('first_login', self.user_);
}).catch(function(error) {
	  console.log(error.message);
	  //return self.performCallback('first_login',user);
	});    
      } else {
	return self.performCallback('logout');
      }
    });
    
    firebase.database().ref('posts/').on('child_added', function(data) {
      self.performCallback('post', data);
    });

    firebase.database().ref('achievements/').on('child_added', function(data) {
      self.performCallback('achievement', data);
    });

    firebase.database().ref('players/').on('child_added', function(data) {
      self.performCallback('player', data);
    });

    firebase.database().ref('players/').on('child_changed', function(data) {
      console.log('players changed');
      self.performCallback('player', data);
    });
  }
};
