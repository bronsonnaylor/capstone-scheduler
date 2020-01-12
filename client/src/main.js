import Vue from 'vue'
import App from './App.vue'
import VueTags from "vue-tags";

Vue.config.productionTip = false
Vue.component("input-tags", VueTags);


new Vue({
  render: h => h(App),
}).$mount('#app')
