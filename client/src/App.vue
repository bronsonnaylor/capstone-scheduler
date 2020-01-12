<template>
  <div id="app" >
    
    <div v-if="userLoggedIn" >
      
    <button v-on:click="logout()">Logout</button>

  <div class="calendar_eventdetails"> 
    <div style="width:100%;">
      <calendarView
      :calendarEvents='zippedEvent'
      @eventClick='eventClick'
      @dateClick='dateClick'
      @select='select'
      @eventDrop='eventDrop'
      @eventResize='eventResize'
      />
    </div>
    <div class="centeredModal">
      <eventDetailsModal
        v-if="isModalVisible" 
        @close="closeModal()"
        :title='eventClickTitle'
        :details='eventClickDescription'
        :start='eventClickStart'
        :end='eventClickEnd'
        :invites='eventInvites'
        @deleteEvent='deleteEventNow'
      />
    </div>
    <!-- Enter event information -->
    <div class="centeredModal">
      <!-- Modal window -->
      <addEventModal 
      v-if="showAddEventModal==true"
      @close="closeModal()"
      :date='newEventClickDate'
      :userID='currentUserID'
      :clearEvents='clearEventList'
      :eventsList='getEvents'
      :startDate='newEventStartDate'
      :endDate='newEventEndDate'
      :allDay="newEventAllDay"
      />
    </div>
  </div>
  </div>
  
  <div v-else-if="userRegistrationActive" >
      <register v-on:enterNewUserInfo="enterNewUserInfo" />
  </div>
  <div v-else >
      <login v-on:enterLoginInfo="enterLoginInfo" or v-on:register="register" />
  </div>
  {{this.selectedEventId}}
  </div>
  
</template>

<script>
import axios from 'axios'
import login from './components/login.vue'
import register from './components/register.vue'
import calendarView from './components/calendarView.vue'
import eventDetailsModal from './components/eventDetailsModal.vue'
import addEventModal from './components/addEventModal.vue'

let moment = require('moment')

