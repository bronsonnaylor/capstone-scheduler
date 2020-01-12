<template>
    <div class="modal-backdrop">
        <div class="modal">
            <header class="modal-header">
                <button class='x-out-button' @click="close"> X </button>
            </header>
            <section class="modal-body">
                <slot name="body">
                    <div>
                        <p>{{start}} - {{end}}</p>
                        <h2>{{ title }}</h2>
                        <p>{{ details }}</p>
                        <p class ='invites' :class='isAccepted(invite)' v-for='(invite, index) in invites' :key='index'> {{invite.email}}</p>
                    </div>
                </slot>
            </section>
        </div>
    </div>
</template>

<script>
export default {
    name: "eventDetailsModal",
    props: ['title', 'details','start','end', 'invites'],
    methods: {
        close() {
        this.$emit('close');
        },
        isAccepted(invite) {
            if (invite.accepted == true) {
                return 'is-coming'
            } else {
                return 'not-coming'
            }
        }
    }
}
</script>

<style scoped>
.invites {
    display:flex;
    flex-direction: column;
}
.is-coming {
    background: rgb(213, 255, 213);
}
.not-coming {
    background: rgb(255, 214, 214);
}
</style>