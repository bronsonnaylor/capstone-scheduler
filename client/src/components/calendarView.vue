
// I am using this library in order to build this calendar: https://fullcalendar.io/docs/vue

<template>
  <div class='demo-app'>
    <div class='demo-app-top'>
      <button class="button" @click="toggleWeekends">toggle weekends</button>
      <button class="button" @click="gotoPast">go to a date in the past</button>
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
      :editable="calendarEditable"
      :events="calendarEvents"
      :allDaySlot="calendarAllDaySlot"
      :allDayMaintainDuration="calendarAllDayMaintainDuration"
      @dateClick="handleDateClick"
      @eventClick="handleEventClick"
      @select="handleSelectClick"
      @eventDrop="handleDragEvent"
      @eventResize="handleResizeEvent"
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
      calendarEditable: true,
      calendarWeekends: true,
      calendarSelectable: true,
      calendarAllDayMaintainDuration: true,
      eventClickTitle: '',
      eventClickDetails: '',
      newEventClickDate: '',
      selectStartDate: '',
      selectEndDate: '',
      selectAllDay: false,
      dragStartDate: '',
      dragEndDate: '',
      dragEventID: '',
      dragEventName: '',
      calendarAllDaySlot: true,
      resizeEventID: '',
      resizeStart:'',
      resizeEnd: '',
      resizeName: '',
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
      this.selectStartDate = info.startStr;
      this.selectEndDate = info.endStr;
      this.selectAllDay = info.allDay;
      this.$emit('select', this.selectStartDate, this.selectEndDate, this.selectAllDay);
    },
    handleDragEvent(eventDropInfo){
      this.dragEventID = eventDropInfo.event.extendedProps.id;
      this.dragStartDate = eventDropInfo.event.start;
      this.dragEndDate = eventDropInfo.event.end;
      this.$emit('eventDrop', this.dragEventID, this.dragStartDate, this.dragEndDate);
    },
    handleResizeEvent(eventResizeInfo){
      this.resizeEventID = eventResizeInfo.event.id;
      this.resizeStart = eventResizeInfo.event.start;
      this.resizeEnd = eventResizeInfo.event.end;
      this.$emit('eventResize', this.resizeEventID, this.resizeStart, this.resizeEnd);
    },
    eventRender(info) {
    // {description: "Lecture", department: "BioChemistry"}
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