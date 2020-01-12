<template>
  <div class="boxes">
    
    <p>Register with The Purple Cape Scheduler</p>
    <br>

    <input v-model="newUserName" id="newUserName" /><label for="newUserName"> Enter a User Name</label>
    <br>
    <input v-model="newPassword" type="password" /><label for="newPassword"> Enter a password</label>
    <br>
    <input v-model="passwordConfirm" type="password" /><label for="passwordConfirm"> Confirm your password</label>
    <br>
    <button v-on:click="enterNewUserInfo();">Register for the Purple Cape Scheduler</button>
    <br>

    <div v-if="userNameBool === false">
      That user name is taken. Please select a unique user name.
    </div>
    <div v-if="passMatchBool === false">
      Your password and password confirmation do not match. Please enter the same password twice.
    </div>


    </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "register",
  
  data () {
    return {
      userLoggedIn: false,
      userRegistrationActive: true,
      passMatchBool: '',
      userNameBool: '',
      newUserName: '',
      newPassword: '',
      passwordConfirm: '',
      
      }
},

methods: {
    
     enterNewUserInfo () {
        axios.post('usersignup', { new_user: this.newUserName, new_password: this.newPassword, 
                  new_pass_confirm: this.passwordConfirm }).then((resp)  => {
                    this.userRegistered = resp.data.regBool;
                    this.passMatchBool = resp.data.passwordBool;
                    this.userNameBool = resp.data.newNameBool;
                    if (this.userRegistered === true) {
                      this.userLoggedIn = true;
                      this.$emit('enterNewUserInfo', this.userLoggedIn)
                      }
                    
                  })

     },
  mounted() {
     
  }
  
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
