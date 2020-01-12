<template>
    <div class="modal-backdrop">
        <div class="modal">
            <header class="modal-header">
                <button class='x-out-button' @click="close"> X </button>
            </header>
            <section class="modal-body">
                <slot name="body">
                    <h2>{{this.startDate}} : {{this.endDate}}</h2>
                    <label>Event Name:</label>
                    <input v-model="eventName" v-on:keyup.enter="submitNewEvent"/>
                    <label>Event Details:</label>
                    <textarea v-model="eventDetails" v-on:keyup.enter="submitNewEvent"/>
                    <br>
                    <label>Invite Friends:</label>
                    <input-tags v-model="emails">
                    <div class="emails-input"
                        slot-scope="{tag,removeTag,inputEventHandlers,inputBindings }">
                        <div v-for="(email, index) in emails"
                        :key='index'
                        class="tags-input-email">
                        <span>{{ email }}</span>
                        <button type="button" class="tags-input-remove"
                            v-on:click="removeTag(email)"
                        >&times;
                        </button>
                        </div>
                        <input
                        class="email-input-text"  placeholder="Add invitee email..."
                        v-on="inputEventHandlers"
                        v-bind="inputBindings"
                        >
                    </div>
                    </input-tags>
                    <p id="failedEntry" v-if="failedEntry == true">You must be logged in, set a time, enter an event name, and enter a description.</p>
                    <button class="submit" @click="submitNewEvent">Submit</button>
                    <hr>
                    <!--I don't know if we need to show the emails listed here since they are listed above but I changed them so they are a bulleted list instead of just a comma separeted one. We can remove this section though and just have it on the event details modal. **KS-->
                    <!-- <h3 v-if="emails.length > 0">Invitees</h3>
                    <ul>
                        <li v-for="(email, index) in emails" v-bind:key="index">{{ email}}</li>
                    </ul> -->
                    <h3 v-if="emails.length > 0">Add a Message to the Email:</h3>
                    <textarea 
                    v-if="emails.length > 0" 
                    rows="4" 
                    cols="40"
                    v-model='custom_message'
                    >
                    </textarea>
                </slot>
            </section>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import VueTags from "vue-tags"

let moment = require('moment')

export default {
    name: "addEventModal",
    data() {
        return{
            emails: [],
            timeCheckbox: false,  
            eventName: '',
            eventDetails: '',
            eventID: '',
            checkbox: false,
            datetime: '',
            range: [],
            startTime: this.startDate,
            endTime: this.endDate,
            failedEntry: false,
            dragEvent: false,
            custom_message: '',
        }
    },
    components: {
        VueTags
    },
    props: ['userID', 'clearEvents', 'eventsList', 'date', 'startDate', 'endDate', 'allDay'],
    methods: {
        close() {
            this.$emit('close');
        },
        submitNewEvent() {
            this.clearEvents()
            this.failedEntry = false
            this.dragEvent = false

            // Selects start and end times depending on if range is selected or not.
            // this.setStartTime()

            // Sets start time to UTC
            let mStartTime = moment.utc(this.startTime)
            this.startTime = mStartTime.toISOString()
            this.startTime = mStartTime.format("YYYY-MM-DD HH:mm:ss")

            // Sets end time to UTC.
            let mEndTime = moment.utc(this.endTime)
            this.endTime = mEndTime.toISOString()
            this.endTime = mEndTime.format("YYYY-MM-DD HH:mm:ss")

            if (this.userID == "" || this.eventName == "" || this.startTime == "") {
                this.failedEntry = true
                return
            }

            axios.post('/newevent', { owner_id: this.userID, event_name: this.eventName, event_details: this.eventDetails, event_start_time: this.startTime, event_end_time: this.endTime, all_day: this.allDay, drag: this.dragEvent})
            .then((response) => {
                this.eventName = ''
                this.eventDetails = ''
                this.startTime = ''
                this.range = ''
                this.endTime = ''
                this.all_day = false
                this.dragEvent = false
                this.eventsList()
                this.currentEventId = response.data.event_id
                this.sendInviteEmails()
                this.close()
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
        sendInviteEmails(){
            axios.post('/sendinvites', {
                emails: this.emails,
                event_id: this.currentEventId,
                custom_message: this.custom_message
            }).then(() => {
                this.currentEventId = []
            })
        }      
    }
}
</script>

<style scoped>


</style>