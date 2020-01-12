<template>
  <div class="boxes">
  
    <input v-model="enteredUserName" id="enteredUserName" /><label for="enteredUserName"> Enter your User Name</label>
    <br>
    <input v-model="enteredPassword" type="password" /><label for="enteredPassword"> Enter your password</label>
    <br>
    <button v-on:click="enterLoginInfo();">Login to the Purple Cape Scheduler</button>
    <br>
    <div v-if="loginInfoBool === false">
      Login info invalid. Please try again.
    </div>
    <p>Don't have a Purple Cape Scheduler?</p>
    <button v-on:click="register();">Register Here</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "login",
  
  data () {
    return {
      userLoggedIn: true,
      userRegistrationActive: false,
      loginInfoBool: '',
      enteredUserName: '',
      enteredPassword: '',
      
      }
},

methods: {

    enterLoginInfo() {
        axios.post('user_login', { username_item: this.enteredUserName, password_item: this.enteredPassword })
        this.verifyLogin();
    },
    register() {
      this.userRegistrationActive = true;
      this.$emit('register', this.userRegistrationActive)
    },
    verifyLogin() {
      axios.get('verify_login')
          .then((resp) => {
            this.loginInfoBool = resp.data.loginbool;
            if (this.loginInfoBool === true) {
              this.$emit('enterLoginInfo', this.userLoggedIn)
             }
          }) 
    },

  },
  mounted() {
    this.checkSession();
  }



}
</script>
<style>
.boxes {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  text-align: right;
  margin: 10% 0;
  min-height: 200px;
  background-color: rgba(33, 33, 33, .3);
  align-items: center;
}
.boxes :first-child {
    align-self: center;
}
</style>

