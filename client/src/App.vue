<template>
  <div id="app">
    <h1>Event scheduler</h1>

    <!-- Crude login -->
    <input v-if="this.currentUser == '' " v-model="inputUserName" v-on:keyup.enter="submitNewUsername"/>
    <button v-if="this.currentUser == '' " @click="submitNewUsername">Enter a username</button>
    <p v-if="this.currentUser != '' ">Welcome {{ currentUser }}!</p>
    <button v-if="this.currentUser != '' " @click="switchUser">Change user</button>
    <hr>

    <!-- Make API call to find time at specific location -->
    <input type="checkbox" class="check" id="timeCheckbox" v-model="timeCheckbox">
    <label for="timeCheckbox">Check this box to find the current time for a specific location</label>
    <br>
    <div v-if="this.timeCheckbox == true">
      <button @click="updateZones" v-on:keyup.enter="updateZones">Update timezones</button>
      <select v-model="chosenTimezoneNumber" @click="selectTimezone">
        <option v-for="(zone, key) in zones" :value="key">
          {{ zone }}
        </option>
      </select>
      <p>{{ chosenTimezoneString }}</p>
    </div>

    <!-- Enter event information -->
    <input type="checkbox" class="check" id="rangeCheckbox" v-model="checkbox">
    <label for="rangeCheckbox">Check this box to select a start and end time.</label>
    <br>
    <p v-if="!checkbox">Select start time.</p>
    <p v-if="checkbox">Select start and end time.</p>
    <date-picker v-if="!checkbox" v-model="datetime" lang="en" confirm type="datetime"  format="YYYY-MM-DD HH:mm:ss" width="500" placeholder="Select Date and Time"></date-picker>
    <date-picker v-if="checkbox" v-model="range" lang="en" range confirm type="datetime" format="YYYY-MM-DD HH:mm:ss" width="500" placeholder="Select Date and Time"></date-picker>
    <p>Enter event name here.</p>
    <input v-model="eventName" v-on:keyup.enter="submitNewEvent"/>
    <p>Enter event details here.</p>
    <textarea v-model="eventDetails" v-on:keyup.enter="submitNewEvent"/>
    <br>
    <p id="failedEntry" v-if="failedEntry == true">You must be logged in, set a time, enter an event name, and enter a description.</p>
    <button @click="submitNewEvent">Submit</button>
    <hr>

    <!-- list all events for current user -->
    <h2>My events</h2>
    <button @click="getEvents">Update my events</button>
    <br>
    <div id=eventList>
      <ul v-for="(event, index) in zippedEvent" :key="index">
        <li> {{ event[0] }} </li>
        <li> {{ event[1] }} </li>
        <li> {{ event[2] }} </li>
        <li> {{ event[3] }} </li>
        <button @click="deleteEvent(event[4])">Delete event</button>
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
      eventID: '',
      eventResponseNames: [],
      eventResponseDetails: [],
      eventResponseStartTime: [],
      eventResponseEndTime: [],
      eventResponseID: [],
      zippedEvent: [],
      sharedUsers: [],
      chosenTimezoneNumber: null,
      chosenTimezoneName: "",
      chosenTimezoneString: "",
      timeCheckbox: false,
      checkbox: false,
      datetime: '',
      zones: [],
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
      this.failedEntry = false

      // Selects start and end times depending on if range is selected or not.
      this.setStartTime()

      // Sets start time to UTC
      let mStartTime = moment.utc(this.startTime)
      this.startTime = mStartTime.toISOString()
      this.startTime = mStartTime.format("YYYY-MM-DD HH:mm:ss")

      // Sets end time to UTC.
      let mEndTime = moment.utc(this.endTime)
      this.endTime = mEndTime.toISOString()
      this.endTime = mEndTime.format("YYYY-MM-DD HH:mm:ss")

      if (this.currentUserID == "" || this.eventName == "" || this.startTime == "") {
        this.failedEntry = true
        return
      }

      axios.post('/newevent', { owner_id: this.currentUserID, event_name: this.eventName, event_details: this.eventDetails, event_start_time: this.startTime, event_end_time: this.endTime})
      .then(() => {
        
      })
        this.eventName = ''
        this.eventDetails = ''
        this.startTime = ''
        this.range = ''
        this.endTime = ''
        this.getEvents()
    },
    deleteEvent(id) {
      // There is currently an issue with the delete button failing to remove list items sometimes.
      // Refreshing the page restores proper functionality.
      // Update: perhaps it's related to a potential race condition, where the updated list isn't properly rendered in time.
      axios.delete('/deleteevent', {data: { event_id: id } })
      .then(() => {
        this.getEvents()
      })
    },
    setStartTime() {
      if (this.range.length != 0) {
        this.startTime = this.range[0]
        this.endTime = this.range[1]
        return
      }
      this.startTime = this.datetime
      this.endTime = this.datetime
      return
    },
    clearEventList() {
      this.zippedEvent = []
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
      // I believe there is a race condition somewhere that sometimes prevents the list of events from updating on the webpage.
      // I included an "Update events" button to manually fix the problem.
      axios.post('/usersignup', { new_user: this.inputUserName })
      .then(() => {
        this.currentUser = this.inputUserName
        this.inputUserName = ""
        this.getCurrentUserID()
        this.getEvents()
      // Maybe this part was unnecissary. I was tinkering for a long time. If it aint broke...
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
      axios.get('/getevents')
      .then((response) => {
        let currentResponse = response.data.all_events
        for (let i = 0; i < currentResponse.length; i++) {
          if (this.currentUserID === currentResponse[i].owner_id) {

            this.eventResponseNames.push(currentResponse[i].event_name)
            this.eventResponseDetails.push(currentResponse[i].details)
            this.eventResponseStartTime.push(currentResponse[i].start_time)
            this.eventResponseEndTime.push(currentResponse[i].end_time)
            this.eventResponseID.push(currentResponse[i].id)
          }
        }
        for (let i = 0; i < this.eventResponseNames.length; i++) {
          let stringConvertStartTime = this.eventResponseStartTime[i].toString()
          let stringConvertEndTime = this.eventResponseEndTime[i].toString()
          this.zippedEvent.push([stringConvertStartTime, stringConvertEndTime, this.eventResponseNames[i], this.eventResponseDetails[i], this.eventResponseID[i]])
        }
        this.eventResponseNames = []
        this.eventResponseDetails = []
        this.eventResponseStartTime = []
        this.eventResponseEndTime = []
      })
    },

    // API calls in the next two methods.
    updateZones() {
      axios.get("http://worldtimeapi.org/api/timezone")
      .then((response) => {
        this.zones = response.data
      })
    },
    selectTimezone() {
      this.chosenTimezoneName = this.zones[this.chosenTimezoneNumber]
      axios.get(`http://worldtimeapi.org/api/timezone/${this.chosenTimezoneName}`)
      .then((response) => {
        this.chosenTimezoneString = moment(response.data.datetime).toString()
      })
    }
  }
}
</script>

<style>
  #failedEntry {
    color: red;
  }
  #app{
    background-image: url("assets/photo-1455612693675-112974d4880b.jpeg");
    background-size: 1000px;
  }
  textarea {
    border: 2px solid black;
    background-color: lightgray;    
  }
  input {
    border: 2px solid black;
    background-color: lightgray;
  }

  /* this one actually works on the datetime picker */
  input[type=text] {
    border: 2px solid black;
    background-color: lightgray;
    font-weight: bold;
  }
  .check {
    border: 2px solid black;
  }
  label {
    font-weight: bold;
  }
  p {
    font-weight: bold;
  }
  button {
    font-weight: bold;
  }
  li {
    font-weight: bold;
  }
</style>
