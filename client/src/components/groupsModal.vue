<template>
    <div class="modal-backdrop">
        <div class="modal">
            <header class="modal-header">
                <button class='x-out-button' @click="close"> X </button>
            </header>
            <section class="modal-body">
                <slot name="body">
                <p>groupmodaltest</p>
                </slot>
            </section>
        </div>
    </div>
</template>

<script>
export default {
    name: "groupsModal",
    
    methods: {
        close() {
        this.$emit('close');
        },
        
    }
}
</script>

<style scoped>

</style>