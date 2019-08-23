import Vue from 'vue'
import Vuetify from 'vuetify'

import store from './store.js'
import router from './router.js'
import App from './App.vue'

import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Vuetify)
Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
