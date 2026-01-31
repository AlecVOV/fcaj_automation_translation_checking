import './assets/styles/global.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// AWS Amplify Configuration
import { Amplify } from 'aws-amplify'
import { awsConfig } from './config/aws-config'

// Configure Amplify
Amplify.configure(awsConfig)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')