
// I am using this library in order to build this calendar: https://fullcalendar.io/docs/vue

<template>
  <div class='demo-app'>
    <div class='demo-app-top'>
      <button class="button" @click="toggleWeekends">toggle weekends</button>
      <button class="button" @click="gotoPast">go to a date in the past</button>
      <button class="button" @click="displayGroups();">your groups</button>
      (also, click a date/time to add an event)
    </div>
    <FullCalendar
      class='demo-app-calendar'
      ref="fullCalendar"
      defaultView="dayGridMonth"
      :header="{
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
      }"
      :views="{
        dayGridMonth: {
          details:'here are the event details'
        }
      }"
      :plugins="calendarPlugins"
      :weekends="calendarWeekends"
      :selectable='calendarSelectable'
      :events="calendarEvents"
      @dateClick="handleDateClick"
      @eventClick="handleEventClick"
      @select="handleSelectClick"
      />
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  name: 'calendarView',
  props: ['calendarEvents'],
  components: {
    FullCalendar // make the <FullCalendar> tag available ** PK
  },
  data() {
    return {
      calendarPlugins: [ // plugins must be defined in the JS ** PK
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin // needed for dateClick ** PK
      ],
      timeZone: 'local',
      calendarWeekends: true,
      calendarSelectable: true,
      eventClickTitle: '',
      eventClickDetails: '',
      newEventClickDate: '',
      selectStartDate: '',
      selectEndDate: '',
      selectAllDay: false,
      isGroupsModalVisible: false,
      
    }
  },
  methods: {
    toggleWeekends() {
      this.calendarWeekends = !this.calendarWeekends // update a property **PK
    },
    gotoPast() {
      let calendarApi = this.$refs.fullCalendar.getApi(); // from the ref="..." ** PK
      calendarApi.gotoDate('2000-01-01'); // call a method on the Calendar object ** PK
    },
    handleDateClick(arg) {
      // console.log('this is the date:'+ arg.date);
      // console.log(arg);
      /* TODO This is for you Kristin to put in the modal view show function, 
      I have provided you the arg.date here so you can auto populate that ** PK */
      this.newEventClickDate = arg.date;
      this.$emit('dateClick', this.newEventClickDate);
    },
    handleEventClick(arg) {
      this.eventClickTitle = arg.event.extendedProps.title
      this.eventClickDetails = arg.event.extendedProps.description
      this.eventClickStart = arg.event.extendedProps.start
      this.eventClickEnd = arg.event.extendedProps.end
      this.eventClickId = arg.event.extendedProps.id
      this.$emit('eventClick', this.eventClickTitle, this.eventClickDetails, this.eventClickStart, this.eventClickEnd, this.eventClickId) 
    },
    handleSelectClick(info) {
      // console.log('selected ' + info.startStr + ' to ' + info.endStr);
      // console.log('selected date ' + info.start + ' to ' + info.end);
      // console.log('all day?' + info.allDay);
      this.selectStartDate = info.startStr;
      this.selectEndDate = info.endStr;
      this.selectAllDay = info.allDay;
      this.$emit('select', this.selectStartDate, this.selectEndDate, this.selectAllDay);
    },
    
    eventRender(info) {
    // {description: "Lecture", department: "BioChemistry"}
    },
    displayGroups() {
      console.log("displayGroups")
      this.isGroupsModalVisible = true;
      this.$emit('displayGroups', this.isGroupsModalVisible);

    
    }
  }
}

</script>

<style lang='scss'>

// you must include each plugins' css ** PK
// paths prefixed with ~ signify node_modules ** PK
@import '~@fullcalendar/core/main.css';
@import '~@fullcalendar/daygrid/main.css';
@import '~@fullcalendar/timegrid/main.css';

.demo-app {
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.demo-app-top {
  margin: 0 0 3em;
}

.demo-app-calendar {
  margin: 0 auto;
  max-width: 900px;
}

</style>