export default {
  name: 'app',
  data() {
    return {
      userLoggedIn: false,
      userRegistrationActive: false,
      isModalVisible: false,
      currentEventId: '',
      moment: moment,
      inputUserName: '',
      currentUserID: '',
      currentUser: '',
      eventResponseNames: [],
      eventResponseDetails: [],
      eventResponseStartTime: [],
      eventResponseEndTime: [],
      eventResponseID: [],
      zippedEvent: [],
      sharedUsers: [], 
      newEventClickDate: '',
      showAddEventModal: false,
      selectedEventId: '',
      eventInvites: '',
      dragEvent: false
    }        
  },
  components: {
    login,
    register,
    calendarView,
    eventDetailsModal,
    addEventModal,
  },
  methods: {

    checkSession() {
        axios.get('checksession')
        .then((resp) => {
            this.userLoggedIn = resp.data.session

            this.getCurrentUserID()
            this.getEvents()
      })
    },

    logout() {
      axios.get('logout')
         .then((resp) => {
            this.userLoggedIn = false;
            this.userRegistrationActive = false;
    })
      
    },
    enterLoginInfo (value) { 
     this.userLoggedIn = value

     if (this.userLoggedIn === true) {
        this.getCurrentUserID()
        this.getEvents()
     }
    },

    register (value) {
     this.userRegistrationActive = value
     
    },

    enterNewUserInfo (value) {
      this.userLoggedIn = value
      if (this.userLoggedIn === true)
        this.getCurrentUserID();
      
    },

    sendInviteEmails(){
      axios.post('/sendinvites', {
        emails: this.emails,
        event_id: this.currentEventId
      }).then(() => {
        this.currentEventId = []
      })
  },
 
    eventClick(title, description, start, end, id) {
      this.eventClickTitle = title
      this.eventClickDescription = description
      this.eventClickStart = start
      this.eventClickEnd = end
      this.isModalVisible = true
      this.getInvites(id)
      this.selectedEventId = id
    },
    getInvites(id) {
      axios.post('/getinvites',{
        event_id: id
      }).then(resp => {
        this.eventInvites = resp.data.all_invites
      })
    },
    dateClick(date){
      this.newEventClickDate = date;
      this.showAddEventModal = true;
    },
    select(start, end, fullDay){
      this.showAddEventModal = false;
      this.newEventStartDate = start;
      this.newEventEndDate = end;
      this.showAddEventModal = true;
      this.newEventAllDay = fullDay;
    },
    eventDrop(dragID, dragStart, dragEnd, dragName){
      // Sets start time to UTC
      let dragEventStartDate = moment.utc(dragStart)
      dragStart = dragEventStartDate.toISOString()
      dragStart = dragEventStartDate.format("YYYY-MM-DD HH:mm:ss")

      // Sets end time to UTC.
      let dragEventEndDate = moment.utc(dragEnd)
      dragEnd = dragEventEndDate.toISOString()
      dragEnd = dragEventEndDate.format("YYYY-MM-DD HH:mm:ss")
      this.dragEvent = true;

      axios.patch('/updateevent', { id: dragID, start_time: dragStart, end_time: dragEnd, drag: this.dragEvent})
      .then(() => {
        this.getEvents()
      });
      axios.post('/eventchanged', {
        id: dragID,
        start_time: dragStart,
        end_time: dragEnd,
      })
      .then(() => {
      })
    },
    eventResize(resizeID, resizeStart, resizeEnd){
      // Sets start time to UTC
      let resizeEventStartDate = moment.utc(resizeStart)
      resizeStart = resizeEventStartDate.toISOString()
      resizeStart = resizeEventStartDate.format("YYYY-MM-DD HH:mm:ss")

      // Sets end time to UTC.
      let resizeEventEndDate = moment.utc(resizeEnd)
      resizeEnd = resizeEventEndDate.toISOString()
      resizeEnd = resizeEventEndDate.format("YYYY-MM-DD HH:mm:ss");

      axios.patch('/updateevent', { id: resizeID, start_time: resizeStart, end_time: resizeEnd, drag: false})
      .then(() => {
        this.getEvents()
      });
      axios.post('/eventchanged', {
        id: resizeID,
        start_time: resizeStart,
        end_time: resizeEnd,
      })
      .then(() => {
      })
    },
    closeModal() {
      this.isModalVisible = false;
      this.showAddEventModal = false;
    },
    deleteEventNow() {
      axios.post('/deleteevent', {event_id: this.selectedEventId })
      .then(() => {
        this.closeModal()
        this.getEvents()
      })
    },
    clearEventList() {
      this.zippedEvent = []
    },
    //use function below but don't break it
    // perhaps if userLoggedIN === true getCurrentUserID()
    //currentResponse is acquiring the correct ID but only
    //at first login of user, not after refresh of browser, errors
    //that it does get after first login I don't recognize

    getCurrentUserID() {
      axios.get('/user')
      .then((response) => {
        //no console log here at first registration
        this.currentUserID = response.data.usernames
        console.log("currentuserid line    "   + this.currentUserID)
        
      })
    },
    submitNewUsername() {
      // I believe there is a race condition somewhere that sometimes prevents the list of events from updating on the webpage.
      // I included an "Update events" button to manually fix the problem.
      axios.post('/usersignup', { new_user: this.inputUserName })
      .then(() => {
        this.currentUser = this.inputUserName //Steve: this is a crucial part of the code already written
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

            this.eventResponseNames.push(currentResponse[i])
            this.eventResponseDetails.push(currentResponse[i])
            this.eventResponseStartTime.push(currentResponse[i])
            this.eventResponseEndTime.push(currentResponse[i])
            this.eventResponseID.push(currentResponse[i])
          }
        }
        for (let i = 0; i < this.eventResponseNames.length; i++) {
          //if the event is all day keep the time in utc, otherwise it will change the start time to the previous day **KS
          let stringConvertStartTime = this.eventResponseStartTime[i].start_time
          let stringConvertEndTime = this.eventResponseEndTime[i].end_time
          if (!this.eventResponseStartTime[i].drag) {
            if (this.eventResponseStartTime[i].all_day == false){
              stringConvertStartTime = this.utcToLocalTime(stringConvertStartTime);
              stringConvertEndTime = this.utcToLocalTime(stringConvertEndTime);
            } 
          } else {
            stringConvertStartTime = this.utcToLocalTime(stringConvertStartTime);
            stringConvertEndTime = this.utcToLocalTime(stringConvertEndTime);
          }     
             
          //the zipped event must be in this format in order for calendarview to display it(as an object) **PK
          
          this.zippedEvent.push({
            title: this.eventResponseNames[i].event_name, 
            start: stringConvertStartTime,
            end: stringConvertEndTime,
            id: currentResponse[i].id,
            extendedProps: {
              title: this.eventResponseNames[i].event_name,
              description: this.eventResponseDetails[i].details,
              start: stringConvertStartTime,
              end: stringConvertEndTime, 
              id: currentResponse[i].id,
            },
            })
            //  ** PK
            //Maybe I will use these later? ** PK
        }
        this.eventResponseNames = []
        this.eventResponseDetails = []
        this.eventResponseStartTime = []
        this.eventResponseEndTime = []
      })
    },
    utcToLocalTime(date){
      var stillUtc = moment.utc(date).toDate();
      var local = moment(stillUtc).local().format('YYYY-MM-DD HH:mm:ss');
      return local;
    }

  },
  mounted () {
    this.checkSession();
  }
}



</script>

<style>
  @import './assets/css/normalize.css';
  @import url(https://fonts.googleapis.com/css?family=Roboto:400,900&display=swap);
  @import './assets/css/styles.css';
  
</style>
