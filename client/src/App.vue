<template>
  <div id="app">
    <input v-if="this.currentUser == '' " v-model="inputUserName"/>
    <button v-if="this.currentUser == '' " @click="submitNewUsername">Enter a username</button>
    <p v-if="this.currentUser != '' ">Welcome {{ currentUser }}!</p>
    <button v-if="this.currentUser != '' " @click="switchUser">Change user</button>

    <hr>

    <input type="checkbox" id="rangeCheckbox" v-model="checkbox">
    <label for="rangeCheckbox">Check this box to select a start and end time.</label>
    <br>
    <p v-if="!checkbox">Select start time.</p>
    <p v-if="checkbox">Select start and end time.</p>
    <date-picker v-if="!checkbox" v-model="datetime" lang="en" confirm type="datetime"  format="YYYY-MM-DD HH:mm:ss" width="500" placeholder="Select Date and Time"></date-picker>
    <date-picker v-if="checkbox" v-model="range" lang="en" range confirm type="datetime" format="YYYY-MM-DD HH:mm:ss" value-type="format" width="500" placeholder="Select Date and Time"></date-picker>
    <p>Enter event name here.</p>
    <input v-model="eventName"/>
    <p>Enter event details here.</p>
    <textarea v-model="eventDetails"/>
    <br>
    <p id="failedEntry" v-if="failedEntry">You must be logged in, set a time, enter an event name, and enter a description.</p>
    <button @click="submitNewEvent">Submit</button>

    <hr>

    <h2>My events</h2>
    <button @click="getEvents">Update my events</button>
    
    <br>
    <p>range {{ this.range }}</p>
    <p>datetime {{ this.datetime }}</p>
    <p>zipped {{ this.zippedEvent }}</p>

    <button @click="test">test</button>
    <div id=eventList>
      <ul v-for="(event, index) in zippedEvent" :key="index">
        <li> {{ event[0] }} </li>
        <li> {{ event[1] }} </li>
        <li> {{ event[2] }} </li>
        <p>---------------------------------</p>
      </ul>
    </div>
    
  </div>
</template>

<script>
import DatePicker from 'vue2-datepicker'
import axios from 'axios'

let moment = require('moment')

export default {
  name: 'app',
  data() {
    return {
      moment: moment,
      inputUserName: '',
      currentUser: '',
      currentUserID: '',
      eventName: '',
      eventDetails: '',
      eventResponseNames: [],
      eventResponseDetails: [],
      eventResponseStartTime: [],
      eventResponseEndTime: [],
      zippedEvent: [],
      sharedUsers: [],
      checkbox: false,
      datetime: '',
      convertedDatetime: [],
      timezone: [],
      timezoneStart: 0,
      timezoneEnd: 0,
      startTime: '',
      endTime: '',
      range: [],
      failedEntry: false
    }        
  },
  components: {
    DatePicker
  },
  methods: {
    submitNewEvent() {
      this.clearEventList()
      // let m = moment.utc()
      if (this.range != []) {
        this.datetime = this.range[0]

        // this.datetime = m.toISOString()
        // this.datetime = m.format("YYYY-MM-DD HH:mm:ss")
        // this.endTime = this.range[1]

        // let mEndTime = this.range[1]
        // this.endTime = mEndTime.toISOString()
        // this.datetime = mEndTime.format("YYYY-MM-DD HH:mm:ss")
        // console.log("times ", mEndTime)
      }
      let mDatetime = moment.utc(this.datetime)
      this.datetime = mDatetime.toISOString()
      this.datetime = mDatetime.format("YYYY-MM-DD HH:mm:ss")
      console.log("Passed format: ", this.datetime)

      if (this.currentUserID == "" || this.eventName == "" || this.datetime == "") {
        this.failedEntry = true
        return
      }

      axios.post('/newevent', { owner_id: this.currentUserID, event_name: this.eventName, event_details: this.eventDetails, event_start_time: this.datetime})
      .then(() => {
        
      })
        this.eventName = ''
        this.eventDetails = ''
        this.datetime = ''
        this.range = ''
        this.endTime = ''
        this.getEvents()
    },
    test() {
      let mDatetime = moment.utc(this.datetime)
      this.datetime = mDatetime.toISOString()
      this.datetime = mDatetime.format("YYYY-MM-DD HH:mm:ss")
      // this.datetime = m.format("YYYY-MM-DD HH:mm:ss")
      // this.endTime = m.toISOString()
    },
    clearEventList() {
      console.log("got into clear")
      this.zippedEvent = []
      console.log("clear ", this.zippedEvent)
      const listID = document.getElementById("eventList")
      if (listID.firstChild) {
        while (listID.firstChild) listID.removeChild(listID.firstChild)
      }
    },
    getCurrentUserID() {
      axios.get('/user')
      .then((response) => {
        let currentResponse = response.data.usernames
        for (let i = 0; i < currentResponse.length; i++) {
          if (this.currentUser === currentResponse[i].username) {
            this.currentUserID = currentResponse[i].id
          }
        }
      })
    },
    submitNewUsername() {
      axios.post('/usersignup', { new_user: this.inputUserName })
      .then(() => {
        this.currentUser = this.inputUserName
        this.inputUserName = ""
        this.getCurrentUserID()
        this.getEvents()
      }, () => {
        this.currentUser = this.inputUserName
        this.inputUserName = ''
        this.getCurrentUserID()
        this.getEvents()
      })
      .catch(() => {
        this.getCurrentUserID()
        this.getEvents()
      })
    },
    switchUser() {
      this.currentUserID = ''
      this.currentUser = ''
      this.clearEventList()
    },
    getEvents() {
      this.clearEventList()
      console.log("getEvents ", this.zippedEvent)
      axios.get('/getevents')
      .then((response) => {
        let currentResponse = response.data.all_events
        console.log(currentResponse)
        for (let i = 0; i < currentResponse.length; i++) {
          if (this.currentUserID === currentResponse[i].owner_id) {
            this.eventResponseNames.push(currentResponse[i].event_name)
            this.eventResponseDetails.push(currentResponse[i].details)
            this.eventResponseStartTime.push(currentResponse[i].datetime)
            this.eventResponseEndTime.push(currentResponse[i].range)
          }
        }
        for (let i = 0; i < this.eventResponseNames.length; i++) {
          // Sometimes this function fails to execute this for loop. I haven't found the cause yet.
          let stringConvertStartTime = this.eventResponseDatetime[i].toString()
          let stringConvertEndTime = this.eventResponseDatetime[i].toString()
          this.zippedEvent.push([stringConvertStartTime, stringConvertEndTime, this.eventResponseNames[i], this.eventResponseDetails[i]])
        }
        this.eventResponseNames = []
        this.eventResponseDetails = []
        this.eventResponseDatetime = []
      })
    }
  }
}
</script>

<style>

</style>
